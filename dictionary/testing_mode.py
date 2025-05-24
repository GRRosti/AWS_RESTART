import vocab_manager


def testing_mode():
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
    words = vocab.get_words(unit)
    if not words:
        print(f"No words in {unit}.")
        return

    print("\nStarting Testing Mode...")
    correct, total, incorrect = 0, 0, []
    for word, data in words.items():
        total += 1
        print(f"\nWord: {word}")
        user_answer = vocab._clean_input(input("What is the meaning? "))
        if not user_answer:
            print("Answer cannot be empty.")
            incorrect.append((word, data["meaning"], user_answer))
            continue
        correct_meaning = data["meaning"].lower()
        if user_answer == correct_meaning:
            print("Correct!")
            correct += 1
        else:
            print(f"Incorrect. Correct meaning: {data['meaning']}")
            incorrect.append((word, data["meaning"], user_answer))

    score = (correct / total * 100) if total else 0
    print("\n=== Test Summary ===")
    print(f"Score: {correct}/{total} ({score:.2f}%)")
    if incorrect:
        print("\nIncorrect answers:")
        for word, correct_meaning, user_answer in incorrect:
            print(f"Word: {word}, Correct: {correct_meaning}, "
                  f"Your answer: {user_answer}")
    else:
        print("All answers correct!")
