import os
import sqlite3
import json
import asyncio
import io
import requests
from typing import List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import paho.mqtt.client as mqtt
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(title="Vermikendra Offline API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.getenv('VK_DB_PATH', 'vermikendra.db')
MQTT_BROKER = os.getenv('VK_MQTT_BROKER', '127.0.0.1')
MQTT_PORT = int(os.getenv('VK_MQTT_PORT', '1883'))
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', '')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------------------------------
# WEBSOCKET MANAGER
# ---------------------------------------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

def on_mqtt_connect(client, userdata, flags, rc):
    print(f"[*] API MQTT Connected. Code {rc}")
    client.subscribe("vk/+/+/up")

def on_mqtt_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        asyncio.run_coroutine_threadsafe(manager.broadcast(payload), loop)
    except Exception as e:
        print(f"[!] MQTT->WS Bridge Error: {e}")

mqttc = mqtt.Client()
mqttc.on_connect = on_mqtt_connect
mqttc.on_message = on_mqtt_message

@app.on_event("startup")
async def startup_event():
    try:
        mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqttc.loop_start()
    except Exception as e:
        print(f"[!] Could not start API MQTT listener: {e}")

@app.on_event("shutdown")
def shutdown_event():
    mqttc.loop_stop()

# ---------------------------------------------------------
# TTS PROVIDERS ABSTRACTION
# ---------------------------------------------------------
class TTSProvider:
    def synthesize(self, text: str, language: str) -> bytes:
        raise NotImplementedError()

class SarvamTTSProvider(TTSProvider):
    def synthesize(self, text: str, language: str) -> bytes:
        if not SARVAM_API_KEY:
            raise Exception("SARVAM_API_KEY not configured on server.")
        
        # https://api.sarvam.ai/text-to-speech
        url = "https://api.sarvam.ai/text-to-speech"
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json"
        }
        # Sarvam expects code like 'hi-IN', 'en-IN'
        data = {
            "inputs": [text],
            "target_language_code": language,
            "speaker": "meera", # typical default female voice
            "pitch": 0,
            "pace": 1.0,
            "loudness": 1.5,
            "speech_sample_rate": 16000,
            "enable_preprocessing": True,
            "model": "bulbul:v1"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Sarvam TTS failed: {response.text}")
        
        # Response contains base64 encoded audio
        import base64
        audio_base64 = response.json()['audios'][0]
        return base64.b64decode(audio_base64)

class HuggingFaceTTSProvider(TTSProvider):
    def synthesize(self, text: str, language: str) -> bytes:
        # [?] UNVERIFIED: Local inference stub
        raise Exception("Hugging Face TTS provider not yet benchmarked/implemented.")

def get_tts_provider() -> TTSProvider:
    provider_name = os.getenv('TTS_PROVIDER', 'sarvam')
    if provider_name == 'sarvam':
        return SarvamTTSProvider()
    elif provider_name == 'huggingface':
        return HuggingFaceTTSProvider()
    else:
        raise Exception(f"Unknown TTS provider: {provider_name}")

# ---------------------------------------------------------
# API ENDPOINTS
# ---------------------------------------------------------
@app.get("/api/health")
def health_check():
    return {"status": "ok", "system": "vermikendra"}

@app.get("/api/nodes/{node_id}/telemetry/latest")
def get_latest_telemetry(node_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM readings 
        WHERE node_id = ? 
        ORDER BY ts DESC LIMIT 1
    ''', (node_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="No telemetry found for node")
    return dict(row)

@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ---------------------------------------------------------
# VOICE ASSISTANT PIPELINE
# ---------------------------------------------------------
@app.post("/api/assistant/voice")
async def process_voice_query(
    audio: UploadFile = File(...),
    language: str = Form(...),
    node_id: int = Form(...)
):
    """
    1. STT via Sarvam Saaras
    2. Context Build (Telemetry)
    3. Deterministic Answer Gen
    4. TTS via configured provider (Bulbul)
    """
    
    # --- 1. STT (Mocked if no key, otherwise real request) ---
    if not SARVAM_API_KEY:
        # Without a key, we cannot transcribe, but we simulate a safe fallback
        # for offline testing to prove the pipeline architecture.
        transcription = "What is the status of the bed?"
        print("[!] No SARVAM_API_KEY. Simulating STT transcription.")
    else:
        audio_content = await audio.read()
        # Real Sarvam STT Call
        url = "https://api.sarvam.ai/speech-to-text"
        headers = {"api-subscription-key": SARVAM_API_KEY}
        files = {
            'file': ('question.webm', audio_content, 'audio/webm')
        }
        data = {'language_code': language}
        try:
            r = requests.post(url, headers=headers, files=files, data=data, timeout=10)
            if r.status_code == 200:
                transcription = r.json().get('transcript', '')
            else:
                raise HTTPException(status_code=500, detail="Transcription failed")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Voice service unavailable")

    # --- 2. Context Build ---
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM readings WHERE node_id = ? ORDER BY ts DESC LIMIT 1', (node_id,))
    latest = cursor.fetchone()
    conn.close()
    
    # --- 3. Deterministic Answer Strategy ---
    # To keep this strictly deterministic and farmer-safe without an expensive LLM,
    # we construct a rule-based summary using the explicit language request.
    
    if latest:
        temp = latest['ambient'] or latest['probe_1']
        is_warm = temp and temp > 30.0
        
        if language == "hi-IN":
            if is_warm:
                text_response = f"बेड गर्म है। तापमान {temp} डिग्री है। कृपया नमी की जांच करें।"
            else:
                text_response = f"बेड सामान्य है। तापमान {temp} डिग्री है।"
        elif language == "gu-IN":
            if is_warm:
                text_response = f"બેડ ગરમ છે. તાપમાન {temp} ડિગ્રી છે. કૃપા કરીને ભેજ તપાસો."
            else:
                text_response = f"બેડ સામાન્ય છે. તાપમાન {temp} ડિગ્રી છે."
        else: # en-IN
            if is_warm:
                text_response = f"The bed is warmer than usual at {temp} degrees. Check moisture."
            else:
                text_response = f"The bed is normal. Temperature is {temp} degrees."
    else:
        text_response = "I have no recent data for this bed." if language == "en-IN" else "मेरे पास इस बेड का कोई नया डेटा नहीं है।"

    # --- 4. TTS Synthesis ---
    try:
        tts = get_tts_provider()
        audio_bytes = tts.synthesize(text_response, language)
    except Exception as e:
        print(f"[!] TTS Error: {e}")
        # Return a fallback empty WAV file if offline testing so UI doesn't crash
        import wave
        with io.BytesIO() as wav_io:
            with wave.open(wav_io, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)
                wav_file.writeframes(b'')
            audio_bytes = wav_io.getvalue()
            
    return Response(content=audio_bytes, media_type="audio/wav")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv('VK_API_HOST', '0.0.0.0')
    port = int(os.getenv('VK_API_PORT', '8000'))
    uvicorn.run(app, host=host, port=port)
