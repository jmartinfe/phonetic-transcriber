from typing import List
from app.models.token_type import TokenType

class TranscriptionToken:
    def __init__(self, transcription: str, ipa: str, display: str, flat_display: str):
        self.transcription = transcription
        self.ipa = ipa
        self.display = display
        self.flat_display = flat_display


class FormattedToken:
    def __init__(self, 
                 display: str,
                 flat_display: str,
                 transcription: str,
                 ipa: str,
                 type: TokenType,
                 found: bool,
                 alternatives: List[TranscriptionToken]):
        self.display = display
        self.flat_display = flat_display
        self.transcription = transcription
        self.ipa = ipa
        self.type = type
        self.found = found
        self.alternatives = alternatives

class FormattedTextTranscription:
    def __init__(self,
                 token_transcriptions: List[FormattedToken],
                 notes: dict[str, str],
                 original: str):
        self.token_transcriptions = token_transcriptions
        self.notes = notes
        self.original = original

