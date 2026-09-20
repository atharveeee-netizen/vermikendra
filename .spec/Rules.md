# Vermikendra Implementation Rules

## 1. Engineering Truth Rule
- Never confuse IMPLEMENTED, VALIDATED, SPECIFIED, PLANNED, or UNVERIFIED.
- An item is IMPLEMENTED only if source code exists. 
- Never fabricate hardware tests, ML accuracy, battery life, or sensor measurements.

## 2. AI and ML Limitations
- Do NOT introduce ML without a real dataset.
- Start with classical, interpretable statistical analytics (rate of change, least-squares fit) before using gradient boosting or deep learning.
- Readiness must be framed as "evidence based on respiration trend," not "AI knows when it is ready."

## 3. Gateway Resilience
- Gateway must work completely without internet.
- SQLite must use WAL mode.
- Systemd must manage and auto-restart Python daemon services.

## 4. Hardware Awareness
- Assume the LoRa radio interface (Waveshare HAT vs native SPI) is risky until tested.
- Do not claim LoRa range until measured.
- Use explicit HMAC-SHA256 signing for all packets to prevent spoofing.
