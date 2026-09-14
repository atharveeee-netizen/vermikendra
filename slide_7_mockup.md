# Slide 7: References & Scientific Citations (Master Edition)

This is the final, high-definition (2560x1440, 16:9) ready-to-upload slide image for **Slide 7: References**.

It strictly documents all primary academic research literature, industrial sensor datasheets, national government policy frameworks, and open-source verification links with zero empty space.

![Slide 7 Master](C:\Users\25beevdt047\.gemini\antigravity-ide\brain\fc062c57-190e-4ee8-816f-4efd1e49c6b8\slide_7_references_master.jpg)

---

## Detailed References Breakdown

### 1. Peer-Reviewed Academic Research & Respiration Standards (Top-Left)
- **[1] TMECC 05.08-B / US Composting Council**: *Carbon Dioxide Evolution Rate Test for Compost Maturity & Biological Stability*. Basis for Vermikendra's closed-lid respiration measurement cycle (120s fan flush + 600s chamber slope calculation).
- **[2] Edwards, C.A., & Arancon, N.Q. (2004)**: *Vermicomposting: Recycling Organic Wastes for Agriculture and the Environment*. CRC Press. Identified lethal thermal inversion layers ($>33^\circ\text{C}$ to $35^\circ\text{C}$) killing *Eisenia fetida*; established optimal 60–80% bed moisture.
- **[3] Dominguez, J., & Edwards, C.A. (2011)**: *Biology and Ecology of Earthworm Species Used for Vermicomposting*. Biology of Earthworms, 27–40. Theoretical foundation for 5-point depth array sensor placement (P1–P5) to preempt hidden core overheating.
- **[4] Vassis, D., et al. (IEEE IoT-J, 2020)**: *Long-Range Low-Power IoT Architectures for Precision Agriculture & Organic Waste Management*. Architectural reference for license-exempt LoRa P2P telemetry, SF9 125kHz modulation, and 18 µA deep sleep duty-cycling.

### 2. Hardware Datasheets, RF Specifications & Compliance Standards (Top-Right)
- **[5] Semtech SX1261/SX1262 Transceiver Datasheet (Rev 2.1)**: *Long-Range Low-Power Sub-GHz Transceiver* (Semtech Corp., 2020). Radio parameters: 865.0625 MHz (India license-exempt band, GSR 564(E)), SF9, BW 125kHz, CR 4/5, +14 dBm Tx power.
- **[6] Sensirion SCD41 Photoacoustic NDIR $\text{CO}_2$ Sensor Manual**: *Miniature $\text{CO}_2$, Temperature & Humidity Sensor* (Sensirion AG, 2021). Photoacoustic NDIR principle; 400–5000 ppm range, $\pm 40\text{ ppm}$ accuracy; forced outdoor 420ppm recalibration protocol.
- **[7] Nordic Semiconductor nRF52840 Product Specification**: *Multiprotocol Bluetooth 5.3 & 2.4 GHz SoC with 64 MHz ARM Cortex-M4F*. Ultra-low power profiling: 18 µA system deep sleep with RTC wake and LIS3DH accelerometer interrupt.
- **[8] Raspberry Pi Compute Module 4 (CM4) Technical Documentation**: *Quad-core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5GHz with onboard WiFi AP*. Headless standalone Linux gateway: hosts Mosquitto MQTT broker, SQLite WAL time-series DB, and offline React PWA.

### 3. Government Guidelines, National Missions & Scheme Alignments (Bottom-Left)
- **[A] Swachh Bharat Mission (Grameen) Phase-II (Ministry of Jal Shakti)**: *Operational Guidelines for Solid and Liquid Waste Management in Rural Areas*. Direct fit: Vermikendra converts rural organic waste into weighed, certified organic compost with digital audit trails.
- **[B] GOBARdhan Scheme (Department of Drinking Water & Sanitation)**: *Galvanizing Organic Bio-Agro Resources Dhan* (Ministry of Jal Shakti, 2023). Direct fit: Utilizes cattle dung as a core vermiculture feedstock, converting environmental liability into monetized rural wealth.
- **[C] DAY-NRLM Lakhpati Didi Initiative (Ministry of Rural Development)**: *Strategy for Promoting Sustainable Livelihood Enterprises for Women SHG Members*. Direct fit: Equips rural women SHG operators with automated alerts to earn ₹45,000+ net profit/year from certified organic inputs.
- **[D] PM-PRANAM (Ministry of Chemicals and Fertilizers, 2023)**: *Programme for Restoration, Awareness, Nourishment and Amelioration of Mother Earth*. Direct fit: Incentivizes states and farmers to reduce synthetic chemical urea/DAP by substituting verified microbial vermicompost.

### 4. Open-Source Implementation, Live Demo & Verification (Bottom-Right)
- **Scannable GitHub QR Code**: Direct link to [`https://github.com/atharvedahima/vermikendra`](https://github.com/atharvedahima/vermikendra).
- **Public Artifacts**: Complete C++ firmware for RAK4631, Raspberry Pi CM4 Python gateway daemons, offline React 18 PWA dashboard, KiCad PCB schematics, and 3D STL printable models.
- **Demonstration Video**: Available in `/demo` directory on repository.
- **Replay Dataset**: Reviewers can execute `python -m tools.replay_sim` to run the full dashboard on a laptop with zero hardware.
