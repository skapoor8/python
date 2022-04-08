"""
    Purpose:    To test my implementation of Binary Search Tree ADT
    Filename:   test_bst.py
    Author:     Siddharth Kapoor
    Date:       April 10, 2020
"""
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()
    
    def peek(self):
        return self.items[len(self.items) - 1]
    
    def length(self):
        return len(self.items)

    def isEmpty(self):
        return not self.items

    def __str__(self):
        return self.items.__str__()
    
    def __repr__(self):
        return self.__str__()
    