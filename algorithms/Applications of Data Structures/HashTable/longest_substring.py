"""
Purpose:    Solve the longest substring problem 
Filename:   longest_substring.py
Author:     Siddharth Kapoor   
Date:       April 28, 2020

      Problem Description - LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS

Given a string, find the length of the longest substring without repeating 
characters.

Example 1:

Input: "abcabcbb"
Output: 3 
Explanation: The answer is "abc", with the length of 3. 
Example 2:

Input: "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
Example 3:

Input: "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3. 

Note that the answer must be a substring, "pwke" is a subsequence and not 
a substring.
"""

def lengthOfLongestSubstring(s):
        """
        :type s: str
        :rtype: int
        
        Algorithm
        1. Set max = 0
        2. For every character i in string s, find the longest
           subsequence without repetition
            - char_map = {}
            - set j = i, and load (char at j: j) into a hash table
            - for every incrememnt of j, check if new char is in table
            - if not, then increase the sliding window
            - if length of window is > max, then max = window length
        3. Return max
        
        Optimization: instead of checking every i, when a reptition is found,
        set i = j
        """
        # my solution runs faster than 20% of python solutions
        # likely because dictionary iteration is not fast and array slice is
        max_length = 0
        curr_length = 0
        sub = {}
        
        for i, ch in enumerate(s):
            #print(ch, str(i), sub)
            if ch in sub:
                #print("HERE")
                for k, v in sub.items():
                    if v < sub[ch]:
                        del sub[k]
                sub[ch] = i
                curr_length = len(sub)
            else:
                curr_length += 1
                sub[ch] = i
            max_length = max(curr_length, max_length)
        
        return max_length
        
        # this solution runs faster than 97% of python solutions
        """
        ans = 0
        sub = ''
        for char in s:
            if char not in sub:
                sub += char
                ans = max(ans, len(sub))
            else:
                cut = sub.index(char)
                sub = sub[cut+1:] + char
        return ans
        """

print(lengthOfLongestSubstring("abcabcd"))
print(lengthOfLongestSubstring("dvdf"))