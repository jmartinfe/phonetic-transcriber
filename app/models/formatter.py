from typing import List
from app.models.token_type import TokenType

class TranscriptionToken:
    def __init__(self, transcription: str, ipa: str):
        self.transcription = transcription
        self.ipa = ipa

class FormattedToken:
    def __init__(self, 
                 display: str,
                 transcription: str,
                 ipa: str,
                 type: TokenType,
                 alternatives: List[TranscriptionToken]):
        self.display = display
        self.transcription = transcription
        self.ipa = ipa
        self.type = type
        self.alternatives = alternatives

class FormattedTextTranscription:
    def __init__(self,
                 token_transcriptions: List[FormattedToken],
                 notes: dict[str, str],
                 original: str):
        self.token_transcriptions = token_transcriptions
        self.notes = notes
        self.original = original

