# Slide 5: Team Composition, Roles & Journey (Master Edition)

This is the final, high-definition (2560x1440, 16:9) ready-to-upload slide image for **Slide 5: Team**.

It cleanly divides all engineering tasks across the three team members (**Atharve Dahima [ECE]**, **Akshit Agarwal [CSE]**, and **Charvi Meddita [CSE]**), while utilizing the entire presentation canvas to highlight the key technical challenges solved and the team's journey from village discovery to national deployment.

![Slide 5 Master](C:\Users\25beevdt047\.gemini\antigravity-ide\brain\fc062c57-190e-4ee8-816f-4efd1e49c6b8\slide_5_team_master.jpg)

---

## Detailed Team Task Division & Responsibilities

### 1. Header & Institutional Alignment
- **Top-Left**: Official team badge **`Vermikendra`** in an orange pill.
- **Center**: Title **"Team Vermikendra & Engineering Leadership"** with subtitle honoring Rashtriya Raksha University (RRU), Gujarat, and Team ID `HSC|GJ|00009`.
- **Top-Right**: Official **`Hack for Social Cause 2027`** emblem.

### 2. Team Member Profile Cards & Explicit Task Division (Top Half)

#### **Atharve Dahima** | Electronics & Communication Engineering (ECE)
- **Role**: Hardware, Embedded Firmware & Power Systems Lead (`ECE LEAD`)
- **Key Deliverables & Responsibilities**:
  - **Embedded Node Firmware**: Authored C++ firmware on RAK4631 (Nordic nRF52840 ARM Cortex-M4F) utilizing PlatformIO and FreeRTOS; built custom 1-Wire and I2C peripheral drivers.
  - **Sensor Suite Integration**: Integrated and calibrated the 5-point DS18B20 depth temperature probe array, Sensirion SCD41 photoacoustic $\text{CO}_2$ sensor, Bosch BME688, and 4x shear-beam load cells with HX711.
  - **Ultra-Low-Power Profiling**: Designed power-rail sequencing with a low-quiescent LDO and switched `3V3_S` sensor bus, achieving an ultralow **18 µA deep-sleep current**.
  - **Solar Energy Harvesting**: Calculated complete battery energy budget; integrated 6V/2W solar panel, TP4056 charge controller, and 3000 mAh 18650 Li-ion cell providing **>7 days zero-sun autonomy**.
  - **Mechanical Enclosure & Prototyping**: Designed the IP65 junction box housing, ePTFE hydrophobic breathable membrane, PG7 cable glands, and lid-pod airflow channel.
- **Technologies Owned**: C++ | PlatformIO | nRF52840 | LoRa SX1262 | 1-Wire | KiCad

#### **Akshit Agarwal** | Computer Science & Engineering (CSE)
- **Role**: Gateway Architecture, Backend & ML Analytics Lead (`CSE BACKEND & ML`)
- **Key Deliverables & Responsibilities**:
  - **Raspberry Pi CM4 Architecture**: Configured headless Linux systemd daemons, Waveshare SX1262 LoRa HAT UART interface (`/dev/ttyUSB0`), and hardware watchdog timer.
  - **High-Performance IPC Ingestion**: Architected decoupled internal message pipeline using Mosquitto MQTT; built asynchronous Python serial packet deserializer.
  - **Offline REST & WebSocket Server**: Developed asynchronous FastAPI and Uvicorn server pushing live sensor telemetry and alerts to local clients.
  - **Time-Series Persistence**: Designed SQLite3 database with Write-Ahead Logging (WAL) and automated 90-day time-series retention and downsampling schema.
  - **Predictive Analytics Engine**: Implemented 1D thermal diffusion ($dT/dt$) risk forecasting to predict heat breaches 60 min ahead, and linear regression slope estimation for $\text{CO}_2$ respiration kinetics.
- **Technologies Owned**: Python 3.10 | FastAPI | SQLite3 WAL | Mosquitto MQTT | Scikit-Learn | Linux

