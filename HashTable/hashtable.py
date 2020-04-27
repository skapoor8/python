"""
    Purpose:    Implement a HashTable ADT  
    Filename:   hashTable.py
    Author:     Siddharth Kapoor
    Date:       April 16, 2020
"""
import unittest

"""
Questions
    1. do all keys need to be rehashed on resize?
    2. 2 parallel array vs single array representation?
    3. does rehash need to be a separate function?
    4. how to support non-numeric keys?
    5. how to implement a universal hash function
    6. HOW TO UNIT TEST THIS DATA STRUCTURE?
    7. how should missing keys be handled? (del and get)
    8. how to make __iter__ and contains
"""

class HashTable:
    """
        Simple hash map implementation with linear probing
    """
    def __init__(self):
        self.capacity = 11
        self.size = 0
        self.loadFactor = 0.5
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
    
    def hashfunction(self, key):
        return key % self.capacity
    
    def rehash(self, oldHash):
        return (oldHash + 1) % self.capacity
    
    def put(self, key, val):
        if self.size/self.capacity > self.loadFactor:
            self.resize()

        hashVal = self.hashfunction(key)
        
        while self.keys[hashVal] != None and self.keys[hashVal] != key:
            hashVal = self.rehash(hashVal)
        
        if self.keys[hashVal] == None:
            self.keys[hashVal] = key
            self.values[hashVal] = val
            self.size += 1
        else:
            self.values[hashVal] = val
    
    def get(self, key):
        hashVal = self.hashfunction(key)

        while self.keys[hashVal] != key and self.keys[hashVal] != None:
            hashVal = self.rehash(hashVal)

        if self.keys[hashVal] == None:
            return None
        else:
            return self.values[hashVal]

    def __len__(self):
        print("HashTable.__len__() called")
        return self.size

    def resize(self):
        print("HashTable.resize() called")
        oldKeys, oldVals = self.keys, self.values

        self.capacity *= 2
        self.keys, self.values = [None] * self.capacity, [None] * self.capacity
        self.size = 0

        for key, val in zip(oldKeys, oldVals):
            if key != None:
                self.put(key, val)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, val):
        self.put(key, val)

    def __delitem__(self, key):
        hashVal = self.hashfunction(key)

        while self.keys[hashVal] != key and self.keys[hashVal] != None:
            hashVal = self.rehash(hashVal)

        if self.keys[hashVal] != None:
            self.keys[hashVal] = None
            self.size -= 1

    def __str__(self):
        hashString = "{\n"
        for key, val in zip(self.keys, self.values):
            if key != None:
                hashString += str(key) + ": " + str(val) + ",\n"
        hashString += "}\n"
        return hashString
    
    def __repr__(self):
        return self.__str__()

class TestHashTable(unittest.TestCase):
    def test_constructor(self):
        aTable = HashTable()
        self.assertEqual(aTable.__str__(), "{\n}\n")

myTable = HashTable()
myTable.put(1, "A")
myTable.put(11, "K")
myTable.put(22, "V")
myTable.put(3, "C")
myTable[4] = "D"
myTable[5] = "E"
print(len(myTable))
print(myTable)
myTable[6] = "F"
print(len(myTable))
print(myTable)
myTable[7] = "G"
print(myTable.get(1))
print(myTable[3])
print(myTable)

print("before deletion, len = ", str(len(myTable)))
del myTable[11]
print("after deletion, len = ", str(len(myTable)))
print(myTable)