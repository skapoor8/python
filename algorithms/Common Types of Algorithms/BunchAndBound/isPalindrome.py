"""
    Purpose:    Check if given string is a palindrome
    Filename:   baseConverter.py
    Author:     Siddharth Kapoor
    Date:       
"""

from deque import Deque

def isPalindrome(aString):
    charDeque = Deque()
    stillEqual = True

    for c in aString.lower():
        charDeque.addFront(c)

    while charDeque.size() > 1 and stillEqual:
        frontChar = charDeque.removeFront()
        rearChar = charDeque.removeRear()
        if frontChar != rearChar:
            stillEqual = False
    
    return stillEqual

print("checking 'toot': ", isPalindrome("toot"))
print("checking 'radar': ", isPalindrome("radar"))
print("checking 'Radar': ", isPalindrome("Radar"))
print("checking 'lsdkjfskf': ", isPalindrome("lsdkjfskf"))
print("checking 't': ", isPalindrome("t"))
print("checking '': ", isPalindrome(""))



