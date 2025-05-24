import random
import time
import vocab_manager


def training_mode():
    vocab = vocab_manager.VocabManager()
    units = vocab.get_units()
    if not units:
        print("No units available. Add words in Editing Mode first.")
        return

    print("\nAvailable units:", ", ".join(units))
    unit = vocab._clean_input(input("Choose a unit (or 'back' to return): "))
    if unit == 'back':
        return
    if unit not in units:
        print(f"Unit '{unit}' does not exist.")
        return

    if not vocab.list_words(unit):
        return
    choice = vocab._clean_input(input(
        "Practice full unit or a range? (full/range/back): "))
    if choice == 'back':
        return
    if choice not in ['full', 'range']:
        print("Invalid choice.")
        return

    words = list(vocab.get_words(unit).keys())
    if not words:
        print(f"No words in {unit}.")
        return

    if choice == 'range':
        start_word = vocab._clean_input(input("Enter start word: "))
        end_word = vocab._clean_input(input("Enter end word: "))
        if not start_word or not end_word:
            print("Start and end words cannot be empty.")
            return
        if start_word not in words or end_word not in words:
            print("One or both words not found in unit.")
            return
        start_idx, end_idx = words.index(start_word), words.index(end_word)
        if start_idx > end_idx:
            print("Start word must come before end word.")
            return
        words = words[start_idx:end_idx + 1]

    print("\nStarting Training Mode...")
    for _ in range(7):
        random.shuffle(words)
        for word in words:
            word_data = vocab.get_words(unit).get(word)
            if not word_data or word_data["repeat_count"] >= 7:
                continue
            print(f"\nWord: {word}")
            input("Press Enter to see meaning (or wait 3 seconds)...")
            time.sleep(3)
            print(f"Meaning: {word_data['meaning']}")
            vocab.update_repeat_count(unit, word)
            input("Press Enter for next word...")
    print("Training session complete!")
