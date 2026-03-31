from app.models.transcription import Transcription, WordTranscription
from app.models.formatter import FormattedTextTranscription, FormattedToken, TranscriptionToken

def transcription_to_formatted_text_transcription(transcription: Transcription) -> FormattedTextTranscription:
    """
    Format the transcription for display purposes.
    This function can be customized to apply specific formatting rules,
    such as adding spaces between phonemes, capitalizing certain symbols, etc.

    Args:
        transcription (str): The raw transcription string.

    Returns:
        FormattedTextTranscription: A formatted transcription object for display purposes.
    """
    # Example formatting: add spaces between phonemes and capitalize
    formatted_tokens = []
    for word_transcription in transcription.transcriptions:
        formatted_token = word_transcription_to_formatted_token(word_transcription)
        formatted_tokens.append(formatted_token)

    return FormattedTextTranscription(
        token_transcriptions=formatted_tokens,
        notes=word_transcriptions_to_notes(transcription.transcriptions),
        original=transcription.original_text
    )

def word_transcription_to_formatted_token(word_transcription: WordTranscription) -> FormattedToken:
    """
    Convert a WordTranscription to a FormattedToken, applying formatting rules.
    display is taken from the first transcription if available, otherwise the original word.
    transcription and ipa are expected to be lists, we take the first element for display and alternatives for the rest.
    """
    has_transcripttions = bool(word_transcription.transcription and len(word_transcription.transcription) > 0)
    has_ipa = bool(word_transcription.ipa and len(word_transcription.ipa) > 0)

    # For display, we take the first transcription if available, otherwise we use the original word.
    main_transcription = word_transcription.transcription[0] if has_transcripttions else ""
    main_ipa = word_transcription.ipa[0] if has_ipa else ""

    raw_word = word_transcription.word
    
    display_text, flat_text = _get_transcription_displays(raw_word, main_transcription, word_transcription.found)

    """
    For alternatives, we take the remaining transcriptions and ipas, and pair them up.
    We also generate display and flat_display for each alternative transcription.
    """
    alternatives = [
        TranscriptionToken(transcription=t, ipa=i, display=d, flat_display=f)
        for t, i in zip(word_transcription.transcription[1:] or [], word_transcription.ipa[1:] or [])
        for d, f in [_get_transcription_displays(raw_word, t, word_transcription.found)]
    ]

    return FormattedToken(
        display=display_text,
        flat_display=flat_text,
        transcription=display_text if main_transcription else "",
        ipa=main_ipa,
        type=word_transcription.type,
        found=word_transcription.found,
        alternatives=alternatives
    )

def _get_transcription_displays(raw_word: str, main_transcription: str, found: bool) -> tuple[str, str]:
    """
    Get the display and flat display for a given WordTranscription.
    If the word was not found or has no transcription, return the original word for both displays.
    Otherwise, return the first transcription for display and a flat version of it for flat_display.
    """
    if not found or not main_transcription:
        display_text = raw_word
        flat_text = raw_word
    else:
        display_text = main_transcription
        flat_text = main_transcription.replace("[", "").replace("]", "")
    return display_text, flat_text

def word_transcriptions_to_notes(word_transcriptions: list[WordTranscription]) -> dict[str, str]:
    """
    Convert a list of WordTranscriptions to a dictionary of notes for display.
    This can be used to provide additional information about each word in the transcription.
    """
    notes: dict[str, str] = {}

    for wt in word_transcriptions:
        if wt.notes:
            notes.update(wt.notes)

    return notes