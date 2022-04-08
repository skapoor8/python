"""
    Purpose:    Unit testing basics for Python 3
    Filename:   exceptions.py
    Author:     Siddharth Kapoor
    Date:       
"""
from unittest import TestCase

class SomeClass:
    def __init__(self):
        self.data = "some data"
    
    def class_method(self, new_data):
        self.data = new_data

class TestSomeClass(TestCase):
    def test_class_method:
        s = SomeClass()
        test_string = "test data"
        s.class_method(test_string)
        self.assertEqual(s.data, test_string))


if __name__ == '__main__':
    unittest.main()