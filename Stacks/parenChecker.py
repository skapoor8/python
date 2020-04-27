"""
    Purpose:    See if all parens are properly closed in a string
                (((() ()) ()))
                vs (((())))))
    Filename:   parenChecker.py
    Author:     Siddharth Kapoor
    Date:       April 8, 2020
"""

from stack import Stack

def parenChecker(aString):
    parenStack = Stack()
    for c in aString:
        if c == '(':
            parenStack.push(c)
        elif c == ')':
            if parenStack.isEmpty():
                return False
            else:
                parenStack.pop()
        else:
            parenStack.pop()
    return True if parenStack.isEmpty() else False

print("((()))", parenChecker("((()))"))
print("((())))", parenChecker("((())))"))
print("((())", parenChecker("((())"))
print(")))", parenChecker(")))"))
print("", parenChecker(""))