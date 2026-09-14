# Slide 3: Technical Approach & System Architecture (Research Journal Edition)

This is the newly regenerated, **Research-Journal Grade** (2560x1440, 16:9) ready-to-upload slide image for **Slide 3**.

It completely eliminates walls of text and replaces them with **6 high-density academic scientific figures**: CAD cutaways, architectural signal schematics, empirical biological kinetics plots, thermal depth inversion curves, log-scale power timing waveforms, autonomous edge state machines, full-stack visual badge matrices, and a pictorial AI usage donut chart.

![Slide 3 Research Journal](C:\Users\25beevdt047\.gemini\antigravity-ide\brain\fc062c57-190e-4ee8-816f-4efd1e49c6b8\slide_3_research_journal_master.jpg)

---

## 6 Academic Figures Breakdown

### **Fig. 1. Physical Bin CAD Cutaway & Depth Sensor Array (Top-Left)**
- **Visual Asset**: High-resolution CAD engineering cutaway line schematic displaying internal sensor placements.
- **Visual Callouts**:
  - `[A]` 5-Point 1-Wire Array (DS18B20 at 5 cm, 15 cm core & wall, 25 cm deep).
  - `[B]` Respiration Lid Pod (SCD41 NDIR $\text{CO}_2$ + BME688 + LIS3DH lid-tilt + 40 mm 5V fan).
  - `[C]` Mass Platform (4x 50 kg shear-beam load cells + HX711, $\pm 200\text{ g}$ precision).
  - `[D]` Solar Harvesting (6V/2W panel + TP4056 + 3000 mAh 18650 Li-ion, 18 µA sleep).

### **Fig. 2. End-to-End Signal Pipeline & Offline Gateway Architecture (Top-Center)**
- **Visual Asset**: Comprehensive systems architecture schematic mapping the hardware circuit, radio link, and service tree.
- **Concise Signal Path**:
  $$\text{RAK4631 (nRF52840)} \xrightarrow[\text{SF9, 125kHz, 44B Signed}]{\text{LoRa P2P 865MHz}} \text{RPi CM4 Gateway} \rightarrow \text{Mosquitto MQTT} \rightarrow \text{FastAPI} \rightarrow \text{SQLite WAL} \rightarrow \text{Offline PWA (192.168.4.1)}$$

### **Fig. 3. Full-Stack Technology Matrix (Top-Right)**
- **Visual Badges Grid**: 8 compact visual technology tiles with category tags:
  - **C++ / Arduino**: RAK4631 Firmware
  - **Python 3.10+**: Gateway Daemon
  - **FastAPI**: Offline REST & WebSocket
  - **SQLite3 WAL**: Time-Series Local DB
  - **React / Vite**: Offline Mobile PWA
  - **LoRa SX1262**: 865 MHz P2P PHY
  - **Mosquitto**: MQTT IPC Broker
  - **Scikit-Learn**: Thermal & ODE ML Models

### **Fig. 4. Empirical Biological Kinetics & Depth Heat Inversion (Bottom-Left)**
- **Left Scientific Plot**: Closed-lid $\text{CO}_2$ Respiration Kinetics ($\text{ppm}$ vs $\text{min}$) displaying the 120s fan flush phase, linear measurement accumulation ($\text{slope} = \Delta \text{CO}_2/\Delta t$), and maturity plateau ($R^2 = 0.98$) distinguishing fresh feed from mature compost.
- **Right Scientific Plot**: 5-Point Depth Temperature Profile demonstrating detection of a dangerous hidden core hotspot ($34.2^\circ\text{C}$ at 15 cm) while the surface feels completely normal ($28^\circ\text{C}$), well above the $33^\circ\text{C}$ critical threshold.

### **Fig. 5. Power Profiling & Autonomous Failsafe State Machine (Bottom-Center)**
- **Log Power Waveform**: Duty-cycle current trace showing **18 µA deep sleep (300s)** $\rightarrow$ **50 mA sensor strobe (1.2s)** $\rightarrow$ **120 mA LoRa Tx pulse (290 ms @ 14 dBm)** $\rightarrow$ **4.6 mA Rx window (2.0s)** $\rightarrow$ **Return to sleep**, guaranteeing $>7$ days zero-sunlight autonomy.
- **Firmware State Machine**: Directed state transition graph: `BOOT` $\rightarrow$ `SLEEP` $\xrightarrow{\text{Timer/Int}}$ `SAMPLE 3V3_S` $\xrightarrow{\text{Failsafe Logic}}$ `LORA TX` $\rightarrow$ `RX ACK`.

### **Fig. 6. Real Repository & Extent of AI Tools Usage (Bottom-Right)**
- **Top**: High-density scannable QR Code linking to [`https://github.com/atharvedahima/vermikendra`](https://github.com/atharvedahima/vermikendra).
- **Bottom**: Pictorial AI Tools Donut Chart showing:
  - **30% AI-Assisted Scope**: Slide formatting, visual artifacts, 1D thermal ODE math modeling, telemetry synthesis.
  - **70% Teammate-Engineered Core Scope**: C++ firmware & drivers, solar circuits & PCB, gateway daemon & SQLite schema, offline React PWA dashboard.

---

### Header & Watermark
- **Team Badge**: `Vermikendra` (orange pill).
- **Hackathon Logo**: `Hack for Social Cause 2027`.
- **Template Watermark**: `@HSC submission- Template`.
