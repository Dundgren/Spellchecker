"""
Trienode
"""

class Node:
    """
    Trienode
    """
    def __init__(self, letter):
        self.value = letter
        self.children = {}
        self.stop = False
        self.frequency = None
        self.parent = None

    def has_parent(self):
        """
        Check if node has parent
        """
        return self.parent is not None

    def has_children(self):
        """
        Check if node has parent
        """
        return bool(self.children)
