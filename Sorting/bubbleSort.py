"""
    Purpose:    implement bubble sort on an int list
    Filename:   bubbleSort.py
    Author:     Siddharth Kapoor
    Date:       April 14, 2020

"""

"""
    ALGORITHM
    - Iterate through the list
    - If no swaps, then sorted
    - If you encounter a pair of values not in the right order, switch them

"""

def bubbleSort(aList):
    unsorted = True
    while unsorted:
        unsorted = False
        for i in range(0, len(aList)-1):
            if aList[i] > aList[i+1]:
                aList[i], aList[i+1] = aList[i+1], aList[i]
                unsorted = True

    print(aList)


bubbleSort([5,4,3,2,1])
bubbleSort([5,4,3,2,1,2,3,4,5])
bubbleSort([9,8,1,7,5,4,3,2,6])
bubbleSort([1,2,3,4,5,6,7,8])
bubbleSort([0,0,0,0])

