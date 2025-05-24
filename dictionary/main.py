import vocab_manager
import training_mode
import testing_mode


class Menu:
    def __init__(self):
        self.options = {
            "1": ("Editing Mode", self.editing_mode),
            "2": ("Training Mode", training_mode.training_mode),
            "3": ("Testing Mode", testing_mode.testing_mode),
            "4": ("Exit", lambda: "exit")
        }

    def display(self):
        print("\n=== Vocabulary Trainer ===")
        for key, (name, _) in self.options.items():
            print(f"{key}. {name}")
        while True:
            choice = input("Choose an option (1-4): ").strip()
            if choice in self.options:
                return choice
            print("Invalid option. Enter 1-4.")

    def editing_mode(self):
        vocab = vocab_manager.VocabManager()
        edit_options = {
            "1": ("Add a word", lambda: vocab.add_word(
                input("Unit name: ").strip(),
                input("English word: ").strip(),
                input("Meaning: ").strip())),
            "2": ("Delete a word", lambda: vocab.delete_word(
                input("Unit name: ").strip(),
                input("Word to delete: ").strip())),
            "3": ("Update a word", lambda: vocab.update_word(
                input("Unit name: ").strip(),
                input("Word to update: ").strip(),
                input("New word (Enter to keep): ").strip() or None,
                input("New meaning (Enter to keep): ").strip() or None)),
            "4": ("List words in a unit", lambda: vocab.list_words(
                input("Unit name: ").strip())),
            "5": ("Back to main menu", lambda: None)
        }
        while True:
            print("\n=== Editing Mode ===")
            for key, (name, _) in edit_options.items():
                print(f"{key}. {name}")
            choice = input("Choose an option (1-5): ").strip()
            if choice in edit_options:
                edit_options[choice][1]()
                if choice == "5":
                    break
            else:
                print("Invalid option. Enter 1-5.")


def main():
    menu = Menu()
    while True:
        choice = menu.display()
        result = menu.options[choice][1]()
        if result == "exit":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
