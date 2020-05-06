"""
    Purpose:    To create a Heap ADT
    Filename:   heap.py
    Author:     Siddharth Kapoor
    Date:       May 4, 2020
"""

class BinaryHeap:

    def __init__(self):
        self.heap_list = [0]
        self.size = 0

    def insert(self, key):
        self.heap_list.append(key)
        self.size += 1
        self._percolate_up(self.size)

    def _percolate_up(self, i):
        while (i // 2) > 0:
            if self.heap_list[i] < self.heap_list[i//2]:
                self.heap_list[i], self.heap_list[i//2] = \
                                        self.heap_list[i//2], self.heap_list[i]
            else:
                break
            i = i // 2
    
    def find_min(self):
        if self.size == 0:
            return None
        else:
            return self.heap_list[1]
    
    def delete_min(self):

        min = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.size]
        self.heap_list.pop()
        self.size -= 1
        self._percolate_down(1)
        return min
    
    def _percolate_down(self, i):
        while i * 2 <= self.size:
            mc = self._minchild(i)
            if self.heap_list[i] > self.heap_list[mc]:
                self.heap_list[i], self.heap_list[mc] = \
                            self.heap_list[mc], self.heap_list[i]
            else:
                break
            i = mc

    
    def _minchild(self, i):
        if i * 2 + 1 > self.size:
            return i * 2
        else:
            if self.heap_list[i * 2] < self.heap_list[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1
    
    def is_empty(self):
        return self.size == 0
    
    def size(self):
        return self.size
    
    def build_heap(self, list):
        pass

    def __str__(self):
        return str(self.heap_list[1:])
    
    def __repr__(self):
        return self.__str__()

"""
    Questions:

    1.  delete_min() how to handle removal from empty heap? Raise error or 
        return None? (Perhaps look at heapq implementation)
    2.  how to do return by value in Python? Isn't it dangerous to return
        a list element in case its mutable?
"""


h = BinaryHeap()
print('Is heap empty? ', str(h.is_empty()))
h.insert(3)
print(h)
h.insert(4)
h.insert(5)
print(h)
h.insert(1)
print(h)
print('Heap min:', h.find_min())
h.delete_min()
print(h)

