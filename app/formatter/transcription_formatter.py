from app.models.transcription import Transcription

def format_transcription_to_display(transcription: Transcription) -> str:
    """
    Format the transcription for display purposes.
    This function can be customized to apply specific formatting rules,
    such as adding spaces between phonemes, capitalizing certain symbols, etc.

    Args:
        transcription (str): The raw transcription string.

    Returns:
        str: A formatted string of the transcription for display purposes.
    """
    # Example formatting: add spaces between phonemes and capitalize
    return transcription.strip().upper()