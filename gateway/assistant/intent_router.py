import re

# Deterministic Intents
STATUS = "STATUS"
TEMPERATURE = "TEMPERATURE"
MOISTURE = "MOISTURE"
CO2_ACTIVITY = "CO2_ACTIVITY"
UNKNOWN = "UNKNOWN"

def route_intent(transcript: str, language: str) -> str:
    """Phase 28: Deterministic Intent Classification before LLM."""
    text = transcript.lower()
    
    if language == "hi-IN":
        if any(w in text for w in ["तापमान", "गर्मी", "गर्म", "ठंडा"]):
            return TEMPERATURE
        if any(w in text for w in ["नमी", "पानी", "सूखा", "गीला"]):
            return MOISTURE
        if any(w in text for w in ["स्थिति", "कैसा", "हाल"]):
            return STATUS
            
    elif language == "gu-IN":
        if any(w in text for w in ["તાપમાન", "ગરમી", "ગરમ", "ઠંડુ"]):
            return TEMPERATURE
        if any(w in text for w in ["ભેજ", "પાણી", "સૂકું", "ભીનું"]):
            return MOISTURE
        if any(w in text for w in ["સ્થિતિ", "કેવું", "હાલ"]):
            return STATUS
            
    else: # English
        if any(w in text for w in ["temperature", "heat", "hot", "cold", "warm"]):
            return TEMPERATURE
        if any(w in text for w in ["moisture", "water", "dry", "wet"]):
            return MOISTURE
        if any(w in text for w in ["status", "how", "condition"]):
            return STATUS
            
    return UNKNOWN
