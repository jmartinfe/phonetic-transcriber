import re

PHONEME_PATTERN = re.compile(r"\[(.*?)\]")
PHRASE_SPLIT_PATTERN = re.compile(r"[^\w\s']")


class Transcription:

    def __init__(self, transcription: str, notes: dict):
        self.transcription = transcription
        self.notes = notes


class TranscriptionService:

    def __init__(self, dictionary: dict, notes: dict):
        self.dictionary = dictionary
        self.notes = notes


    def get_word_transcription(self, word: str) -> Transcription:

        entry = self.dictionary.get(word.lower())
        transcription = word
        if entry:
            transcription = entry[0].get("transcription", word)
        notes = self._get_transcription_notes(transcription)

        return Transcription(transcription, notes)


    def get_phrase_transcription(self, phrase: str) -> Transcription:

        normalized = PHRASE_SPLIT_PATTERN.sub("", phrase.lower())
        words = normalized.split()

        phrase_transcriptions = []
        phrase_notes = {}

        for word in words:

            transcription_obj = self.get_word_transcription(word)

            phrase_transcriptions.append(transcription_obj.transcription)
            phrase_notes.update(transcription_obj.notes)

        transcription = " ".join(phrase_transcriptions)

        return Transcription(transcription, phrase_notes)


    def _get_transcription_notes(self, transcription: str) -> dict:

        transcription_notes = {}

        for phoneme in PHONEME_PATTERN.findall(transcription):

            if phoneme in self.notes:
                transcription_notes[phoneme] = self.notes[phoneme]

        return transcription_notes