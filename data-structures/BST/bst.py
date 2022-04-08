"""
    Purpose:    To create a Binary Search Tree ADT
    Filename:   bst.py
    Author:     Siddharth Kapoor
    Date:       May 6, 2020
"""

class BinarySearchTree:
        
    def __init__(self):
        self.root = None
        self.size = 0
    
    def __len__(self):
        return self.size # why not call length()

    def length(self):
        return len(self)  

    def is_empty(self):
        return self.root is None

    def __iter__(self):
        if self.root:
            return self.root.__iter__()
        else:
            return iter(())

    
    def put(self, k, v):
        if self.root:
            self._put(k, v, self.root)
        else:
            self.root = TreeNode(k, v)
            self.size += 1

    def _put(self, k, v, current_node):
        if k == current_node.key:
            current_node.value = v
        elif k < current_node.key:
            if current_node.has_left_child():
                self._put(k, v, current_node.left_child)
            else:
                current_node.left_child = TreeNode(k, v, parent=current_node)
                self.size += 1
        else:
            if current_node.has_right_child():
                self._put(k, v, current_node.right_child)
            else:
                current_node.right_child = TreeNode(k, v, parent=current_node)
                self.size += 1

    def __setitem__(self, k, v):
        self.put(k, v)

    def get(self, k):
        if self.root:
            res = self._get(k, self.root)
            if res:              
                return res.value
            else:
                raise KeyError(k)
        else:
            raise KeyError(k)
    
    def _get(self, k, current_node):
        if current_node is None: # is not current_node better than current_node is None
            return None
        if k == current_node.key:
            return current_node
        elif k < current_node.key:
            return self._get(k, current_node.left_child) # what happens when we omit return here
        else:
            return self._get(k, current_node.right_child)

    def __getitem__(self, k):
        return self.get(k)

    def __contains__(self, k):
        if self._get(k, self.root):
            return True
        else:
            return False

    def delete(self, k):
        if self.size > 1:
            node_to_remove = self._get(k, self.root)
            if node_to_remove: 
                self._remove(node_to_remove)
                self.size -= 1
            else:
                raise KeyError(k)
        elif self.size == 1 and self.root.key == k:
            self.root = None
            self.size -= 1
        else:
            raise KeyError(k)
    
    def __delitem__(self, k):
        self.delete(k)
    
    def _remove(self, current_node):
        if current_node.is_leaf():
            if current_node == current_node.parent.left_child:
                current_node.parent.left_child = None 
                # does this delete the node from memory, it still contains references
                # to existing nodes
            else:
                current_node.parent.right_child = None
        elif current_node.has_both_children():
            successor = current_node.find_successor()
            #successor.splice_out()
            current_node.key = successor.key
            current_node.value = successor.value
            self._remove(successor)
        else:
            if current_node.has_left_child():
                if current_node.is_left_child():
                    current_node.parent.left_child = current_node.left_child
                    current_node.left_child.parent = current_node.parent
                elif current_node.is_right_child():
                    current_node.parent.right_child = current_node.left_child
                    current_node.left_child.parent = current_node.parent
                else:
                    current_node.replace_node_data(current_node.left_child.key,
                                        current_node.left_child.value, 
                                        current_node.left_child.left_child,
                                        current_node.left_child.right_child)
            else:
                if current_node.is_left_child():
                    current_node.parent.left_child = current_node.right_child
                    current_node.right_child.parent = current_node.parent
                elif current_node.is_right_child():
                    current_node.parent.right_child = current_node.right_child
                    current_node.right_child.parent = current_node.parent
                else:
                    current_node.replace_node_data(current_node.right_child.key,
                                        current_node.right_child.value,
                                        current_node.right_child.left_child,
                                        current_node.right_child.right_child)

    def __str__(self):
        result = 'BST{'
        for k in self:
            result += str(k) + ':' + str(self[k]) + ', '
        result += '}'
        return result
    
    def __repr__(self):
        return self.__str__()

    def print_pretty(self):
        #   a function that prints or returns a verbose string representation 
        #   of the tree
        pass

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
        return self.parent is None
    
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
    
    def __iter__(self):
        if self:
            if self.left_child:
                for node in self.left_child:
                    yield node
            yield self.key
            if self.right_child:
                for node in self.right_child:
                    yield node
    
    def find_successor(self):
        successor = None
        if self.has_right_child():
            successor = self.right_child._find_subtree_min()
        elif self.is_left_child():
            successor = self.parent
        elif self.is_right_child():
            self.parent.right_child = None
            successor = self.parent.find_successor()
            self.parent.right_child = self
        return successor

    def _find_subtree_min(self):
        # find min value in subtree starting at this node
        min = self
        while min.has_left_child():
            min = min.left_child
        return min

    def splice_out(self):
        # splice out assumes that it is only being called on leaves or nodes
        # with only one child
        if self.is_leaf():
            if self.is_left_child():
                self.parent.left_child = None
            else:
                self.parent.right_child = None
        elif self.has_any_children():
            if self.has_left_child():
                if self.is_left_child():
                    self.parent.left_child = self.left_child
                else:
                    self.parent.right_child = self.left_child
                self.left_child.parent = self.parent
            else:
                if self.is_left_child():
                    self.parent.left_child = self.right_child
                else:
                    self.parent.right_child = self.right_child
                self.right_child.parent = self.parent


