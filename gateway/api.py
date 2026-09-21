import os
import json
import asyncio
import requests
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Local modules
from db import get_connection
from assistant.context_builder import build_node_context
from assistant.intent_router import route_intent
from assistant.llm_provider import get_llm_provider
from assistant.tts_provider import get_tts_provider
from core.ingestion import ingest_telemetry_payload, calculate_status, DuplicateTelemetryError, ValidationError

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

SARVAM_API_KEY = os.getenv('SARVAM_API_KEY')

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

class TelemetryPayload(BaseModel):
    node: int
    seq: int
    probes_c: List[float | None] = []
    ambient_c: float | None = None
    rh_pct: float | None = None
    co2_ppm: int | None = None
    mass_g: float | None = None
    rssi: int | None = None
    faults: int = 0
    ts: str | None = None

@app.post("/api/internal/telemetry")
async def ingest_telemetry(payload: TelemetryPayload):
    try:
        canonical_event = ingest_telemetry_payload(payload.dict())
        # Phase 3 & 4: Only broadcast if DB insertion succeeds
        await manager.broadcast(json.dumps(canonical_event))
        return {"status": "broadcasted"}
    except DuplicateTelemetryError as e:
        return JSONResponse(status_code=409, content={"status": "duplicate", "message": str(e)})
    except ValidationError as e:
        raise StandardApiError("INVALID_TELEMETRY", str(e), retryable=False, status_code=400)
    except Exception as e:
        raise StandardApiError("INTERNAL_ERROR", str(e), retryable=True, status_code=500)

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

@app.get("/api/fields")
def get_fields():
    conn = get_connection()
    cur = conn.execute("SELECT * FROM fields")
    fields = [dict(row) for row in cur.fetchall()]
    conn.close()
    return fields

@app.get("/api/fields/{field_id}/bins")
def get_field_bins(field_id: str):
    conn = get_connection()
    cur = conn.execute("SELECT * FROM bins WHERE field_id = ?", (field_id,))
    bins = [dict(row) for row in cur.fetchall()]
    conn.close()
    return bins

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

@app.get("/api/sites/{site_id}/fleet")
def get_site_fleet(site_id: str):
    conn = get_connection()
    query = """
        SELECT n.id as node_id, n.bin_id, n.mac_address, n.last_seen,
               b.field_id, b.name as bin_name
        FROM nodes n
        JOIN bins b ON n.bin_id = b.id
        WHERE b.site_id = ?
    """
    cur = conn.execute(query, (site_id,))
    nodes = [dict(row) for row in cur.fetchall()]

    fleet = []
    stats = {"total": len(nodes), "online": 0, "offline": 0, "normal": 0, "attention": 0, "critical": 0}

    for n in nodes:
        ctx = build_node_context(conn, n['node_id'])
        
        if not ctx:
            n['latest_telemetry'] = None
            n['computed_status'] = 'OFFLINE'
            n['computed_reason'] = 'No telemetry data'
            stats['offline'] += 1
            fleet.append(n)
            continue
            
        probes_c = [
            ctx.get('probe_1'), ctx.get('probe_2'), ctx.get('probe_3'),
            ctx.get('probe_4'), ctx.get('probe_5')
        ]
        status, reason = calculate_status({"faults": ctx.get('faults', 0), "probes_c": probes_c})
        
        ctx['computed_status'] = status
        ctx['computed_reason'] = reason
        n['latest_telemetry'] = ctx
        n['computed_status'] = status
        n['computed_reason'] = reason
        
        stats['online'] += 1
        if status == 'ACTION_NEEDED' or status == 'SENSOR_FAULT':
            stats['critical'] += 1
        elif status == 'WATCH':
            stats['attention'] += 1
        else:
            stats['normal'] += 1
        
        fleet.append(n)
        
    conn.close()
    return {"nodes": fleet, "stats": stats}

@app.get("/api/nodes/{node_id}/telemetry/latest")
def get_latest_telemetry(node_id: int):
    conn = get_connection()
    context = build_node_context(conn, node_id)
    
    # Get node and bin info
    cur = conn.execute("""
        SELECT n.mac_address, n.fw_version, n.last_seen, b.name as bin_name, b.field_id
        FROM nodes n
        JOIN bins b ON n.bin_id = b.id
        WHERE n.id = ?
    """, (node_id,))
    node_info = cur.fetchone()
    
    conn.close()
    
    if not context:
        raise StandardApiError("NO_TELEMETRY", "No telemetry found for node", retryable=False, status_code=404)
        
    # Phase 6 & 10: Server-side Status computation via canonical function
    probes_c = [
        context.get('probe_1'),
        context.get('probe_2'),
        context.get('probe_3'),
        context.get('probe_4'),
        context.get('probe_5')
    ]
    context_for_status = {
        "faults": context.get('faults', 0),
        "probes_c": probes_c
    }
    status, reason = calculate_status(context_for_status)
        
    context['computed_status'] = status
    context['computed_reason'] = reason
    
    if node_info:
        context['mac_address'] = node_info['mac_address']
        context['fw_version'] = node_info['fw_version']
        context['bin_name'] = node_info['bin_name']
        context['field_id'] = node_info['field_id']
    
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
    except Exception:
        raise StandardApiError("STT_UNAVAILABLE", "Failed to reach STT provider", retryable=True, status_code=503)

    if r.status_code != 200:
        raise StandardApiError("STT_FAILED", f"Transcription failed: {r.text}", retryable=True, status_code=502)
        
    transcription = r.json().get('transcript', '')

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
