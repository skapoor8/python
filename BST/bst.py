"""
    Purpose:    To create a Binary Search Tree ADT
    Filename:   bst.py
    Author:     Siddharth Kapoor
    Date:       May 6, 2020
"""

class BinarySearchTree:
    class TreeNode:
        def __init__(self, key, val, left=None, right=None, parent=None):
            self.key = key
            self.value = val
            self.left_child = left
            self.right_child = right
            self.parent = parent
        
        def has_left_child(self):
            return self.left_child
        
        def has_right_child(self):
            return self.right_child
        
        def is_left_child(self):
            return self.parent and self.parent.left_child is self # or should it be ==
        
        def is_right_child(self):
            return self.parent and self.parent.right_child is self
        
        def is_root(self):
            return parent is None # not self.parent
            # is or ==
        
        def is_leaf(self):
            return not (self.left_child or self.right_child)
            # not w/ and 
            # self.left_child is None and self.right_child is None
            # self.left_child and self.right_child

        def has_any_children(self):
            return self.left_child or self.right_child
        
        def has_both_children(self):
            return self.left_child and self.right_child
        
        def replace_node_data(self, key, val, lc, rc):
            self.key = key
            self.value = val
            self.left_child = lc
            self.right_child = rc
            if self.has_left_child(): # why use function instead of if lc is not None ???
                self.left_child.parent = self
            if self.has_right_child():
                self.right_child.parent = self
        
    def __init__(self):
        self.root = None
        self.size = 0
    
    def length(self):
        return self.size
    
    def __len__(self):
        return self.size # why not call length()

    def __iter__(self):
        pass
    
    def put(self, key, val):
        pass
    
    def get(self, key):
        pass

    def delete(self, key):
        pass

    def __getitem__(self, key):
        pass
    
    def __setitem__(self, key, val):
        pass
    
    def __contains__(self, key):
        pass
    
    def __delitem__(self, key):
        pass
    