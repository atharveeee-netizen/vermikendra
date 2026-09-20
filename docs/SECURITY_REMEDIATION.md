# Security Remediation Report

**Date**: 2026-09-21
**Phase**: 1 - Secret Incident

## Incident Summary
An independent repository audit uncovered a hardcoded `SARVAM_API_KEY` credential belonging to the user (`sk_b7zyfv59_q1pV0JXoTApKDUQ8oITKGtFK`) embedded within `gateway/api.py` and `gateway/test_stt.py`.

## Remediation Applied
1. The hardcoded keys were stripped from `api.py` and `test_stt.py`.
2. The code now exclusively uses `os.getenv("SARVAM_API_KEY")` with no fallback.
3. A `gateway/.env.example` file was created defining the placeholder.
4. **CRITICAL:** The leaked API key exists in the Git history of `gateway/api.py`. It MUST be revoked and rotated externally via the Sarvam provider console by the account owner. Do not use this key for production.