"""

b = BinarySearchTree()
b[10] = 10
b[5] = 5
b[15] = 15
b[3] = 3
b[6] = 6
print(b)     
del b[5]
print(b)  
del b[10]
print(b)

b = BinarySearchTree()
b.put(5,5)
b[2] = 2
print(b)
b[2] = 22
b[6] = 6
print("b[2] is", b[2])
print("Is 7 in BST?", 7 in b)
print(b)
del b[2]
print(b)

for k in b:
    print(k)

empty = BinarySearchTree()
if 3 in empty:
    print('This is unexpected.')
for k in empty:
    print('iterating empty BST')

# del empty[0]

print(b)
b[2] = 2
print(b)
b[4] = 4
b[1] = 1
b[7] = 7
print(b)

del b[7]
print(b)

b[7] = 7
del b[6]
print(b)
b[6] = 6
print(b)
del b[7]
print(b)
b[8] = 8
print(b)
del b[2]
print(b)
b[4.5] =4.5
print(b)
"""
"""
Questions:
    1.  What would be the behavior of calling __contains__ on empty tree?
        KeyError? What is idiomatic execution of contains method?

        __contains__ returns False if map does not contain the key, true
        otherwise. __getitem__ returns KeyError if map does not have the key.
        This is as per Python 3's map ADT spec.

    2.  What would be the behavior of iterating through empty BST?

        As per map ADT, there should be no iteration. In linked structures that
        internally use nodes, the class __iter__() function that calls the 
        node's __iter__() function can return an empty iterable object iter(())
        since the node's iterator will never be accessed

        Alternately, the data structure class can implement the iterator instead
        of relying on the node class to do so


    3.  Can something that is still referred to by a variable be deleted, 
        like a node in a tree that is still referred to by a variable outside 
        the class?

        As long as there is an active reference to the object, the object will 
        persist in memory. This is why it is good to have some idiomatic way
        of indicating that a node has been deleted, like setting a node 
        attribute or making self.parent = self

    4.  What are other ways to implement a BST? Other patterns? It might take
        time to figure that out

        Look at other implementations

    5.  There is a lot of repeated code here. Could we use functions to reduce
        the probablity of errors on updates? Would this badly affect 
        performance?

        Readability is the first priority, so avoiding duplication is good.

    6.  Is it possible for right subtree of a node to contain values smaller
        than it due to rotation?

        No, deeper nodes in a BST are added after nodes above them. This ensures
        that right subtree can only contain values greater than the parent
        node. Rotation is executed to preserve this invariant, so this should
        be the case even after rotations.

    7.  What are the invariants for a binary tree?
            -   right child is greater than node, left child is smaller
            -   inorder nodes are sorted
    
    8.  Are getters and setter the pythonic way of doing things? In C++
        data is made private for encapsulation. But not in python.

        Look at OOP Patterns in python. A good resource could be the book
        Effective Python

    9.  Why doesn't replace_node_data() change parent reference?

        Unclear
"""