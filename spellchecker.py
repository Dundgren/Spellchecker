#!/usr/bin/python3
""" Main file with SpellChecker class """

import sys
import inspect
from operator import itemgetter
# import treevizer
from trie import Trie
from errors import SearchMiss

class SpellChecker:
    """ SpellChecker class """

    _OPTIONS = {
        "1": "is_word",
        "2": "search",
        "3": "change_file",
        "4": "print_all_words",
        "5": "remove_word",
        "6": "quit"
    }

    def __init__(self):
        """ Initialize class """
        self.trie = Trie()
        self.load_words()
        self.start()


    def _get_method(self, method_name):
        """
        Uses function getattr() to dynamically get value of an attribute.
        """
        return getattr(self, self._OPTIONS[method_name])


    def _print_menu(self):
        """
        Use docstring from methods to print options for the program.
        """
        menu = ""

        for key in sorted(self._OPTIONS):
            method = self._get_method(key)
            docstring = inspect.getdoc(method)

            menu += "{choice}: {explanation}\n".format(
                choice=key,
                explanation=docstring
            )

        print(chr(27) + "[2J" + chr(27) + "[;H")
        print(menu)

    @staticmethod
    def quit():
        """ Quit the program """
        sys.exit()

    def start(self):
        """ Start method """
        while True:
            self._print_menu()
            choice = input("Enter menu selection:\n-> ")

            try:
                self._get_method(choice.lower())()
            except KeyError:
                print("Invalid choice!")

            input("\nPress any key to continue ...")

    def load_words(self, filename="tiny_frequency.txt"):
        """
        Load words to Trie from file
        """
        with open(filename) as filehandle:
            words = filehandle.readlines()

        for word in words:
            word = word.split()
            self.trie.add_word(word[0], word[1])

    def is_word(self):
        """
        Check spelling
        """
        word = input("\nWord to check: \n>>> ").lower()

        try:
            self.trie.is_word(word)
            print("Correct spelling!")
        except SearchMiss:
            print("Incorrect spelling!")

    def change_file(self):
        """
        Change file
        """
        filename = input("\nEnter filename: \n>>> ")
        self.trie = Trie()

        try:
            self.load_words(filename)
        except FileNotFoundError:
            print("File not found!")

    def print_all_words(self):
        """
        Print all words from Trie
        """
        words = self.trie.get_words(self.trie.root)
        words = words.items()
        words = sorted(words)
        for word in words:
            print(word[0], " ", word[1])

    def search(self):
        """
        Search for words using prefix
        """
        prefix = ""
        print("Enter at least 3 letters at first. Then any amount of letters.")
        print("Type 'quit' to quit")

        while True:
            prefix = prefix + input(f"\nEnter prefix: \n>>> {prefix}").lower()

            if prefix[-4:] == "quit":
                break

            if len(prefix) < 3:
                print("Enter at least 3 letters!")
                prefix = ""
                continue

            try:
                words = self.trie.search(prefix)
                words = words.items()
                words = sorted(words, key=itemgetter(1), reverse=True)

                for word, frequency in words[:10]:
                    print(word, " ", frequency)
            except SearchMiss:
                print(f"No words with prefix: {prefix}")
                prefix = ""

    def remove_word(self):
        """
        Remove word from Trie
        """
        word = input("\nWord to remove: \n>>> ").lower()

        try:
            self.trie.remove_word(word)
            print("Word removed")
        except SearchMiss:
            print("Word not found")

if __name__ == "__main__":
    SpellChecker()
