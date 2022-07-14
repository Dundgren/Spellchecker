# Spellchecker

A simple spellchecking program where you can read words from a file and then add, delete, search or check spelling for a word.

The words are broken up into nodes that contain a single letter, a parent node, children nodes and a stop-boolean indicating the end of a word. The spelling is checked by
traversing the node-tree letter by letter of the word given. If traversing the tree succesfully and the last letter of the given word contains a stop-value of True then
the word is considered correctly spelled.

This program was made for the Object-Oriented Python/Data structure course at BTH. It was before I knew how to design test-cases and therefore the tests in this repo are abyssmal.
