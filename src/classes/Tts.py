import os
import requests
import json
from typing import Optional
from status import info, warning, error, success
from config import ROOT_DIR, get_tts_engine, get_tts_voice, get_elevenlabs_api_key, get_openai_api_key

class TTS:
    def __init__(self) -> None:
        self.tts_engine = get_tts_engine()
        self.tts_voice = get_tts_voice()
        self.elevenlabs_api_key = get_elevenlabs_api_key() if self.tts_engine == 'elevenlabs' else None
        self.openai_api_key = get_openai_api_key() if self.tts_engine == 'openai' else None

    def synthesize(self, text: str, output_file: str = os.path.join(ROOT_DIR, "tmp", "audio.wav")) -> str:
        if self.tts_engine == 'elevenlabs':
            return self._synthesize_elevenlabs(text, output_file)
        elif self.tts_engine == 'openai':
            return self._synthesize_openai(text, output_file)
        else:
            raise ValueError(f"Unsupported TTS engine: {self.tts_engine}")

    def _synthesize_elevenlabs(self, text: str, output_file: str) -> str:
        info("Synthesizing text using ElevenLabs")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.tts_voice}"
        headers = {
            "xi-api-key": self.elevenlabs_api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2"
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        with open(output_file, "wb") as f:
            f.write(response.content)

        success(f"Audio synthesized successfully and saved to {output_file}")
        return output_file

    def _synthesize_openai(self, text: str, output_file: str) -> str:
        info("Synthesizing text using OpenAI")
        url = "https://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "tts-1",
            "input": text,
            "voice": self.tts_voice
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        with open(output_file, "wb") as f:
            f.write(response.content)

        success(f"Audio synthesized successfully and saved to {output_file}")
        return output_file
