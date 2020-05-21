"""
    Purpose:    To create a AVL Tree ADT
    Filename:   avltree.py
    Author:     Siddharth Kapoor
    Date:       May 12, 2020

    Questions:
    1.  Why do we no longer need to update the parents balance factor if a node
        is rotated around? Could there not be a situation where after rotation
        the balance factor changes from 2 to 1, or -2 to -1?
    2.  How to handle deletion with AVL Tree?
"""

class AVLTree:
        
    def __init__(self):
        self.root = None
        self.size = 0
    
    def length(self):
        return len(self)
    
    def __len__(self):
        return self.size # why not call length()

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
                self._update_balance(current_node.left_child)
        else:
            if current_node.has_right_child():
                self._put(k, v, current_node.right_child)
            else:
                current_node.right_child = TreeNode(k, v, parent=current_node)
                self.size += 1
                self._update_balance(current_node.right_child)

    def _update_balance(self, node):
        if node.balance_factor > 1 or node.balance_factor < -1:
            self._rebalance(node)
            return
        if node.parent != None:
            if node.is_left_child():
                node.parent.balance_factor += 1
            elif node.is_right_child():
                node.parent.balance_factor -= 1
            
            if node.parent.balance_factor != 0:
                self._update_balance(node.parent)
    
    def _rebalance(self, node):
        if node.balance_factor < 0:
            if node.right_child.balance_factor > 0:
                self._rotate_right(node.right_child)
                self._rotate_left(node)
            else:
                self._rotate_left(node)
        elif node.balance_factor > 0:
            if node.left_child.balance_factor < 0:
                self._rotate_left(node.left_child)
                self._rotate_right(node)
            else:
                self._rotate_right(node)
    
    def _rotate_left(self, rot_root):
        print("left rotation at", rot_root.key)
        new_root = rot_root.right_child
        rot_root.right_child = new_root.left_child
        if new_root.left_child != None:
            new_root.left_child.parent = rot_root
        new_root.parent = rot_root.parent
        if rot_root.is_root():
            self.root = new_root
        else:
            if rot_root.is_left_child():
                rot_root.parent.left_child = new_root
            else:
                rot_root.parent.right_child = new_root
        new_root.left_child = rot_root
        rot_root.parent = new_root
        rot_root.balance_factor = rot_root.balance_factor + 1 \
                                - min(new_root.balance_factor, 0)
        new_root.balance_factor = new_root.balance_factor + 1 \
                                + max(rot_root.balance_factor, 0)
    
    def _rotate_right(self, rot_root):
        print("right rotation at", rot_root.key)
        new_root = rot_root.left_child
        rot_root.left_child = new_root.right_child
        if new_root.right_child != None:
            new_root.right_child.parent = rot_root
        new_root.parent = rot_root.parent
        if rot_root.is_root():
            self.root = new_root
        else:
            if rot_root.is_left_child():
                rot_root.parent.left_child = new_root
            else:
                rot_root.parent.right_child = new_root
        new_root.right_child = rot_root
        rot_root.parent = new_root
        rot_root.balance_factor = rot_root.balance_factor - 1 \
                                - max(new_root.balance_factor, 0)
        new_root.balance_factor = new_root.balance_factor - 1 \
                                + min(rot_root.balance_factor, 0)
        

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
            if node_to_remove: # _get() should not raise errors if this way
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
                current_node.parent.balance_factor -= 1
                print("immediately after removing 13", str(self))
                self._update_balance_after_remove(current_node.parent)
                # does this delete the node from memory, it still contains references
                # to existing nodes
            else:
                current_node.parent.right_child = None
                current_node.parent.balance_factor += 1
                self._update_balance_after_remove(current_node.parent)
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
                    current_node.parent.balance_factor -= 1
                    self._update_balance_after_remove(current_node.parent)
                elif current_node.is_right_child():
                    current_node.parent.right_child = current_node.left_child
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.balance_factor += 1
                    self._update_balance_after_remove(current_node.parents)
                else:
                    current_node.replace_node_data(current_node.left_child.key,
                                        current_node.left_child.value, 
                                        current_node.left_child.left_child,
                                        current_node.left_child.right_child,
                                        current_node.balance_factor)
            else:
                if current_node.is_left_child():
                    current_node.parent.left_child = current_node.right_child
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.balance_factor -= 1
                    self._update_balance_after_remove(current_node.parent)
                elif current_node.is_right_child():
                    current_node.parent.right_child = current_node.right_child
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.balance_factor += 1
                    self._update_balance_after_remove(current_node.parent)
                else:
                    current_node.replace_node_data(current_node.right_child.key,
                                        current_node.right_child.value,
                                        current_node.right_child.left_child,
                                        current_node.right_child.right_child,
                                        current_node.balance_factor)
    
    def _update_balance_after_remove(self, node):
        if node.balance_factor > 1 or node.balance_factor < -1:
            self._rebalance(node)
            node = node.parent # the rotated node has moved down the tree
        print("after rebalance at", node.key, str(self))
        if node.balance_factor == 1 or node.balance_factor == -1:
            return
        if node.parent != None and node.balance_factor == 0:
            if node.is_left_child():
                node.parent.balance_factor -= 1
            elif node.is_right_child():
                node.parent.balance_factor += 1
            self._update_balance_after_remove(node.parent)

    def __str__(self):
        result = 'AVL{'
        for k in self:
            result += str(k) + ':' + str(self[k]) + ', '
        result += '}'
        return result
    
    def verbose_string(self):
        result = 'AVL{'
        for k in self:
            result += str(k) + ':' + str(self[k]) + ':' + \
                        str(self._get(k, self.root).balance_factor) + ', '
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
        self.balance_factor = 0
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
    
    def replace_node_data(self, key, val, lc, rc, bf):
        self.key = key
        self.value = val
        self.left_child = lc
        self.right_child = rc
        if self.has_left_child(): # why use function instead of if lc is not None ???
            self.left_child.parent = self
        if self.has_right_child():
            self.right_child.parent = self
        self.balance_factor = bf
    
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
A = AVLTree()
A[10] = 10
A[5] = 5
A[15] = 15
A[0] = 0
A[20] = 20
A[13] = 13
A[-1] = -1
print(A)
A[25] = 25
print(A)
del A[13]
print(A)
"""