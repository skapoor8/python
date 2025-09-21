"""
53. Given an integer array nums, find the subarray with the largest sum, and return its sum.

Example 1:

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
Example 2:

Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.
Example 3:

Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.

Tags: Divide and Conquer, Dynamic Programming
"""


from functools import reduce

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # print('nums=', nums)
        return self.maxSubArrayDNC(nums)

    def maxSubArrayDNC(self, nums: List[int]) -> int:
        return self.maxSubArrayDNCInPlaceHelper(nums, 0, len(nums)-1)

    def maxSubArrayDNCHelper(self, nums: List[int]) -> int:
        """
            Runtime: beats ~5% 
            Space: beats ~98%
            Evidently, array slice is in place and using them requires maintaining fewer variables on callstack
        """
        # base case
        if len(nums) == 0:
            return -math.inf

        # partition
        mid_idx = len(nums) // 2
        left = nums[0:mid_idx]
        right = nums[mid_idx+1:len(nums)]
        
        # conquer
        left_pinned_max = right_pinned_max = -math.inf
        sum = 0
        for l in range(mid_idx-1, -1, -1):
            sum += nums[l]
            left_pinned_max = max(left_pinned_max, sum)
        sum = 0
        for r in range (mid_idx+1, len(nums)):
            sum += nums[r]
            right_pinned_max = max(right_pinned_max, sum)
        mid = nums[mid_idx]
        # print('left_pinned_max=', left_pinned_max, 'right_pinned_max=', right_pinned_max)
        comb_max = max(mid, mid + left_pinned_max, mid + right_pinned_max, left_pinned_max + mid + right_pinned_max)

        # divide
        left_max = self.maxSubArrayDNCHelper(left)
        right_max = self.maxSubArrayDNCHelper(right)
        # print('left=', left, 'mid=', nums[mid_idx], 'right=', right)
        # print('check left and right now', left_max, right_max, comb_max)

        return max(comb_max, left_max, right_max)

    def maxSubArrayDNCInPlaceHelper(self, nums: List[int], start: int, end: int) -> int:
        """
            Runtime: beats ~5% 
            Space: beats ~10%
        """
        # print('start=', start, 'end=', end)
        # base case
        if end < start:
            return -math.inf

        # conquer
        mid_idx = (end+start+1) // 2
        sum = left_pinned_max = right_pinned_max = 0
        for l in range(mid_idx-1, start-1, -1):
            sum += nums[l]
            left_pinned_max = max(left_pinned_max, sum)
        sum = 0
        for r in range (mid_idx+1, end+1):
            sum += nums[r]
            right_pinned_max = max(right_pinned_max, sum)
        mid = nums[mid_idx]
        # print('left_pinned_max=', left_pinned_max, 'right_pinned_max=', right_pinned_max)
        comb_max = nums[mid_idx] + left_pinned_max + right_pinned_max

        # divide
        left_max = self.maxSubArrayDNCInPlaceHelper(nums, start, mid_idx-1)
        right_max = self.maxSubArrayDNCInPlaceHelper(nums, mid_idx+1, end)
        # print('left=', nums[start:mid_idx], 'mid=', nums[mid_idx], 'right=', nums[mid_idx+1:end+1])
        # print('check left and right now', left_max, right_max, comb_max)

        return max(comb_max, left_max, right_max)
