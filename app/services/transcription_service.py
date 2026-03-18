from app.models.transcription import Transcription, WordTranscription
from app.models.compiled_data import CompiledData
from app.services.exceptions import EmptyTextError, TextTooLongError, WordHasBlankSpacesError
import re


PHONEME_PATTERN = re.compile(r"\[(.*?)\]")
PHRASE_SPLIT_PATTERN = re.compile(r"[^\w\s']", re.UNICODE)
MAX_WORD_LENGTH = 50
MAX_TEXT_LENGTH = 2000


class TranscriptionService:

    def __init__(self, compiled_data: CompiledData):
        self.data = compiled_data


    def get_word_transcription(self, word: str) -> WordTranscription:
        """ Returns the transcription and IPA for a given word, along with any relevant notes. """
        if not word.strip():
            raise EmptyTextError()
        if len(word) > MAX_WORD_LENGTH:
            raise TextTooLongError(MAX_WORD_LENGTH)
        if " " in word:
            raise WordHasBlankSpacesError()
        word_normalized = word.lower()
        entries = self.data.dictionary.get(word_normalized, [])
        if entries:
            transcription = [entry.get("transcription") for entry in entries if "transcription" in entry]
            ipa = [entry.get("ipa") for entry in entries if "ipa" in entry]
            notes = {}
            for entry in entries:
                if "transcription" in entry:
                    notes.update(
                        self._get_transcription_notes(entry.get("transcription", ""))
                    )
            found = True
        else:
            transcription = [word_normalized]
            ipa = [word_normalized]
            notes = {}
            found = False

        return WordTranscription(word=word_normalized, transcription=transcription, ipa=ipa, notes=notes, found=found)

    def get_phrase_transcription(self, phrase: str) -> Transcription:
        """ Returns the transcription and IPA for each word in a given phrase, along with any relevant notes. """
        if not phrase.strip():
            raise EmptyTextError()
        if len(phrase) > MAX_TEXT_LENGTH:
            raise TextTooLongError(MAX_TEXT_LENGTH)
        normalized = PHRASE_SPLIT_PATTERN.sub("", phrase.lower())
        words = normalized.split()

        return Transcription(original_text=phrase, transcriptions=[self.get_word_transcription(word) for word in words])


    def _get_transcription_notes(self, transcription: str) -> dict:
        """ Extracts phonemes from the transcription and retrieves any associated notes from the compiled data. """
        return {
            phoneme: self.data.notes[phoneme]
            for phoneme in PHONEME_PATTERN.findall(transcription)
            if phoneme in self.data.notes
        }