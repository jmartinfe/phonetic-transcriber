import pytest
from app.services.transcription import TranscriptionService, Transcription


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
    return TranscriptionService(sample_dictionary, sample_notes)


class TestTranscriptionService:

    def test_get_word_transcription_existing_word(self, transcription_service):
        result = transcription_service.get_word_transcription("hello")
        assert isinstance(result, Transcription)
        assert result.transcription == "h[e]lo"
        assert result.notes == {"e": "Note for e"}

    def test_get_word_transcription_known_word_no_notes(self, transcription_service):
        result = transcription_service.get_word_transcription("world")
        assert isinstance(result, Transcription)
        assert result.transcription == "w[o]rld"
        assert result.notes == {"o": "Note for o"}

    def test_get_word_transcription_unknown_word(self, transcription_service):
        result = transcription_service.get_word_transcription("xyz")
        assert isinstance(result, Transcription)
        assert result.transcription == "xyz"
        assert result.notes == {}

    def test_get_word_transcription_case_insensitive(self, transcription_service):
        result = transcription_service.get_word_transcription("HELLO")
        assert isinstance(result, Transcription)
        assert result.transcription == "h[e]lo"
        assert result.notes == {"e": "Note for e"}

    def test_get_phrase_transcription_single_word(self, transcription_service):
        result = transcription_service.get_phrase_transcription("hello")
        assert isinstance(result, Transcription)
        assert result.transcription == "h[e]lo"
        assert result.notes == {"e": "Note for e"}

    def test_get_phrase_transcription_multiple_words(self, transcription_service):
        result = transcription_service.get_phrase_transcription("hello world")
        assert isinstance(result, Transcription)
        assert result.transcription == "h[e]lo w[o]rld"
        assert result.notes == {"e": "Note for e", "o": "Note for o"}

    def test_get_phrase_transcription_with_punctuation(self, transcription_service):
        result = transcription_service.get_phrase_transcription("hello, world!")
        assert isinstance(result, Transcription)
        assert result.transcription == "h[e]lo w[o]rld"
        assert result.notes == {"e": "Note for e", "o": "Note for o"}

    def test_get_phrase_transcription_mixed_known_unknown(self, transcription_service):
        result = transcription_service.get_phrase_transcription("hello xyz")
        assert isinstance(result, Transcription)
        assert result.transcription == "h[e]lo xyz"
        assert result.notes == {"e": "Note for e"}

    def test_get_phrase_transcription_empty_phrase(self, transcription_service):
        result = transcription_service.get_phrase_transcription("")
        assert isinstance(result, Transcription)
        assert result.transcription == ""
        assert result.notes == {}

    def test_get_phrase_transcription_case_insensitive(self, transcription_service):
        result = transcription_service.get_phrase_transcription("HELLO WORLD")
        assert isinstance(result, Transcription)
        assert result.transcription == "h[e]lo w[o]rld"
        assert result.notes == {"e": "Note for e", "o": "Note for o"}


class TestTranscription:

    def test_transcription_creation(self):
        trans = Transcription("h[e]lo", {"e": "note"})
        assert trans.transcription == "h[e]lo"
        assert trans.notes == {"e": "note"}