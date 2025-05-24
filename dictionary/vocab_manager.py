import json
import os
from typing import Dict, Optional


class VocabManager:
    VOCAB_FILE = "vocab_hebrew.json"
    _vocab: Dict = {}

    def __init__(self):
        if not VocabManager._vocab:
            VocabManager._vocab = self._load_vocab()

    def _load_vocab(self) -> Dict:
        if not os.path.exists(self.VOCAB_FILE):
            return {}
        try:
            with open(self.VOCAB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Validate and convert units to dictionaries
            for unit in list(data.keys()):  # Use list to allow deletion
                if isinstance(data[unit], dict):
                    # Ensure all entries have repeat_count
                    for word in data[unit]:
                        if "repeat_count" not in data[unit][word]:
                            data[unit][word]["repeat_count"] = 0
                    continue
                if isinstance(data[unit], list):
                    print(f"Warning: Unit '{unit}' in vocab_hebrew.json is a "
                          f"list. Converting to dictionary format.")
                    new_dict = {}
                    for item in data[unit]:
                        if not isinstance(item, dict) or \
                           "word" not in item or "meaning" not in item:
                            print(f"Skipping invalid item in unit '{unit}': "
                                  f"{item}")
                            continue
                        word = item["word"].strip().lower()
                        if word in new_dict:
                            print(f"Skipping duplicate word '{word}' in "
                                  f"unit '{unit}'.")
                            continue
                        new_dict[word] = {
                            "meaning": item["meaning"],
                            "repeat_count": 0
                        }
                    data[unit] = new_dict
                else:
                    print(f"Error: Unit '{unit}' in vocab_hebrew.json is "
                          f"invalid (got {type(data[unit])}, expected dict).")
                    del data[unit]  # Remove invalid unit
            # Save corrected data to ensure future compatibility
            self._vocab = data
            self._save_vocab()
            return data
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("Error reading vocab file. Resetting to empty vocabulary.")
            self._save_vocab()
            return {}

    def _save_vocab(self) -> None:
        try:
            with open(self.VOCAB_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._vocab, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving vocab file: {e}")

    @staticmethod
    def _clean_input(text: str) -> str:
        return text.strip().lower() if text else ""

    def add_word(self, unit: str, word: str, meaning: str) -> bool:
        unit, word, meaning = map(self._clean_input, (unit, word, meaning))
        if not (unit and word and meaning):
            print("Unit, word, and meaning cannot be empty.")
            return False
        if unit not in self._vocab:
            self._vocab[unit] = {}
        if word in self._vocab[unit]:
            print(f"Word '{word}' already exists in {unit}.")
            return False
        self._vocab[unit][word] = {"meaning": meaning, "repeat_count": 0}
        self._save_vocab()
        print(f"Added '{word}' to {unit}.")
        return True

    def delete_word(self, unit: str, word: str) -> bool:
        unit, word = map(self._clean_input, (unit, word))
        if not unit or not word:
            print("Unit and word cannot be empty.")
            return False
        if unit not in self._vocab:
            print(f"Unit '{unit}' does not exist.")
            return False
        if word not in self._vocab[unit]:
            print(f"Word '{word}' not found in {unit}.")
            return False
        confirm = input(f"Delete '{word}' from {unit}? (y/n): ")
        if confirm.strip().lower() != 'y':
            print("Deletion canceled.")
            return False
        del self._vocab[unit][word]
        if not self._vocab[unit]:
            del self._vocab[unit]
        self._save_vocab()
        print(f"Deleted '{word}' from {unit}.")
        return True

    def update_word(self, unit: str, old_word: str, new_word: Optional[str],
                    new_meaning: Optional[str]) -> bool:
        unit, old_word = map(self._clean_input, (unit, old_word))
        new_word = self._clean_input(new_word) if new_word else None
        new_meaning = self._clean_input(new_meaning) if new_meaning else None
        if not unit or not old_word:
            print("Unit and word cannot be empty.")
            return False
        if unit not in self._vocab:
            print(f"Unit '{unit}' does not exist.")
            return False
        if old_word not in self._vocab[unit]:
            print(f"Word '{old_word}' not found in {unit}.")
            return False
        if new_word and new_word != old_word and \
           new_word in self._vocab[unit]:
            print(f"Word '{new_word}' already exists in {unit}.")
            return False
        if new_word:
            self._vocab[unit][new_word] = self._vocab[unit].pop(old_word)
        if new_meaning:
            self._vocab[unit][new_word or old_word]["meaning"] = new_meaning
        self._save_vocab()
        print(f"Updated '{old_word}' in {unit}.")
        return True

    def list_words(self, unit: str) -> bool:
        unit = self._clean_input(unit)
        if not unit:
            print("Unit cannot be empty.")
            return False
        if unit not in self._vocab:
            print(f"Unit '{unit}' does not exist.")
            return False
        if not isinstance(self._vocab[unit], dict):
            print(f"Error: Unit '{unit}' data is invalid "
                  f"(got {type(self._vocab[unit])}, expected dict).")
            return False
        print(f"\nWords in {unit}:")
        for word, data in self._vocab[unit].items():
            print(f"{word}: {data['meaning']} (Repeated: "
                  f"{data['repeat_count']} times)")
        return True

    def get_units(self) -> list:
        return list(self._vocab.keys())

    def get_words(self, unit: str) -> Dict:
        unit = self._clean_input(unit)
        if not isinstance(self._vocab.get(unit, {}), dict):
            return {}
        return self._vocab.get(unit, {})

    def update_repeat_count(self, unit: str, word: str) -> bool:
        unit, word = map(self._clean_input, (unit, word))
        if unit in self._vocab and \
           isinstance(self._vocab[unit], dict) and \
           word in self._vocab[unit]:
            self._vocab[unit][word]["repeat_count"] += 1
            self._save_vocab()
            return True
        return False
