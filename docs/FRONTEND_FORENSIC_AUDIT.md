# FRONTEND FORENSIC AUDIT

## Hardcoded Entities
*   **Node ID:** `const [nodeId, setNodeId] = useState(101);` in `page.tsx:11`.
*   **Bed Label:** `<h2>BED 01</h2>` in `page.tsx:150`.
*   **Farmer Identity:** `<p>नमस्ते, रामभाई</p>` in `page.tsx:132`.

## Fake Telemetry & Status
*   **Moisture:** `<p className="text-2xl font-bold">Stable</p>` in `page.tsx:171`. No actual moisture value or threshold evaluation exists.
*   **Activity:** Displayed as generic raw `co2_ppm`, assuming "activity" maps 1:1 to CO2 ppm without scientific basis for the label.
*   **Readiness:** `const isReady = false; // Deterministic calculation is unverified, default false` in `page.tsx:119`. Not used or displayed accurately.

## Connection & Path Vulnerabilities
*   **API URLs:** Hardcoded `http://localhost:8000/api/...` in `page.tsx:22` and `93`. Breaks when deployed on cloud/mobile.
*   **WebSocket URLs:** Hardcoded `ws://localhost:8000/ws/telemetry` in `page.tsx:31`. Breaks on remote access.
*   **PWA Cache:** `next-pwa` is configured in `next.config.ts`, but service workers, manifest completeness, and actual offline navigation fallback are unverified.

## Architecture
*   **Monolithic Structure:** The entire application (Voice state machine, WebSocket handling, UI layout, telemetry state) is dumped into `page.tsx`. There is no separation of concerns (Features vs Components vs Services).
*   **Untyped Contracts:** Extensive use of `any` for telemetry data (`useState<any>(null)`).

## Verdict
The frontend is currently a visually compliant **UX Prototype**. It relies on hardcoded local paths, static user identities, and lacks error-resilient data parsing. It must be refactored into a scalable, typed, API-driven architecture.
