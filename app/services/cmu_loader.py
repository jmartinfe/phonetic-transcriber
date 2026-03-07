import json
from dataclasses import dataclass
from typing import List, Optional
from functools import lru_cache

CMU_FILE_PATH = 'app/data/cmu_dict.json'  # Path to the CMU Pronouncing Dictionary JSON file
ES_TRANSCRIPTION_PATH = 'app/data/es_transcription.json'  # Path to the Spanish transcription JSON file
ES_COMPILED_DICTIONARY_PATH = 'app/build/es_compiled_dictionary.json'  # Path to save the compiled dictionary JSON file
cmu_dict = None
transcription_dict = None

@dataclass
class WordTranscription:
    transcription: List[str]
    ipa: Optional[List[str]] = None
    description: Optional[str] = None

@lru_cache
def get_cmu_dict() -> dict:
    """Get the CMU Pronouncing Dictionary. """
    with open(CMU_FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

@lru_cache
def get_transcription() -> dict:
    """Get the Spanish transcription dictionary."""
    with open(ES_TRANSCRIPTION_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_word_transcription(word: str) -> list[list[str]]:
    """
    Get the transcription of a word using the CMU Pronouncing Dictionary and the Spanish transcription.
    - cmu_dict json format is a dictionary with words as keys and lists of pronunciations as values.
        example: {"PRONUNCIATION": ["P R AH N AH N S IY EY SH AH N"]} 

    - transcription json format is a dictionary with phonemes as keys and dictionaries with "transcription",
        "ipa" and "description" as values.
        example: {"P": {"transcription": "p", "ipa": "p", "description": "voiceless bilabial plosive"}}
    """
    
    cmu_dict = get_cmu_dict()
    transcription_dict = get_transcription()

    prons = cmu_dict.get(word.upper(), [])

    results = []

    for pron in prons:
        phonemes = pron.split()

        results.append([
            transcription_dict.get(p, {}).get("transcription", "")
            for p in phonemes
        ])

    return results

def build_compiled_dictionary():
    """Build a compiled dictionary that combines the CMU Pronouncing Dictionary and the Spanish transcription.
        The compiled dictionary will have the following format:
        {
            "EXCLAMATION": [
                {
                    "transcription":"ekskle(o)méise(o)n",
                    "ipa": "ɛkskɫəmeɪʃən",
                    "description": "e(o): Sonido \"e\" con labios de decir \"o\". s: Sonido siseante, más corto que al pedir silencio"
                }
            ]
        }
    """
    cmu = get_cmu_dict()
    rules = get_transcription()

    trans_map = {}
    ipa_map = {}
    desc_map = {}

    for phoneme, rule in rules.items():
        trans_map[phoneme] = rule.get("transcription", "")
        ipa = rule.get("ipa", "")
        ipa_map[phoneme] = ipa
        desc = rule.get("description", "")
        desc_map[phoneme] = f"/{ipa}/: {desc}" if ipa and desc else "" # Only add to desc_map if there is a description

    compiled = {}

    for word, prons in cmu.items():

        entries = []

        for pron in prons:

            phonemes = pron.split()

            transcription = []
            ipa = []
            descriptions = []
            seen = set()

            for p in phonemes:

                t = trans_map.get(p)
                if t:
                    transcription.append(t)
                ipa.append(ipa_map.get(p, ""))

                desc = desc_map.get(p)

                if desc and desc not in seen:
                    descriptions.append(desc)
                    seen.add(desc)

            entry = {
                "transcription": "".join(transcription),
                "ipa": "".join(ipa)
            }

            if descriptions:
                descriptions = dict.fromkeys(sorted(descriptions))  # Remove duplicates while preserving order
                entry["description"] = ". ".join(descriptions)

            entries.append(entry)

        compiled[word] = entries

    return compiled

def save_compiled_dictionary():
    compiled = build_compiled_dictionary()

    with open(ES_COMPILED_DICTIONARY_PATH, "w", encoding="utf8") as f:
        json.dump(compiled, f, ensure_ascii=False, separators=(",", ":"))