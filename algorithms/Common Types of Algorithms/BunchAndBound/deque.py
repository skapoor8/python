"""
    Purpose: Make a deque ADT
"""

class Deque:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self, item):
        self.items.append(item)
    
    def removeFront(self):
        return self.items.pop()

    def addRear(self, item):
        self.items.insert(0, item)

    def removeRear(self):
        return self.items.pop(0)
    
    def size(self):
        return len(self.items)

    def __str__(self):
        return "REAR" + self.items.__str__() + "FRONT"

    def __repr__(self):
        return self.__str__()
