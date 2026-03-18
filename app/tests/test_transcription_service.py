import pytest
from app.services.transcription_service import TranscriptionService
from app.models.transcription import Transcription, WordTranscription
from app.models.compiled_data import CompiledData


@pytest.fixture
def sample_dictionary():
    return {
        "hello": [{"transcription": "h[e]lo", "ipa": "helo"}],
        "world": [{"transcription": "w[o]rld", "ipa": "world"}],
        "test": [{"transcription": "t[e]st", "ipa": "test"}],
        "unknown": [{"transcription": "unknown", "ipa": "unknown"}]  # fallback case
    }


@pytest.fixture
def sample_notes():
    return {
        "e": "Note for e",
        "o": "Note for o"
    }


@pytest.fixture
def transcription_service(sample_dictionary, sample_notes):
    return TranscriptionService(CompiledData(dictionary=sample_dictionary, notes=sample_notes))


class TestTranscriptionService:

    def test_get_word_transcription_existing_word(self, transcription_service):
        result = transcription_service.get_word_transcription("hello")
        assert isinstance(result, WordTranscription)
        assert result.word == "hello"
        assert result.transcription == ["h[e]lo"]
        assert result.ipa == ["helo"]
        assert result.notes == {"e": "Note for e"}
        assert result.found == True

    def test_get_word_transcription_known_word_no_notes(self, transcription_service):
        result = transcription_service.get_word_transcription("world")
        assert isinstance(result, WordTranscription)
        assert result.word == "world"
        assert result.transcription == ["w[o]rld"]
        assert result.ipa == ["world"]
        assert result.notes == {"o": "Note for o"}
        assert result.found == True

    def test_get_word_transcription_unknown_word(self, transcription_service):
        result = transcription_service.get_word_transcription("xyz")
        assert isinstance(result, WordTranscription)
        assert result.word == "xyz"
        assert result.transcription == ["xyz"]
        assert result.ipa == ["xyz"]
        assert result.notes == {}
        assert result.found == False

    def test_get_word_transcription_case_insensitive(self, transcription_service):
        result = transcription_service.get_word_transcription("HELLO")
        assert isinstance(result, WordTranscription)
        assert result.word == "hello"
        assert result.transcription == ["h[e]lo"]
        assert result.ipa == ["helo"]
        assert result.notes == {"e": "Note for e"}
        assert result.found == True

    def test_get_phrase_transcription_single_word(self, transcription_service):
        result = transcription_service.get_phrase_transcription("hello")
        assert isinstance(result, Transcription)
        assert result.original_text == "hello"
        assert len(result.transcriptions) == 1
        word_trans = result.transcriptions[0]
        assert word_trans.word == "hello"
        assert word_trans.transcription == ["h[e]lo"]
        assert word_trans.ipa == ["helo"]
        assert word_trans.notes == {"e": "Note for e"}
        assert word_trans.found == True

    def test_get_phrase_transcription_multiple_words(self, transcription_service):
        result = transcription_service.get_phrase_transcription("hello world")
        assert isinstance(result, Transcription)
        assert result.original_text == "hello world"
        assert len(result.transcriptions) == 2
        hello_trans = result.transcriptions[0]
        assert hello_trans.word == "hello"
        assert hello_trans.transcription == ["h[e]lo"]
        assert hello_trans.notes == {"e": "Note for e"}
        world_trans = result.transcriptions[1]
        assert world_trans.word == "world"
        assert world_trans.transcription == ["w[o]rld"]
        assert world_trans.notes == {"o": "Note for o"}

    def test_get_phrase_transcription_with_punctuation(self, transcription_service):
        result = transcription_service.get_phrase_transcription("hello, world!")
        assert isinstance(result, Transcription)
        assert result.original_text == "hello, world!"
        assert len(result.transcriptions) == 2
        hello_trans = result.transcriptions[0]
        assert hello_trans.word == "hello"
        assert hello_trans.transcription == ["h[e]lo"]
        assert hello_trans.notes == {"e": "Note for e"}
        world_trans = result.transcriptions[1]
        assert world_trans.word == "world"
        assert world_trans.transcription == ["w[o]rld"]
        assert world_trans.notes == {"o": "Note for o"}

    def test_get_phrase_transcription_mixed_known_unknown(self, transcription_service):
        result = transcription_service.get_phrase_transcription("hello xyz")
        assert isinstance(result, Transcription)
        assert result.original_text == "hello xyz"
        assert len(result.transcriptions) == 2
        hello_trans = result.transcriptions[0]
        assert hello_trans.word == "hello"
        assert hello_trans.transcription == ["h[e]lo"]
        assert hello_trans.notes == {"e": "Note for e"}
        xyz_trans = result.transcriptions[1]
        assert xyz_trans.word == "xyz"
        assert xyz_trans.transcription == ["xyz"]
        assert xyz_trans.ipa == ["xyz"]
        assert xyz_trans.notes == {}
        assert xyz_trans.found == False

    def test_get_phrase_transcription_empty_phrase(self, transcription_service):
        result = transcription_service.get_phrase_transcription("")
        assert isinstance(result, Transcription)
        assert result.original_text == ""
        assert result.transcriptions == []

    def test_get_phrase_transcription_case_insensitive(self, transcription_service):
        result = transcription_service.get_phrase_transcription("HELLO WORLD")
        assert isinstance(result, Transcription)
        assert result.original_text == "HELLO WORLD"
        assert len(result.transcriptions) == 2
        hello_trans = result.transcriptions[0]
        assert hello_trans.word == "hello"
        assert hello_trans.transcription == ["h[e]lo"]
        assert hello_trans.notes == {"e": "Note for e"}
        world_trans = result.transcriptions[1]
        assert world_trans.word == "world"
        assert world_trans.transcription == ["w[o]rld"]
        assert world_trans.notes == {"o": "Note for o"}


class TestWordTranscription:

    def test_word_transcription_creation(self):
        trans = WordTranscription(word="hello", transcription=["h[e]lo"], ipa=["helo"], notes={"e": "note"}, found=True)
        assert trans.word == "hello"
        assert trans.transcription == ["h[e]lo"]
        assert trans.ipa == ["helo"]
        assert trans.notes == {"e": "note"}
        assert trans.found == True


class TestTranscription:

    def test_transcription_creation(self):
        word_trans = WordTranscription(word="hello", transcription=["h[e]lo"], notes={"e": "note"})
        trans = Transcription(original_text="hello", transcriptions=[word_trans])
        assert trans.original_text == "hello"
        assert trans.transcriptions == [word_trans]