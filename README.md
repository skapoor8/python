# Python Data Structures

The purpose of this repository is to create implementations of common data 
structures in Python 3. 

Key Notes:
* The List, Queue, Stack and Deque use the stadard Python List ABC interface. 
* The Heap, HashTable, Tree, BinarySearchTree, and AVLTree all use the Python 
Map ABC interface. 
* Testing is done with the unittest module

## List of Data Structures Implemented
1. UnorderedList
2. Queue
3. Dequeue
4. Stack
5. Heap
6. HashTable
7. Tree
8. BinarySearchTree - Fully Tested
9. AVLTree - Partially Tested

## Example Usage

To use the included classes, use the class name to construct empty data 
structures:

```python
a = AVLTree()
a[10] = 10
a[15] = 15

print(a)
# should print 'AVL{10:10, 15:15, }'
print(a.verbose_string())
# should print tree with balance factors 'AVL{10:10:-1, 15:15:0, }'


a[13] = 13
# the AVL Tree should undergo a double rotation here to stay balanced


print(a)
# should print 'AVL{10:10, 13:13, 15:15, }'
print(a.verbose_string())
# should print 'AVL{10:10:0, 13:13:0, 15:15:0, }'

```

## Running Unit Tests

To test, simply run the relevant test file. For example, to test AVL Tree,
go to the AVL Tree directory and type:

```bash
$ python3 test_avltree.py
```

## Data Structures Yet To Be Implemented
1. Red Black Tree
2. Ordered List
3. Various Graph Implementations

## TO-DO
- [ ] Finish unit testing remaining data structures
- [ ] Compile pseudocode algorithms in folders for data structures for future reference
- [ ] Clean up files - add comments, remove print stubs

## Credits
Implementations are based on Problem Solving with Data Structures and Algorithms
in Python 2e, Data Structures and Algorithms in Python 1e, CLRS 2e.