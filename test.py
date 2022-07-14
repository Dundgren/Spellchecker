#!/usr/bin/env python3
""" Module for unittests """

import unittest
from errors import SearchMiss
from trie import Trie
from node import Node

class TestTrie(unittest.TestCase):
    """
    Unittests for Trie data structure
    """

    first_word = "daniel"
    first_word_sub1 = "danielle"
    first_word_sub2 = "daniellina"
    second_word = "hej"
    first_word_freq = 1
    second_word_freq = 2

    def setUp(self):
        """
        Create Trie for all tests
        """
        self.trie = Trie()

    def tearDown(self):
        """
        Reset Trie
        """
        self.trie = None

    def test_add_word(self):
        """
        Test adding a word to the Trie
        """
        trie = self.trie
        trie.add_word(self.second_word, self.second_word_freq)
        last_node = trie.get_word_stopnode(self.second_word)
        self.assertIsInstance(last_node, Node)
        self.assertEqual(last_node.value, self.second_word[-1])
        self.assertEqual(last_node.frequency, self.second_word_freq)
        self.assertTrue(last_node.stop)
        self.assertTrue(self.trie.is_word(self.second_word))

    def test_is_word(self):
        """
        Test checking the Trie for words
        """
        self.trie.add_word(self.first_word, self.first_word_freq)
        self.trie.add_word(self.first_word_sub1, self.first_word_freq)
        self.assertTrue(self.trie.is_word(self.first_word))
        self.assertTrue(self.trie.is_word(self.first_word_sub1))

    def test_is_word_searchmiss(self):
        """
        Test checking the Trie for non existing words
        """
        self.trie.add_word(self.first_word_sub1, self.first_word_freq)
        with self.assertRaises(SearchMiss) as _:
            self.trie.is_word(self.first_word)
        with self.assertRaises(SearchMiss) as _:
            self.trie.is_word(self.first_word_sub2)

    def test_search(self):
        """
        Test searching Trie using prefix
        """
        self.trie.add_word(self.first_word, self.first_word_freq)
        self.trie.add_word(self.first_word_sub1, self.first_word_freq)
        self.trie.add_word(self.first_word_sub2, self.first_word_freq)
        result = self.trie.search(self.first_word[:3])
        self.assertTrue(self.first_word in result)
        self.assertTrue(self.first_word_sub1 in result)
        self.assertTrue(self.first_word_sub2 in result)

    def test_search_searchmiss(self):
        """
        Test searching Trie using unused prefix
        """
        self.trie.add_word(self.first_word, self.first_word_freq)
        with self.assertRaises(SearchMiss) as _:
            self.trie.search(self.second_word)

    def test_remove_independent_word(self):
        """
        Test removing a word that has no prefix and is no prefix
        """
        self.trie.add_word(self.first_word, self.first_word_freq)
        self.trie.remove_word(self.first_word)
        self.assertFalse(self.first_word[0] in self.trie.root.children)
        with self.assertRaises(SearchMiss) as _:
            self.trie.is_word(self.first_word)

    def test_remove_prefix_word(self):
        """
        Test removing a word that is a prefix
        """
        self.trie.add_word(self.first_word, self.first_word_freq)
        self.trie.add_word(self.first_word_sub1, self.first_word_freq)
        self.trie.remove_word(self.first_word)
        self.assertTrue(self.trie.is_word(self.first_word_sub1))
        with self.assertRaises(SearchMiss) as _:
            self.trie.is_word(self.first_word)

    def test_remove_shared_word(self):
        """
        Test removing a word that shares a prefix with another word
        """
        self.trie.add_word(self.first_word, self.first_word_freq)
        self.trie.add_word(self.first_word_sub1, self.first_word_freq)
        self.trie.add_word(self.first_word_sub2, self.first_word_freq)
        self.trie.remove_word(self.first_word_sub1)
        self.assertTrue(self.trie.is_word(self.first_word_sub2))
        with self.assertRaises(SearchMiss) as _:
            self.trie.is_word(self.first_word_sub1)

    def test_remove_non_word(self):
        """
        Test removing a word that is not in Trie
        """
        self.trie.add_word(self.first_word, self.first_word_freq)
        with self.assertRaises(SearchMiss) as _:
            self.trie.remove_word(self.second_word)

    def test_get_all_words(self):
        """
        Test getting all words from trie. (Starting from root.)
        """
        words = [self.first_word, self.first_word_sub1, self.first_word_sub2, self.second_word]
        for word in words:
            self.trie.add_word(word, self.second_word_freq)
        all_words = self.trie.get_words(self.trie.root)
        for word in words:
            self.assertTrue(word in all_words)

if __name__ == "__main__":
    unittest.main(verbosity=3)
