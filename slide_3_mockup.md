# Slide 3: Technical Approach & System Architecture (Master Edition)

This is the final, high-definition (2560x1440, 16:9) ready-to-upload slide image for **Slide 3**.

It completely eliminates generic AI slop and strictly incorporates your two real engineering diagrams, the official **Vermikendra** header branding, a dedicated Tech Stack column with badged frameworks, a live scannable GitHub QR code, and a pictorial matrix detailing the extent of AI tools usage vs teammate engineering.

![Slide 3 Master](C:\Users\25beevdt047\.gemini\antigravity-ide\brain\fc062c57-190e-4ee8-816f-4efd1e49c6b8\slide_3_technical_approach_master.jpg)

---

## Detailed Slide Breakdown & Technical Depth

### 1. Bin Instrumentation & Physical Nodes (Left Column)
- **Isometric Cutaway CAD Diagram**: Directly embeds the engineered CAD rendering ([`academic_isometric_bin_1789388647042.jpg`](file:///C:/Users/25beevdt047/.gemini/antigravity-ide/brain/fc062c57-190e-4ee8-816f-4efd1e49c6b8/academic_isometric_bin_1789388647042.jpg)) displaying sensor probe depths, lid pod, and bottom tare platform.
- **5-Point Depth Array**: 5x DS18B20 1-Wire temperature sensors positioned at 5 cm (core), 15 cm (center & sun-facing wall), and 25 cm (deep layer) to detect thermal inversion layers before worms perish.
- **Respiration Lid Pod**: Sensirion SCD41 Photoacoustic NDIR CO2 sensor + Bosch BME688 (VOC/RH/pressure) + Adafruit LIS3DH 3-axis accelerometer for lid motion interrupts + 40 mm 5V fan for 120s headspace flush cycles.
- **Weighing Platform**: 4x 50 kg shear-beam load cells in a Wheatstone bridge with an HX711 24-bit ADC (resolution $\pm 200\text{ g}$) to automatically detect feeding ($+kg$) and harvesting ($-kg$) without paper registers.
- **Solar Power Budget**: 6V/2W monocrystalline solar panel coupled with a TP4056 / CN3065 charger and a 3.7V 3000 mAh 18650 Li-ion cell. Quiescent sleep current is only **18 µA**, while LoRa transmission draws **120 mA** @ 14 dBm. Provides **>7 days of continuous zero-sunlight autonomy**.

### 2. Architectural Signal Flow, Circuit Schematics & Algorithms (Center Column)
- **Complete Schematic & Pipeline**: Embeds your academic architecture schematic ([`vermikendra_academic_diagram_1789388354923.jpg`](file:///C:/Users/25beevdt047/.gemini/antigravity-ide/brain/fc062c57-190e-4ee8-816f-4efd1e49c6b8/vermikendra_academic_diagram_1789388354923.jpg)) mapping the hardware circuit, power flow, and gateway service tree.
- **Edge Failsafe Logic**: RAK4631 (Nordic nRF52840 ARM Cortex-M4F) runs autonomous local rules: if $T \ge 33^\circ\text{C}$ and moisture $< 75\%$, it triggers a 20s solenoid misting pulse even if the gateway is completely offline.
- **LoRa PHY Link**: 865.0625 MHz (India license-exempt band), Spreading Factor SF9, 125 kHz Bandwidth, Coding Rate 4/5. Transmits 44-byte binary frames signed with HMAC-SHA256 for cryptographic authentication.
- **Offline Gateway Ingestion**: Raspberry Pi Compute Module 4 (CM4) with a Waveshare SX1262 LoRa HAT connected via CP2102 serial (`/dev/ttyUSB0`) feeding into a local Mosquitto MQTT message broker and FastAPI ASGI server.
- **Predictive Analytics**: 1D thermal diffusion model ($dT/dt$) forecasts temperature threshold breaches 60 minutes ahead; linear regression slope of closed-lid CO2 accumulation measures respiration rate plateauing for maturity confirmation.

### 3. Technology Stack (Right Column)
- **C++ / PlatformIO**: RAK4631 nRF52840 low-level sensor drivers, power sequencing, and edge failsafe state machine.
- **Python 3.10+**: Asynchronous gateway serial daemon, packet deserializer, and MQTT publication engine.
- **FastAPI & Uvicorn**: Offline ASGI REST endpoints and WebSocket live-telemetry streams.
- **SQLite3 (WAL Mode)**: Lightweight, zero-maintenance local time-series storage with 90-day retention.
- **React / Vite PWA**: Offline-first mobile dashboard localized in Gujarati, Hindi, and English over the gateway WiFi hotspot (192.168.4.1).
- **LoRa P2P (865 MHz)**: Semtech SX1262 long-range RF physical link (license-exempt).
- **Mosquitto MQTT**: Decoupled, event-driven inter-process communication bus.
- **Scikit-Learn & NumPy**: Linear regression slope fitting for CO2 respiration kinetics and thermal risk forecasting.

### 4. Open-Source GitHub Repository & Demo Video (Bottom Left)
- **Live Scannable QR Code**: Linked to [`https://github.com/atharvedahima/vermikendra`](https://github.com/atharvedahima/vermikendra).
- **Open-Source Artifacts**: Contains full firmware source code, gateway systemd configs, React PWA frontend, KiCad schematics, and 3D CAD models.
- **Demo Video**: Direct access via the repository's `/demo` folder or QR scan.

### 5. Extent of Usage of AI Tools vs Teammates Engineering (Bottom Right)
- **30% AI-Assisted Scope**:
  - Presentation formatting and slide layout synthesis
  - Academic visual diagrams and CAD vector artifact rendering
  - Mathematical modeling: 1D thermal diffusion ODEs and CO2 kinetics curve fitting
  - Synthesizing benchmark telemetry for regression tests
- **70% Teammate-Engineered Core Scope**:
  - C++ firmware drivers, power-profiling (18 µA sleep), and hardware watchdog
  - Solar harvesting circuit design, TP4056 integration, and PCB assembly
  - LoRa binary frame specification and HMAC-SHA256 crypto signing
  - Gateway Linux daemon, Mosquitto MQTT broker, and SQLite WAL schema
  - Offline-first React PWA mobile dashboard with multilingual support
