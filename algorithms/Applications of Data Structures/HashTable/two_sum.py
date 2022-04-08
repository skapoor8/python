"""

Purpose:    Solve the two sum problem 
Filename:   two_sum.py
Author:     Siddharth Kapoor   
Date:       April 27, 2020

                    Problem Description - TWO SUM
                    
Given an array of integers, return indices of the two numbers such that they 
add up to a specific target.

You may assume that each input would have exactly one solution, and you may not 
use the same element twice.

Example:

Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
"""


def twoSum(nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]

        Algorithm: One Pass Hash
        1. Go through the list
        2. For every element,
            - if element's complement is in hash table, return index of element
              and the complement 
            - if not, put the element into the hash table (key = element, 
              val = index)
        3. At the end of the pass, if no match is found, then there is no match.
           Return [-1, -1]
        """
        
        intMap = {}
        for i in range(len(nums)):
            if target - nums[i] in intMap:
                return [i, intMap[target - nums[i]]]
            else:
                intMap[nums[i]] = i
        
        return [-1, -1]


print(twoSum([1, 2, 4, 6, 8], 8))