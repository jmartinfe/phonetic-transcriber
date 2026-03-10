import json
from dataclasses import dataclass
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

sources = {
    "cmu" : Path("app/data/cmu_dict.json"),  # Path to the CMU Pronouncing Dictionary JSON file
    "es_transcriptions" : Path("app/data/es_transcription.json")  # Path to the Spanish transcription JSON file
}

BUILD_DIR = Path("app/build") # Path to the folder where compiled files are stored
ES_COMPILED_DICTIONARY_PATH = BUILD_DIR / "es_compiled_dictionary.json"  # Path to save the compiled dictionary JSON file

@dataclass
class RuleMaps:
    transcriptions: dict
    ipa: dict
    descriptions: dict

def get_source_dict(source: Path) -> dict:
    """Returns dict structure based on source json file. """
    with source.open(encoding="utf-8") as f:
        return json.load(f)

def needs_rebuild():
    """ Executes compiled dictionary rebuild if it doesn't exist or is not up to date """
    if not ES_COMPILED_DICTIONARY_PATH.exists():
        logger.info(f"Compiled dictionary not found at {ES_COMPILED_DICTIONARY_PATH}. Rebuild needed.")
        return True

    compiled_time = ES_COMPILED_DICTIONARY_PATH.stat().st_mtime
    for s in sources.values():
        if s.stat().st_mtime > compiled_time:
            logger.info(f"Source file {s} has been modified since last compilation. Rebuild needed.")
            return True

    logger.info("Compiled dictionary is up to date. No rebuild needed.")
    return False

def parse_rules(transcriptions: dict) -> RuleMaps:

    trans_map = {}
    ipa_map = {}
    desc_map = {}
    """
        Build lookup maps for each phoneme rule so we can access transcription,
        IPA symbol and description in O(1) time during dictionary compilation.

        Example rule:
        {
            "AA0": {
                "transcription": "a",
                "description": "normal pronunciation of Spanish a",
                "ipa": "ɑ"
            }
        }

        Becomes three lookup tables:
        trans_map: {"AA0": "a"}
        ipa_map: {"AA0": "ɑ"}
        desc_map: {"AA0": "/ɑ/: normal pronunciation of Spanish a"}
    """
    for phoneme, rule in transcriptions.items():
        trans_map[phoneme] = rule.get("transcription", "")
        ipa = rule.get("ipa", "")
        ipa_map[phoneme] = ipa
        desc = rule.get("description", "")
        desc_map[phoneme] = f"/{ipa}/: {desc}" if ipa and desc else "" # Only add to desc_map if there is a description

    return RuleMaps(trans_map, ipa_map, desc_map)

def parse_pronunciations(rules: RuleMaps, cmu: dict) -> dict:
    """
        Convert each CMU dictionary pronunciation into a compiled entry
        using the transcription and IPA maps created above.

        Example CMU entry:
        {
            "AN": ["AA0 N"]
        }

        Becomes:
        {
            "AN": [
                {
                    "transcription": "an",
                    "ipa": "ɑn",
                    "description": "..."
                }
            ]
        }
    """
    compiled = defaultdict(list)
    for word, prons in cmu.items():

        # Remove any parenthetical suffixes (e.g. "AN(1)" -> "AN")
        # Convert to lowercase for consistent lookup
        base_word = word.partition("(")[0].lower()  

        # Each word can have multiple pronunciations in the CMU dictionary.
        # Build one compiled entry per pronunciation.
        for pron in prons:

            phonemes = pron.split()

            transcription = []
            ipa = []
            descriptions = []
            seen = set()

            # Build transcription, IPA and descriptions for the current pronunciation
            # by iterating over its phonemes.
            for p in phonemes:

                transcription.append(rules.transcriptions.get(p, ""))
                ipa.append(rules.ipa.get(p, ""))

                desc = rules.descriptions.get(p)

                if desc and desc not in seen:
                    seen.add(desc)
                    descriptions.append(desc)

            entry = {
                "transcription": "".join(transcription),
                "ipa": "".join(ipa)
            }

            if descriptions:
                entry["description"] = ". ".join(descriptions)

            compiled[base_word].append(entry)

    return dict(compiled)

def build_dictionary():
    rules_maps = parse_rules(get_source_dict(sources["es_transcriptions"]))
    return parse_pronunciations(rules_maps, get_source_dict(sources["cmu"]))

def compile_dictionary():
    compiled = build_dictionary()
    BUILD_DIR.mkdir(exist_ok=True)
    with ES_COMPILED_DICTIONARY_PATH.open("w", encoding="utf8") as f:
        json.dump(compiled, f, ensure_ascii=False, separators=(",", ":"))

@lru_cache
def get_compiled_dictionary():
    if needs_rebuild():
        compile_dictionary()
    with ES_COMPILED_DICTIONARY_PATH.open(encoding="utf-8") as f:
        return json.load(f)