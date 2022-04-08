"""
    Purpose:    a function to implement binary search
    Filename:   binarySearch.py
    Author:     Siddharth Kapoor
    Date:       April 10, 2020
"""

"""
    Binary search algorithm search(sortedList, target)
    - Divide list into two - check if midpoint = target
    - if yes, done
    - if no,
        if target < midpoint, search(sortedList.leftHalf, target)
        else search(sortedList.rightHalf, target)     

"""

def recBinarySearch(aList, target):
    return recBinarySearchHelper(aList, 0, len(aList)-1, target)

def recBinarySearchHelper(aList, start, end, target):
    #print("recBinarySearchHelper(%s, %d, %d, %d)" % (str(aList), start, end, target))
    if end < start:
        return False
    
    mid =  (start + end) // 2
    if target == aList[mid]:
        return True
    elif target < aList[mid]:
        return recBinarySearchHelper(aList, start, mid-1, target)
    else:
        return recBinarySearchHelper(aList, mid+1, end, target)

print("TESTING REC BINARY SEARCH")
print("recBinarySearch([0, 1, 2, 3, 4], 3) is " + \
                        str(recBinarySearch([0, 1, 2, 3, 4], 3)))

print("recBinarySearch([0], 0) is " + str(recBinarySearch([0], 0)))
print("recBinarySearch([0], 1) is " + str(recBinarySearch([0], 1)))
print("recBinarySearch([1], 0) is " + str(recBinarySearch([1], 0)))
print("recBinarySearch([1,2], 1) is " + str(recBinarySearch([1,2], 1)))
print("recBinarySearch([1,2], 2) is " + str(recBinarySearch([1,2], 2)))
print("recBinarySearch([1,2], 0) is " + str(recBinarySearch([1,2], 0)))
print("recBinarySearch([1,2], 3) is " + str(recBinarySearch([1,2], 3)))


def iterBinarySearch(aList, target):
    
    start, end = 0, len(aList) - 1
    mid =  (start + end)//2
    found = False

    while start <= end and not found:
        #print("iterBinarySearchHelper(%s, %d, %d, %d, %d)" % (str(aList), start, end, mid, target))
        if aList[mid] == target:
            found = True

        elif aList[mid] < target:
            start, mid = mid + 1, (start + end) // 2
        else:
            end, mid = mid - 1, (start + end) // 2
    
    return found

print("TESTING ITR BINARY SEARCH")
print("recBinarySearch([0, 1, 2, 3, 4], 3) is " + \
                        str(iterBinarySearch([0, 1, 2, 3, 4], 3)))
print("recBinarySearch([0], 0) is " + str(iterBinarySearch([0], 0)))
print("recBinarySearch([0], 1) is " + str(iterBinarySearch([0], 1)))
print("recBinarySearch([1], 0) is " + str(iterBinarySearch([1], 0)))
print("recBinarySearch([1,2], 1) is " + str(iterBinarySearch([1,2], 1)))
print("recBinarySearch([1,2], 2) is " + str(iterBinarySearch([1,2], 2)))
print("recBinarySearch([1,2], 0) is " + str(iterBinarySearch([1,2], 0)))
print("recBinarySearch([1,2], 3) is " + str(iterBinarySearch([1,2], 3)))