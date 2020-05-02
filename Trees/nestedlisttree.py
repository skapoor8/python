"""
    Purpose:    To create a Tree ADT using a nested list representation
    Filename:   nestedlisttree.py
    Author:     Siddharth Kapoor
    Date:       May 1, 2020
"""

class NestedListTree:

    def __init__(self, root_val):
        self.tree = [root_val, [], []]

    def get_left_child(self):
        return self.tree[1]

    def get_right_child(self):
        return self.tree[2]

    def set_root_val(self, val):
        self.tree[0] = val

    def get_root_val(self):
        return self.tree[0]

    def insert_left(self, val):
        # check if there is left child
        # if yes
        #   remove left child and make it left child of new node
        #   insert new node as the left child of root
        # if no
        #   insert new node as left child of root
        new_tree = NestedListTree(val)
        if self.tree[1] != []:
            new_tree.tree[1] = self.tree[1]
        self.tree[1] = new_tree

        # [1 [4 [] []] []] -> insert [2 [] []]
        # left child = [2 [4 [] []] []]
        # [1 [2 [4 [] []] []] []]

    def insert_right(self, val):
        new_tree = NestedListTree(val)
        right_child = self.get_right_child()
        if right_child != []: 
            # this vs. self.tree[2] != [] vs. create a has_left_child() function
            new_tree.tree[2] = right_child
        self.tree[2] = new_tree




    def __str__(self):
        return str(self.tree)
    
    def __repr__(self):
        return self.__str__()

"""
    NOTES

    1.  Tried inserting lists instead of new NestedListTrees as children, and 
        found that the lists don't behave as NestedListTrees(). Essentially this
        is the same as creating a C++ class with one variable that's an int, and
        getting it to behave as an ordinary int. The new class might appear to 
        be a int, but it's not to C++. This distinction is easily forgotten in
        Python since variables don't have types.
        
        def __str__(self):
            result = '['
            for el in self.tree:
                result += super.__str__(el) + ', '
            result += ']'
            return result
            above

        This custom string function returns:
        '[val, NestedTreeObject at ..., NestedTreeObject at ...]'

        Essentially this is no different from  linked subtree representation.
        It should be more inefficient because of an added list access function.
    2.  Using an nested list representation might be useful in problems
        where we don't have time to create a tree, or only want to use one
        ascpect of the tree ADTs functionality

    QUESTIONS
    1.  Using pre defined functions like get_left_child() vs manipulating the 
        internal representation directly. It seems like using the function 
        supports single source of truth, but is more inefficient due to an added
        function call. It also seems more readable. Is this added cost worth the
        added readability and single source of truth?

"""


