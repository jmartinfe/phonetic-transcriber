import re
from functools import lru_cache
from app.models.transcription import Transcription, WordTranscription, TokenType
from app.models.compiled_data import CompiledData
from app.services.exceptions import EmptyTextError, TextTooLongError, WordHasBlankSpacesError


PHONEME_PATTERN = re.compile(r"\[(.*?)\]")
WORD_PATTERN = r"\w+(?:['’]\w+)*"
PUNCT_PATTERN = r"[^\w\s\"'“”‘’]" # Matches any punctuation character except ambiguous opening/closing characters
PHRASE_SPLIT_PATTERN = re.compile(
    f"{WORD_PATTERN}|{PUNCT_PATTERN}",
    re.UNICODE
)
MAX_WORD_LENGTH = 50
MAX_TEXT_LENGTH = 2000
OPEN_PUNCT = {
    "(", "[", "{",
    "¿", "¡",
    "«"
}
CLOSE_PUNCT = {
    ")", "]", "}",
    "?", "!",
    "»"
}
AMBIGUOUS_PUNCT = {'"', "'", "“", "”", "‘", "’"}

class TranscriptionService:

    def __init__(self, compiled_data: CompiledData):
        self.data = compiled_data

    @lru_cache(maxsize=10000)
    def _get_word_transcription_cached(self, word: str) -> WordTranscription:
        """ Internal method to retrieve transcription and IPA for a word,
            with caching for performance. """
        if not re.match(r"^\w+(?:['’]\w+)*$", word):
            return WordTranscription(word=word,
                                     type=TokenType.PUNCT_OPEN 
                                        if word in OPEN_PUNCT 
                                            else TokenType.PUNCT_CLOSE if word in CLOSE_PUNCT
                                            else TokenType.PUNCT,
                                     transcription=[],
                                     ipa=[],
                                     notes={},
                                     found=False)
        entries = self.data.dictionary.get(word, [])
        transcription = [entry.get("transcription") for entry in entries if "transcription" in entry]
        ipa = [entry.get("ipa") for entry in entries if "ipa" in entry]
        notes = {}

        for entry in entries:
            if "transcription" in entry:
                notes.update(self._get_transcription_notes(entry["transcription"]))

        return WordTranscription(word=word,
                                 type=TokenType.WORD,
                                 transcription=transcription,
                                 ipa=ipa,
                                 notes=notes,
                                 found=bool(entries))


    def get_word_transcription(self, word: str) -> WordTranscription:
        """ Returns the transcription and IPA for a given word, along with any relevant notes. """
        if not word.strip():
            raise EmptyTextError()
        if len(word) > MAX_WORD_LENGTH:
            raise TextTooLongError(MAX_WORD_LENGTH)
        if " " in word:
            raise WordHasBlankSpacesError()

        word_normalized = word.lower()
        return self._get_word_transcription_cached(word_normalized)
    
    def get_phrase_transcription(self, phrase: str) -> Transcription:
        """ Returns the transcription and IPA for each word in a given phrase, along with any relevant notes. """
        if not phrase.strip():
            raise EmptyTextError()
        if len(phrase) > MAX_TEXT_LENGTH:
            raise TextTooLongError(MAX_TEXT_LENGTH)
        words = PHRASE_SPLIT_PATTERN.findall(phrase.lower())

        return Transcription(original_text=phrase, transcriptions=[self.get_word_transcription(word) for word in words])


    def _get_transcription_notes(self, transcription: str) -> dict:
        """ Extracts phonemes from the transcription and retrieves any associated notes from the compiled data. """
        return {
            phoneme: self.data.notes[phoneme]
            for phoneme in PHONEME_PATTERN.findall(transcription)
            if phoneme in self.data.notes
        }