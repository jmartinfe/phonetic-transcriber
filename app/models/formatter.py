from typing import List
from app.models.token_type import TokenType
from pydantic import BaseModel
from typing import List, Optional, Dict

class TranscriptionToken(BaseModel):
    transcription: str
    ipa: str
    display: str
    flat_display: str

class FormattedToken(BaseModel):
    display: str
    flat_display: str
    transcription: str
    ipa: str
    type: TokenType
    found: bool
    alternatives: List[TranscriptionToken]

class FormattedTextTranscription(BaseModel):
    token_transcriptions: List[FormattedToken]
    notes: dict[str, str]
    original: str
