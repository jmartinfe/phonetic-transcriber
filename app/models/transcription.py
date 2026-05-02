from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from app.models.token_type import TokenType
    
class WordTranscription(BaseModel):
    word: str = Field(
        ..., 
        description="Original token from the input text (word or punctuation)"
    )

    type: TokenType = Field(
        ..., 
        description="Type of token: word, opening punctuation, closing punctuation or neutral punctuation"
    )

    transcription: Optional[List[str]] = Field(
        None,
        description="Spanish-friendly phonetic transcription (approximate pronunciation)"
    )

    ipa: Optional[List[str]] = Field(
        None,
        description="IPA phonetic transcription"
    )

    notes: Optional[Dict[str, str]] = Field(
        None,
        description="Additional notes about pronunciation or transcription"
    )

    found: bool = Field(
        True,
        description="Whether the word was found in the dictionary"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "word": "Hello",
                "type": "word",
                "transcription": ["jelou"],
                "ipa": ["həˈloʊ"],
                "notes": {
                    "pronunciation": "Stress on second syllable"
                },
                "found": True
            }
        }
    }


class Transcription(BaseModel):
    original_text: str = Field(
        ..., 
        description="Original input text"
    )

    transcriptions: List[WordTranscription] = Field(
        ..., 
        description="List of tokens with their phonetic transcription"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "original_text": "Hello, world!",
                "transcriptions": [
                    {
                        "word": "Hello",
                        "type": "word",
                        "transcription": ["jelou"],
                        "ipa": ["həˈloʊ"],
                        "notes": {
                            "pronunciation": "Stress on second syllable"
                        },
                        "found": True
                    },
                    {
                        "word": ",",
                        "type": "punct",
                        "transcription": None,
                        "ipa": None,
                        "notes": None,
                        "found": True
                    },
                    {
                        "word": "world",
                        "type": "word",
                        "transcription": ["uorld"],
                        "ipa": ["wɜrld"],
                        "notes": {},
                        "found": True
                    }
                ]
            }
        }
    }

class TranscriptionRequest(BaseModel):
    text: str

class BatchTranscriptionRequest(BaseModel):
    texts: List[str]

class BatchTranscriptionResponse(BaseModel):
    transcriptions: List[Transcription]