from pydantic import BaseModel
from typing import List, Optional, Dict
from app.models.token_type import TokenType
    
class WordTranscription(BaseModel):
    word: str
    type: TokenType
    transcription: Optional[List[str]] = None
    ipa: Optional[List[str]] = None
    notes: Optional[Dict[str, str]] = None
    found: bool = True


class Transcription(BaseModel):
    original_text: str
    transcriptions: List[WordTranscription]

class TranscriptionRequest(BaseModel):
    text: str

class BatchTranscriptionRequest(BaseModel):
    texts: List[str]

class BatchTranscriptionResponse(BaseModel):
    transcriptions: List[Transcription]