#### **Charvi Meddita** | Computer Science & Engineering (CSE)
- **Role**: Frontend PWA, Multi-lingual UX & Product Strategy Lead (`CSE FRONTEND & PRODUCT`)
- **Key Deliverables & Responsibilities**:
  - **Offline-First PWA Dashboard**: Engineered responsive Progressive Web App in React 18, Vite, and Tailwind CSS served entirely from the standalone CM4 WiFi hotspot (`192.168.4.1`).
  - **Low-Literacy Universal UX**: Designed high-visibility visual status hierarchy (Green/Amber/Red), intuitive icons, and single-tap action cards tailored for rural operators.
  - **Multilingual Localization (i18n)**: Implemented complete regional localization in Gujarati, Hindi, and English with voice-guided alert audio prompts.
  - **Traceable Batch Records**: Built automated batch history ledger and scannable QR verification certificates for commercial compost and vermiwash buyers.
  - **Field Research & User Flows**: Mapped operator journeys (J1–J5); conducted usability evaluations with non-technical village composting stakeholders.
- **Technologies Owned**: React 18 | Vite | Tailwind CSS | PWA | Chart.js | i18n Localization

---

### 3. Engineering Challenges Overcome (Bottom-Left)
1. **Off-Grid Power Budget & Monsoon Autonomy (Hardware / ECE)**:
   - *Problem*: Continuous sampling drew $>120\text{ mA}$, depleting batteries within 24 hours under monsoon cloud cover.
   - *Solution*: Engineered sleep duty-cycling (18 µA deep sleep) via low-quiescent LDO, switched `3V3_S` rails, and optimized LoRa SF9 transmit bursts, securing $>7$ days zero-sun autonomy.
2. **Complete Internet Independence & Offline Hotspot (Backend / CSE)**:
   - *Problem*: Rural cellular 4G connectivity suffered constant dropouts, freezing cloud-dependent dashboards.
   - *Solution*: Pivoted to a 100% offline-first architecture on the Raspberry Pi CM4. Hosts its own local WiFi hotspot (`192.168.4.1`) running FastAPI, SQLite, and the PWA with zero cloud dependency.
3. **Biological Respiration vs. Ambient Noise (AI & UX / CSE)**:
   - *Problem*: Diurnal ambient temperature and wind drafts caused erratic raw $\text{CO}_2$ spikes inside the compost headspace.
   - *Solution*: Designed an active lid pod with a 40 mm flush fan executing a 120s pre-flush followed by a 600s sealed chamber build-up. Scikit-learn linear regression calculates slope (ppm/min) with $R^2 > 0.95$ quality gating.

---

### 4. Our Engineering Journey & Vision for Bharat (Bottom-Right)
- **Phase 1: Problem Discovery & Ground Reality (Aug 2026)**: Visited rural vermiculture beds in Gujarat. Witnessed women SHGs abandon units after silent heat waves wiped out entire earthworm populations. Identified critical need for multi-depth thermal telemetry.
- **Phase 2: Hardware-Software Co-Design at RRU Labs (Sep 2026)**: Combined ECE circuit engineering with CSE systems architecture at Rashtriya Raksha University. Sourced sensors, built WisBlock LoRa prototype, 3D printed lid pods, and coded the offline gateway daemon.
- **Phase 3: Live Real-Bin Validation & Stress Testing (Late Sep 2026)**: Instrumented a live pilot bin with live *Eisenia fetida* worms. Successfully validated autonomous misting during $33^\circ\text{C}$ heat spikes, verified respiration plateau against manual maturity, and refined Gujarati UI.
- **Phase 4: Scaling Vision & National Field Deployment (Oct 2026 - 2027)**: Partnering with local Krishi Vigyan Kendras (KVK) and DAY-NRLM cluster federations to deploy 20-bin village clusters under GOBARdhan and Swachh Bharat Phase II, scaling Lakhpati Didi enterprises.

---

### 5. Institutional Affiliation & Watermark
- **Institutional Banner**: `Rashtriya Raksha University, Gujarat | School of Applied Sciences, Technology & National Security | Mentorship: KVK & Agriculture Extension Experts`
- **Template Watermark**: `@HSC submission- Template`
