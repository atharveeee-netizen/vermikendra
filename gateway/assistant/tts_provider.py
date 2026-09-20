import os
import requests
import base64

SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', '')

class TTSProvider:
    def synthesize(self, text: str, language: str) -> bytes:
        raise NotImplementedError()

class SarvamTTSProvider(TTSProvider):
    def synthesize(self, text: str, language: str) -> bytes:
        if not SARVAM_API_KEY:
            raise Exception("SARVAM_API_KEY not configured")
            
        url = "https://api.sarvam.ai/text-to-speech"
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "inputs": [text],
            "target_language_code": language,
            "speaker": "meera",
            "pitch": 0,
            "pace": 1.0,
            "loudness": 1.5,
            "speech_sample_rate": 16000,
            "enable_preprocessing": True,
            "model": "bulbul:v1"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code != 200:
            raise Exception(f"Sarvam TTS failed: {response.text}")
            
        return base64.b64decode(response.json()['audios'][0])

class HuggingFaceTTSProvider(TTSProvider):
    def synthesize(self, text: str, language: str) -> bytes:
        raise Exception("UNVERIFIED: HF local TTS not benchmarked on target hardware.")

def get_tts_provider() -> TTSProvider:
    provider = os.getenv('TTS_PROVIDER', 'sarvam')
    if provider == 'huggingface':
        return HuggingFaceTTSProvider()
    return SarvamTTSProvider()
