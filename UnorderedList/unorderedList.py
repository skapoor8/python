
class Node:
    def __init__(self, initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data
    
    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext

    def __str__(self):
        return "Node(data: " + str(self.data) + ", next: " + str(id(self.next)) + ")"
    
    def __repr__(self):
        return self.__str__()