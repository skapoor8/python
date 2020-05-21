from bst import BinarySearchTree, TreeNode
from unittest import TestCase, main

class TestTreeNode(TestCase):
    def test_create_new_node(self):
        pass
    
    def test_is_left_child(self):
        pass
    
    def test_is_right_child(self):
        pass

    def test_has_left_child(self):
        pass
    
    def test_has_right_child(self):
        pass

    def test_is_root(self):
        pass
    
    def is_leaf(self):
        pass

    def test_has_any_children(self):
        pass
    
    def test_has_both_children(self):
        pass

    def test_replace_node_data(self):
        pass
    
    def test_find_subtree_min(self):
        pass
    
    def test_spliceout(self):
        pass
    
    def test_find_successor(self):
        pass


    


class TestBinarySearchTree(TestCase):
    def test_create_empty_BST(self):
        b = BinarySearchTree()
        self.assertEqual(str(b), 'BST{}')

    def test_setitem(self):
        b = BinarySearchTree()
        # CASE 1: inserting into empty tree
        b.put(10, 10)
        self.assertEqual(str(b), 'BST{10:10, }')
        # CASE 2: inserting into non-empty tree, both right and left child
        b[15] = 15
        b[5] = 5
        self.assertEqual(str(b), 'BST{5:5, 10:10, 15:15, }')
        # CASE 3: test insert into non-root nodes
        b[3] = 3
        b[8] = 8
        b[13] = 13
        b[18] = 18
        self.assertEqual(str(b), 
                        'BST{3:3, 5:5, 8:8, 10:10, 13:13, 15:15, 18:18, }')
        # CASE 4: insert into existing keys, root and non-root
        b[15] = 150
        b[10] = 100
        self.assertEqual(str(b), 
                        'BST{3:3, 5:5, 8:8, 10:100, 13:13, 15:150, 18:18, }')
    
    def test_length(self):
        b = BinarySearchTree()
        self.assertEqual(len(b), 0)
        b[10] = 10
        self.assertEqual(len(b), 1)
        b[15] = 15
        b[5] = 5
        self.assertEqual(len(b), 3)
    
    def test_is_empty(self):
        b = BinarySearchTree()
        self.assertTrue(b.is_empty())
        b[10] = 10
        self.assertFalse(b.is_empty())

    def test_getitem(self):
        # CASE 1: get from empty tree
        b = BinarySearchTree()
        with self.assertRaises(KeyError):
            b[10]
        # CASE 2: get value stored at root
        b[10] = 100
        self.assertEqual(b[10], 100)
        # CASE 3: get values stored in left or right subtrees 
        b[5] = 50
        b[15] = 150
        b[18] = 180
        b[13] = 130
        b[3] = 30
        b[8] = 80
        b[4] = 40
        self.assertEqual(b[5], 50)
        self.assertEqual(b[10], 100)
        self.assertEqual(b[18], 180)
        self.assertEqual(b[4], 40)
        # CASE 4: get value not in non-empty tree
        with self.assertRaises(KeyError):
            b[2]
    
    def test_deleteitem(self):
        # CASE 1: delete from empty tree
        b = BinarySearchTree()
        with self.assertRaises(KeyError):
            del b[10]
        # CASE 2: delete from root
        b[10] = 100
        del b[10]
        self.assertEqual(str(b), 'BST{}')
        b[8] = 80
        b[10] = 108
        b[5] = 50
        del b[8]
        self.assertEqual(str(b), 'BST{5:50, 10:108, }')
        # CASE 3a: delete from tree body - LEAF
        b[15] = 150
        b[18] = 180
        b[13] = 130
        b[8] = 80
        b[3] = 30
        b[4] = 40
        b[9] = 90
        del b[9]
        self.assertEqual(str(b), 'BST{3:30, 4:40, 5:50, 8:80, 10:108, 13:130, 15:150, 18:180, }')
        # CASE 3b: delete from tree body - ONE CHILD
        b[9] = 90
        b[14] = 140
        b[17] = 170
        del b[3]
        del b[8]
        del b[13]
        del b[18]
        self.assertEqual(str(b), 'BST{4:40, 5:50, 9:90, 10:108, 14:140, 15:150, 17:170, }')
        b[3] = 30
        b[8] = 80
        b[13] = 130
        b[18] = 180
        self.assertEqual(str(b), 'BST{3:30, 4:40, 5:50, 8:80, 9:90, 10:108, 13:130, 14:140, 15:150, 17:170, 18:180, }')
        # CASE 3c: delete from tree body - TWO CHILDREN
        del b[5]
        del b[15]
        self.assertEqual(str(b), 'BST{3:30, 4:40, 8:80, 9:90, 10:108, 13:130, 14:140, 17:170, 18:180, }')
        # CASE 4: delete non existent value from non-empty tree
        with self.assertRaises(KeyError):
            del b[99]

    def test_contains(self):
        # CASE 1: find value in empty BST
        b = BinarySearchTree()
        self.assertFalse(3 in b)
        # CASE 2: find value at root
        b[10] = 100
        self.assertTrue(10 in b)
        # CASE 3: find value in non-root nodes
        b[15] = 150
        b[5] = 50
        b[18] = 180
        b[13] = 130
        b[3] = 30
        b[8] = 80
        self.assertTrue(5 in b)
        self.assertTrue(15 in b)
        self.assertTrue(18 in b)
        self.assertTrue(8 in b)
        # CASE 4: find non-existent value in non-empty BST
        self.assertFalse(20 in b)
    
    def test_str(self):
        # CASE 1: empty BST
        b = BinarySearchTree()
        self.assertEqual(str(b), 'BST{}')
        # CASE 2: non-empty BST
        b[10] = 100
        b[5] = 50
        b[15] = 150
        b[8] = 80
        b[13] = 130
        self.assertEqual(str(b), 'BST{5:50, 8:80, 10:100, 13:130, 15:150, }')
        pass
    
    def test_itr(self):
        # CASE 1: empty BST
        b = BinarySearchTree()
        test_string = ''
        for key in b:
            test_string += str(key)
        self.assertEqual(test_string, '')
        # CASE 2: non empty BST
        b[10] = 100
        b[5] = 50
        b[15] = 150
        b[8] = 80
        b[13] = 130
        test_string = ''
        for key in b:
            test_string += str(key)
        self.assertEqual(test_string, '58101315')
    
if __name__ == '__main__':
    main()