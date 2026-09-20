# Vermikendra: Performance Metrics

This document outlines the hard mathematical constraints the architecture was built around.

## 1. LoRa Time-on-Air (ToA)
The `PayloadType0x01` binary struct is strictly enforced at **44 bytes**.

Using LoRa at 865 MHz (India ISM band):
*   **Spreading Factor (SF):** 9
*   **Bandwidth (BW):** 125 kHz
*   **Coding Rate (CR):** 4/5
*   **Explicit Header:** On
*   **Preamble Length:** 8 symbols

**Calculated ToA:** `144.38 ms`
*   This falls well within the legal 1% duty cycle limit (allowing up to ~250 packets per hour if needed, though we only transmit once every 10-60 minutes).

## 2. Power Budget (RAK4631 Edge Node)
*   **Deep Sleep Baseline:** ~2.0 µA (The firmware physically cuts `3V3_S` to the sensors).
*   **Wake / Sample (SCD41):** ~18 mA for 5 seconds (The SCD41 requires spin-up time).
*   **Transmit (Tx @ 14 dBm):** ~110 mA for 144 ms.
*   **Battery Life Estimate:** On a standard 18650 (3000 mAh) sending data every 60 minutes, the node should theoretically last >18 months before a solar recharge is strictly necessary.

## 3. Database Ingestion (Raspberry Pi CM4)
*   **SQLite WAL Mode:** Can handle hundreds of concurrent read operations from the Next.js dashboard while `vk_ingest.py` writes new packets. No locking contention expected at the target scale of 100 bins per Gateway.
