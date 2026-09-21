# Reference Implementation Matrix

| Reference Pattern | Vermikendra Component | Route | Data Source | Implementation | Validation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Fleet List** (Panel 1) | Multi-Bed List View | `/` | `GET /api/bins`, `GET /api/nodes` | IMPLEMENTED | VALIDATED |
| **Satellite Map** (Panel 2) | Map View | `/map` | Node GPS (Logical fallback) | IMPLEMENTED | VALIDATED |
| **Deep Telemetry** (Panel 3) | Detail Dashboard | `/bed/[id]` | `GET /api/telemetry/latest` | IMPLEMENTED | VALIDATED |
| **Bottom Navigation** | `BottomNav` | All | Static Route Map | IMPLEMENTED | VALIDATED |
| **Status Badges** | `status-normal` CSS | `/bed/[id]` | `computed_status` | IMPLEMENTED | VALIDATED |
| **Voice Interaction** | Assistant Button | `/bed/[id]` | `POST /api/assistant/voice` | IMPLEMENTED | VALIDATED |

## Deviations / Missing Data
- **Real GPS Coordinates**: The current Vermikendra backend does not provide exact lat/lon for nodes. The map implementation uses a stylized logical zone representation until real geospatial data is exposed by the gateway. This is documented and prevents fabricating fake GPS data.
