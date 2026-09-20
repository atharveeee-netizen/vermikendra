import os
import json
import asyncio
import requests
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import paho.mqtt.client as mqtt

# Local modules
from db import get_connection
from assistant.context_builder import build_node_context
from assistant.intent_router import route_intent
from assistant.llm_provider import get_llm_provider
from assistant.tts_provider import get_tts_provider

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(title="Vermikendra API")

# Phase 49: Restrict CORS
ALLOWED_ORIGINS = os.getenv('VK_CORS_ORIGINS', 'http://localhost:3000').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

MQTT_BROKER = os.getenv('VK_MQTT_BROKER', '127.0.0.1')
MQTT_PORT = int(os.getenv('VK_MQTT_PORT', '1883'))
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', '')

# ---------------------------------------------------------
# ERROR HANDLING (Phase 48)
# ---------------------------------------------------------
class StandardApiError(Exception):
    def __init__(self, code: str, message: str, retryable: bool, status_code: int = 400):
        self.code = code
        self.message = message
        self.retryable = retryable
        self.status_code = status_code

@app.exception_handler(StandardApiError)
async def standard_error_handler(request, exc: StandardApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "retryable": exc.retryable
            }
        }
    )

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

def on_mqtt_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        # Phase 12: We should validate payload and emit typed telemetry event
        # For now we broadcast the JSON
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        asyncio.run_coroutine_threadsafe(manager.broadcast(payload), loop)
    except Exception as e:
        print(f"[!] MQTT->WS Bridge Error: {e}")

mqttc = mqtt.Client()
mqttc.on_message = on_mqtt_message

@app.on_event("startup")
async def startup_event():
    try:
        mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqttc.subscribe("vk/+/+/up")
        mqttc.loop_start()
    except Exception as e:
        print(f"[!] Could not start API MQTT listener: {e}")

@app.on_event("shutdown")
def shutdown_event():
    mqttc.loop_stop()

# ---------------------------------------------------------
# DISCOVERY API (Phase 3 & 9)
# ---------------------------------------------------------
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/sites")
def get_sites():
    conn = get_connection()
    cur = conn.execute("SELECT * FROM sites")
    sites = [dict(row) for row in cur.fetchall()]
    conn.close()
    return sites

@app.get("/api/sites/{site_id}/bins")
def get_bins(site_id: str):
    conn = get_connection()
    cur = conn.execute("SELECT * FROM bins WHERE site_id = ?", (site_id,))
    bins = [dict(row) for row in cur.fetchall()]
    conn.close()
    return bins

@app.get("/api/bins/{bin_id}/nodes")
def get_nodes(bin_id: str):
    conn = get_connection()
    cur = conn.execute("SELECT * FROM nodes WHERE bin_id = ?", (bin_id,))
    nodes = [dict(row) for row in cur.fetchall()]
    conn.close()
    return nodes

@app.get("/api/nodes/{node_id}/telemetry/latest")
def get_latest_telemetry(node_id: int):
    conn = get_connection()
    context = build_node_context(conn, node_id)
    conn.close()
    
    if not context:
        raise StandardApiError("NO_TELEMETRY", "No telemetry found for node", retryable=False, status_code=404)
        
    # Phase 6: Server-side Status computation
    temp = context.get('ambient_c') or context.get('probe_1')
    faults = context.get('faults', 0)
    
    status = "NORMAL"
    reason = ""
    
    if faults > 0:
        status = "SENSOR_FAULT"
        reason = "Hardware sensor fault detected."
    elif temp and temp > 32.0:
        status = "ACTION_NEEDED"
        reason = "Temperature exceeds normal operating threshold."
    elif temp and temp > 30.0:
        status = "WATCH"
        reason = "Temperature is elevated."
        
    context['computed_status'] = status
    context['computed_reason'] = reason
    
    return context

@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ---------------------------------------------------------
# VOICE ASSISTANT PIPELINE (Phase 23)
# ---------------------------------------------------------
@app.post("/api/assistant/voice")
async def process_voice_query(
    audio: UploadFile = File(...),
    language: str = Form(...),
    node_id: int = Form(...)
):
    # Phase 52: Audio Limits
    audio_bytes = await audio.read()
    if len(audio_bytes) > 5 * 1024 * 1024:
        raise StandardApiError("AUDIO_TOO_LARGE", "Audio exceeds 5MB limit", retryable=False)
        
    # 1. STT (Phase 24 & 26)
    if not SARVAM_API_KEY:
        raise StandardApiError("STT_NOT_CONFIGURED", "Sarvam API Key missing", retryable=False, status_code=503)
        
    url = "https://api.sarvam.ai/speech-to-text"
    headers = {"api-subscription-key": SARVAM_API_KEY}
    files = {'file': ('question.webm', audio_bytes, 'audio/webm')}
    data = {'language_code': language}
    
    try:
        r = requests.post(url, headers=headers, files=files, data=data, timeout=15)
        if r.status_code != 200:
            raise StandardApiError("STT_FAILED", "Transcription failed from provider", retryable=True, status_code=502)
        transcription = r.json().get('transcript', '')
    except Exception:
        raise StandardApiError("STT_UNAVAILABLE", "Failed to reach STT provider", retryable=True, status_code=503)

    if not transcription.strip():
        raise StandardApiError("EMPTY_AUDIO", "Could not hear any speech", retryable=True)

    # 2. Context & Intent (Phase 27 & 28)
    conn = get_connection()
    context = build_node_context(conn, node_id)
    conn.close()
    
    intent = route_intent(transcription, language)
    
    # 3. LLM/Answer Gen (Phase 29 & 30)
    llm = get_llm_provider()
    answer_text = llm.generate_answer(intent, context, language)
    
    # 4. TTS (Phase 32)
    tts_audio_b64 = None
    tts_status = "ok"
    try:
        tts = get_tts_provider()
        raw_audio = tts.synthesize(answer_text, language)
        import base64
        tts_audio_b64 = base64.b64encode(raw_audio).decode('utf-8')
    except Exception as e:
        print(f"[!] TTS Error: {e}")
        tts_status = "unavailable"

    # Phase 23: Return structured JSON contract
    return JSONResponse(content={
        "language": language,
        "transcript": transcription,
        "intent": intent,
        "answer_text": answer_text,
        "audio_status": tts_status,
        "audio_base64": tts_audio_b64,
        "status": "success"
    })

if __name__ == "__main__":
    import uvicorn
    host = os.getenv('VK_API_HOST', '0.0.0.0')
    port = int(os.getenv('VK_API_PORT', '8000'))
    uvicorn.run(app, host=host, port=port)
