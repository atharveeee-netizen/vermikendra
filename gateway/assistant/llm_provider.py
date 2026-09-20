from typing import Dict, Any

class LLMProvider:
    def generate_answer(self, intent: str, context: Dict[str, Any], language: str) -> str:
        raise NotImplementedError()

class DeterministicFallbackLLM(LLMProvider):
    def generate_answer(self, intent: str, context: Dict[str, Any], language: str) -> str:
        """Phase 29/30: Safe Deterministic Generation if no external LLM is configured."""
        if not context:
            if language == "hi-IN": return "मेरे पास इस बेड का कोई नया डेटा नहीं है।"
            if language == "gu-IN": return "મારી પાસે આ બેડનો કોઈ નવો ડેટા નથી."
            return "I have no recent data for this bed."
            
        temp = context.get('ambient_c') or context.get('probe_1')
        moist = context.get('moisture_raw')
        
        if language == "hi-IN":
            if intent == "TEMPERATURE":
                return f"बेड का तापमान {temp} डिग्री है।"
            elif intent == "MOISTURE":
                return f"नमी का स्तर {moist} है।"
            else:
                return f"बेड सामान्य है। तापमान {temp} डिग्री और नमी {moist} है।"
                
        elif language == "gu-IN":
            if intent == "TEMPERATURE":
                return f"બેડનું તાપમાન {temp} ડિગ્રી છે."
            elif intent == "MOISTURE":
                return f"ભેજનું સ્તર {moist} છે."
            else:
                return f"બેડ સામાન્ય છે. તાપમાન {temp} ડિગ્રી અને ભેજ {moist} છે."
                
        else: # en-IN
            if intent == "TEMPERATURE":
                return f"The bed temperature is {temp} degrees."
            elif intent == "MOISTURE":
                return f"The moisture level is {moist}."
            else:
                return f"The bed is normal. Temperature is {temp} degrees and moisture is {moist}."

def get_llm_provider() -> LLMProvider:
    # Future integration point for OpenAI/Anthropic/LocalLLM
    return DeterministicFallbackLLM()
