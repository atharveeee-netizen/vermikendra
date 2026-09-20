# Vermikendra (Production Truth)

A scientific vermicompost telemetry and agricultural monitoring system designed explicitly for zero-literacy usability, off-grid resilience, and deterministic ground-truth sensing.

## The Principle

*   **No "AI Slop":** The system never attempts to sound "smart". It delivers binary state data (e.g., "The bed is too hot") using deterministic rule engines.
*   **Zero UI Density:** The farmer sees *only* the state of the active bed, with large typography, bold colors, and an ambient voice interface. No graphs, no dashboards, no complex menus.
*   **Hardware Ground-Truth:** The frontend is completely stateless and dumb. It only renders exactly what the SQLite database proves was received from a physical LoRaWAN/Serial node.

## Architecture

*   **Firmware:** C++ based bare-metal edge nodes (RAK4631/nRF52) producing highly compact 44-byte binary packets to save battery and bandwidth.
*   **Gateway Ingestion (`vk_ingest.py`):** Unpacks binary frames, applies fault masking, writes to SQLite WAL, and emits typed events over MQTT.
*   **API Gateway (`api.py`):** FastAPI app providing Discovery (Sites, Bins, Nodes), a Status Calculation engine, standard JSON APIs, and a WebSocket bridge.
*   **Voice Assistant Engine:** 
    *   *STT:* Sarvam API (Hindi, Gujarati, English).
    *   *Context:* SQLite DB state retrieval.
    *   *LLM:* Deterministic rule-based template generation (fallback LLM).
    *   *TTS:* Sarvam Bulbul API / HuggingFace local fallback.
*   **Frontend (`dashboard/`):** Next.js 14 React app configured as a Progressive Web App (PWA). Employs strict TypeScript definitions for API contracts, exponential backoff for WebSockets, and a robust offline/fault display mode.

## Local Setup

1. Run the Gateway:
   ```bash
   cd gateway
   pip install -r requirements.txt
   python db.py          # Bootstraps the DB with seed data
   python api.py         # Starts FastAPI on port 8000
   ```
2. Run the Dashboard:
   ```bash
   cd dashboard
   npm install
   npm run dev           # Starts Next.js on port 3000
   ```
3. Run the Simulator (to emit fake telemetry):
   ```bash
   python simulator/node_sim.py
   ```
