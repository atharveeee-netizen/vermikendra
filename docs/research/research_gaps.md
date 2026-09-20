# Research Gaps & Unverified Assumptions

The following items cannot be determined purely through theoretical research and **MUST** be measured physically during Phase 5 (Hardware Engineering). Attempting to guess these values violates the Engineering Truth Rule.

## 1. LoRa SX1262 Range and Penetration
- **Gap:** How much does a 50kg bin of dense, wet compost attenuate the 865MHz signal? 
- **Action:** Must perform field tests transmitting from inside a wet compost bin to the gateway indoors. Cannot assume line-of-sight range claims from Semtech datasheets.

## 2. Power Consumption (ePTFE Flush Fan)
- **Gap:** The 40mm fan draws ~150mA at 5V, powered via a boost converter from a 1S Li-Ion cell. What is the real-world battery drain of running this fan for 120 seconds every 4 hours?
- **Action:** Must measure the total coulombic draw of a full respiration cycle using a multimeter/profiler.

## 3. UART SX1262 HAT Interoperability
- **Gap:** The Waveshare LoRa HAT runs custom UART firmware, while the RAK4631 runs raw SPI RadioLib commands. Are they actually packet-compatible?
- **Action:** Must run the "Spike test" (Days 1-3) defined in the TRD to prove the HAT can decode raw LoRa P2P packets from the node. If it fails, fallback to a second RAK4631 as the gateway radio.
