# Vermikendra: Security Threat Model

This document outlines the security posture of an entirely offline, local-only IoT system deployed in rural agricultural environments.

## 1. The Core Assumption: Zero Physical Security
We must assume the Raspberry Pi CM4 and the RAK4631 Edge Nodes are mounted in unlocked boxes in open fields.

*   **Risk:** SD Card theft.
*   **Mitigation:** The SQLite database contains zero Personally Identifiable Information (PII), no financial data, and no cloud API keys. The theft of the SD card yields only temperature and CO2 timestamps. Therefore, disk encryption (which would hurt SD card lifespan) is deemed unnecessary for V1.

## 2. The Open Hotspot Paradigm
To ensure rural operators can easily connect their smartphones without managing complex credentials, the `vermikendra.local` Wi-Fi hotspot broadcasted by the Raspberry Pi is **unencrypted and open**.

*   **Risk:** Anyone within 50 meters can connect and access the Next.js PWA Dashboard.
*   **Mitigation:** The system is "Read-Only by Default". The Dashboard provides no vectors to alter the database or command the physical pumps (for V1). An attacker viewing the compost temperatures poses no threat to the operation.

## 3. LoRa Signal Spoofing
*   **Risk:** A bad actor brings their own LoRa transmitter and broadcasts fake 44-byte payloads (e.g., claiming the compost is 80°C) to deliberately trigger the misting pumps and drown the worms.
*   **Mitigation:** The `PayloadType0x01` struct includes a 4-byte `hmac_tag`. In V2, the Gateway will drop any LoRa packet where `HMAC(node_key, payload)` is invalid, making packet injection mathematically infeasible.

## 4. Conclusion
Because Vermikendra operates offline and handles non-sensitive biological data, we optimize for **Availability and Integrity over Confidentiality**. We intentionally sacrifice Wi-Fi confidentiality to maximize operator ease-of-use.
