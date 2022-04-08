"""
    Purpose:    To create a Tree ADT using a linked recursive subtree 
                representation
    Filename:   linktree.py
    Author:     Siddharth Kapoor
    Date:       May 2, 2020
"""


class LinkTree:

    def __init__(self, root_val):
        self.key = root_val
        self.left_child = None
        self.right_child = None

    def get_root_val(self):
        return self.key

    def set_root_val(self, val):
        self.key = val
    
    def get_left_child(self):
        return self.left_child

    def get_right_child(self):
        return self.right_child
    
    def insert_left_child(self, val):
        new_tree = LinkTree(val)
        #if self.left is not None:
        #    new_tree.left = self.left
        #self.left = new_tree
        new_tree.left_child = self.left_child
        self.left_child = new_tree

    def insert_right_child(self, val):
        new_tree = LinkTree(val)
        new_tree.right_child = self.right_child
        self.right_child = new_tree
    
    def preorder_map(self, apply):
        apply(self.key)
        if self.left_child:
            self.left_child.preorder_map(apply)
        if self.right_child:
            self.right_child.preorder_map(apply)        

    def inorder_map(self, apply):
        if self.left_child:
            self.left_child.inorder_map(apply)
        apply(self.key)
        if self.right_child:
            self.right_child.inorder_map(apply)
    
    def postorder_map(self, apply):
        if self.left_child:
            self.left_child.postorder_map(apply)
        if self.right_child:
            self.right_child.postorder_map(apply)
        apply(self.key)
    
    def levelorder_map(self, apply):
        apply(self.key)
        if self.left_child:
            apply(self.left_child.key)
        if self.right_child:
            apply(self.right_child.key)
        if self.left_child:
            self.levelorder_helper(self.left_child, apply)
        if self.right_child:
            self.levelorder_helper(self.right_child, apply)
        
    @staticmethod
    def levelorder_helper(subtree, apply):
        if subtree.left_child:
            apply(subtree.left_child.key)
        if subtree.right_child:
            apply(subtree.right_child.key)
        if subtree.left_child:
            subtree.levelorder_helper(subtree.left_child, apply)
        if subtree.right_child:
            subtree.levelorder_helper(subtree.right_child, apply)

    def __str__(self):
        result = '[' + str(self.key) + ', '
        if self.left_child is None:
            result += '[], '
        else:
            result += str(self.left_child) + ', '
        if self.right_child is None:
            result += '[]]'
        else:
            result += str(self.right_child) + ']'
        return result
    
    def __repr__(self):
        return self.__str__()

l = LinkTree(1)
l.insert_left_child(4)
l.insert_left_child(2)
l.insert_right_child(7)
l.insert_right_child(3)
l1 = l.get_left_child()
l2 = l.get_right_child()
l1.insert_right_child(5)
l2.insert_left_child(6)
print(l)

printer = lambda x: print(str(x), end='')
print('preorder: ', end='')
l.preorder_map(printer)
print('')
print('inorder: ', end='')
l.inorder_map(printer)
print('')
print('postorder: ', end='')
l.postorder_map(printer)
print('')
print('levelorder: ', end='')
l.levelorder_map(printer)
print('')
