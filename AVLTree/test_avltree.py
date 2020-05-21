from avltree import AVLTree, TreeNode
from unittest import TestCase, main

class TestTreeNode(TestCase):
    pass

class TestAVLTree(TestCase):
    def test_create_empty_AVLTree(self):
        a = AVLTree()
        self.assertEqual(str(a), 'AVL{}')
    
    def test_setitem(self):
        # CASE 1: into empty tree
        a = AVLTree()
        a[10] = 10
        self.assertEqual(a.verbose_string(), 'AVL{10:10:0, }')

        # CASE 2: Root rotation - left
        a = AVLTree()
        a[10] = 10
        a[5] = 5
        a[15] = 15
        a[13] = 13
        a[20] = 20
        self.assertEqual(a.verbose_string(), 'AVL{5:5:0, 10:10:-1, 13:13:0, 15:15:0, 20:20:0, }')
        a[25] = 25
        self.assertEqual(a.verbose_string(), 'AVL{5:5:0, 10:10:0, 13:13:0, 15:15:0, 20:20:-1, 25:25:0, }')
        
        # CASE 3: Root rotation - right
        a = AVLTree()
        a[10] = 10
        a[5] = 5
        a[15] = 15
        a[3] = 3
        a[8] = 8
        self.assertEqual(a.verbose_string(), 'AVL{3:3:0, 5:5:0, 8:8:0, 10:10:1, 15:15:0, }')
        a[2] = 2
        self.assertEqual(a.verbose_string(), 'AVL{2:2:0, 3:3:1, 5:5:0, 8:8:0, 10:10:0, 15:15:0, }')

        # CASE 4: Root rotation - right left
        a = AVLTree()
        a[10] = 10
        a[15] = 15
        self.assertEqual(a.verbose_string(), 'AVL{10:10:-1, 15:15:0, }')
        a[13] = 13
        self.assertEqual(a.verbose_string(), 'AVL{10:10:0, 13:13:0, 15:15:0, }')

        # CASE 5: Root rotation - left right
        a = AVLTree()
        a[10] = 10
        a[5] = 5
        self.assertEqual(a.verbose_string(), 'AVL{5:5:0, 10:10:1, }')
        a[8] = 8
        self.assertEqual(a.verbose_string(), 'AVL{5:5:0, 8:8:0, 10:10:0, }')

        # CASE 6: Non-Root rotation - left
        a = AVLTree()
        a[10] = 10
        a[5] = 5
        a[3] = 3
        a[8] = 8
        a[15] = 15
        a[13] = 13
        a[20] = 20
        a[18] = 18
        a[25] = 25
        self.assertEqual(a.verbose_string(), 'AVL{3:3:0, 5:5:0, 8:8:0, 10:10:-1, 13:13:0, 15:15:-1, 18:18:0, 20:20:0, 25:25:0, }')
        a[30] = 30
        self.assertEqual(a.verbose_string(), 'AVL{3:3:0, 5:5:0, 8:8:0, 10:10:-1, 13:13:0, 15:15:0, 18:18:0, 20:20:0, 25:25:-1, 30:30:0, }')

        # CASE 7: Non-Root rotation - right
        a = AVLTree()
        a[10] = 10
        a[5] = 5
        a[3] = 3
        a[8] = 8
        a[15] = 15
        a[13] = 13
        a[18] = 18
        a[12] = 12
        a[14] = 14
        self.assertEqual(a.verbose_string(), 'AVL{3:3:0, 5:5:0, 8:8:0, 10:10:-1, 12:12:0, 13:13:0, 14:14:0, 15:15:1, 18:18:0, }')
        a[11] = 11
        self.assertEqual(a.verbose_string(), 'AVL{3:3:0, 5:5:0, 8:8:0, 10:10:-1, 11:11:0, 12:12:1, 13:13:0, 14:14:0, 15:15:0, 18:18:0, }')
        
        # CASE 8: Non-Root rotation - right left
        a = AVLTree()
        a[10] = 10
        a[5] = 5
        a[3] = 3
        a[8] = 8
        a[15] = 15
        a[13] = 13
        a[20] = 20
        a[18] = 18
        a[25] = 25
        self.assertEqual(a.verbose_string(), 'AVL{3:3:0, 5:5:0, 8:8:0, 10:10:-1, 13:13:0, 15:15:-1, 18:18:0, 20:20:0, 25:25:0, }')
        a[17] = 17
        self.assertEqual(a.verbose_string(), 'AVL{3:3:0, 5:5:0, 8:8:0, 10:10:-1, 13:13:0, 15:15:0, 17:17:0, 18:18:0, 20:20:-1, 25:25:0, }')
        
        # CASE 9: Non-Root rotation - left right
        a = AVLTree()
        a[10] = 10
        a[5] = 5
        a[3] = 3
        a[8] = 8
        a[16] = 16
        a[13] = 13
        a[18] = 18
        a[12] = 12
        a[14] = 14
        self.assertEqual(a.verbose_string(), 'AVL{3:3:0, 5:5:0, 8:8:0, 10:10:-1, 12:12:0, 13:13:0, 14:14:0, 16:16:1, 18:18:0, }')
        a[15] = 15
        self.assertEqual(a.verbose_string(), 'AVL{3:3:0, 5:5:0, 8:8:0, 10:10:-1, 12:12:0, 13:13:1, 14:14:0, 15:15:0, 16:16:0, 18:18:0, }')
        
    
    def test_getitem(self):
        pass
    
    def test_delitem(self):
        # CASE 1: LEAF - no cascading deletion, left rotation
        a = AVLTree()
        a[20] = 20
        a[10] = 10
        a[30] = 30
        a[5] = 5
        a[15] = 15
        a[29] = 29
        a[40] = 40
        a[8] = 8
        a[28] = 28
        a[35] = 35
        a[50] = 50
        a[60] = 60
        self.assertEqual(a.verbose_string(), 'AVL{5:5:-1, 8:8:0, 10:10:1, 15:15:0, 20:20:-1, 28:28:0, 29:29:1, 30:30:-1, 35:35:0, 40:40:-1, 50:50:-1, 60:60:0, }')
        del a[35]
        self.assertEqual(a.verbose_string(), 'AVL{5:5:-1, 8:8:0, 10:10:1, 15:15:0, 20:20:0, 28:28:0, 29:29:1, 30:30:0, 40:40:0, 50:50:0, 60:60:0, }')
        
        # CASE 2: LEAF - no cascading deletion, right left rotation

        # CASE 3: LEAF - cascading deletion, left following by right predecessor rotation
        a = AVLTree()
        a[20] = 20
        a[10] = 10
        a[30] = 30
        a[5] = 5
        a[15] = 15
        a[29] = 29
        a[40] = 40
        a[3] = 3
        a[8] = 8
        a[13] = 13
        a[18] = 18
        a[28] = 28
        a[35] = 35
        a[50] = 50
        a[2] = 2
        a[9] = 9
        a[12] = 12
        a[14] = 14
        a[19] = 19
        a[60] = 60
        a[11] = 11
        self.assertEqual(a.verbose_string(), 'AVL{2:2:0, 3:3:1, 5:5:0, 8:8:-1, 9:9:0, 10:10:-1, 11:11:0, 12:12:1, 13:13:1, 14:14:0, 15:15:1, 18:18:-1, 19:19:0, 20:20:1, 28:28:0, 29:29:1, 30:30:-1, 35:35:0, 40:40:-1, 50:50:-1, 60:60:0, }')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        del a[35]
        self.assertEqual(a.verbose_string(), 'AVL{2:2:0, 3:3:1, 5:5:0, 8:8:-1, 9:9:0, 10:10:0, 11:11:0, 12:12:1, 13:13:1, 14:14:0, 15:15:0, 18:18:-1, 19:19:0, 20:20:-1, 28:28:0, 29:29:1, 30:30:0, 40:40:0, 50:50:0, 60:60:0, }')
        
        # CASE 4: 2 CHILDREN - no cascading deletion, right rotation
        # CASE 5: 2 CHILDREN - no cascading deletion, left right rotation
        # CASE 6: 2 CHILDREN - cascading deletion, right rotation
        # CASE 7: 2 CHILDREN ROOT DELETION 
        # CASE 8: 1 CHILD - no cascading deletion, no rotation
    
    def test_len(self):
        pass
    
    def test_is_empty(self):
        pass
    
    def test_contains(self):
        pass
    
    def test_iterator(self):
        pass
    
    def test_str(self):
        pass
    


if __name__ == '__main__':
    main()