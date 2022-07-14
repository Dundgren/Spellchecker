"""
Trie class
"""

from node import Node
from errors import SearchMiss

class Trie:
    """
    Trie
    """

    def __init__(self):
        self.root = Node("")

    def add_word(self, word, frequency):
        """
        Add word to Trie
        """
        current_node = self.root

        for letter in word:
            current_node.children[letter] = current_node.children.get(letter, Node(letter))
            parent = current_node
            current_node = current_node.children[letter]
            current_node.parent = parent

        current_node.stop = True
        current_node.frequency = float(frequency)

    def is_word(self, word):
        """
        Check trie for word
        """
        current_node = self.get_word_stopnode(word)

        if not current_node.stop:
            raise SearchMiss

        return current_node.stop

    def get_word_stopnode(self, word):
        """
        Get the last node of a word
        """
        current_node = self.root
        for letter in word:
            try:
                current_node = current_node.children[letter]
            except KeyError:
                raise SearchMiss
        return current_node

    def search(self, prefix):
        """
        Search for words using prefix
        """
        last_node = self.get_word_stopnode(prefix)
        wordlist = self.get_words(last_node)
        new_wordlist = {}

        for word in wordlist:
            new_wordlist[prefix[:-1] + word] = wordlist[word]

        return new_wordlist

    def get_words(self, current_node, word=""):
        """
        get_words from given start-point
        """
        wordlist = {}
        word += current_node.value

        if current_node.stop:
            wordlist[word] = current_node.frequency

        if current_node.children:
            for letter in current_node.children:
                wordlist.update(self.get_words(current_node.children[letter], word))

        return wordlist

    def remove_word(self, word):
        """
        Remove given word from Trie
        """
        last_node = self.get_word_stopnode(word)

        if not last_node.stop:
            raise SearchMiss

        last_node.stop = False

        if not last_node.has_children():
            self._delete_leaf(last_node)

    def _delete_leaf(self, current_node):
        """
        Delete leafword
        """
        if not current_node.stop and current_node.has_parent() and not current_node.has_children():
            del current_node.parent.children[current_node.value]
            self._delete_leaf(current_node.parent)
