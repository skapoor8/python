"""
    Purpose:    Make a queue ADT that supports 
    Filename:   queue.py
    Author:     Siddharth Kapoor
    Date:       April 9, 2020
"""

class Queue:
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        self.items.insert(0, item)
    
    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def __str__(self):
        return self.items.__str__()
    
    def __repr__(self):
        return self.__str__()