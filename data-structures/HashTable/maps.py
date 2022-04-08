"""
    Purpose:    To create an Unordered Map, and HashMap (linear probing and
                chaining) ADTS
    Filename:   maps.py
    Author:     Siddharth Kapoor
    Date:       April 22, 2020
"""

from collections import MutableMapping
from random import randrange
from abc import abstractmethod
from unittest import TestCase

class MapBase(MutableMapping):

    class _Item:
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v
        
        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)
        
        def __lt__(self, other):
            return self._key < other._key
        
class UnsortedTableMap(MapBase):

    def __init__(self):
        self._table = []
    
    def __getitem__(self, k):
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError('Key Error: ' + repr(k))

    def __setitem__(self, k, v):
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        self._table.append(self._Item(k, v)) 
    
    def __delitem__(self, k):
        for i in range(len(self._table)):
            if self._table[i]._key == k:
                self._table.pop(i)
                return
        raise KeyError('Key Error: ' + repr(k))
    
    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for item in self._table:
            yield item._key


class HashMapBase(MapBase):

    def __init__(self, cap=11, p=109345121):
        self._table = cap * [None]
        self._size = 0
        self._prime = p
        self._scale = 1 + randrange(p-1)
        self._shift = randrange(p)
    
    def _hash_function(self, k):
        return (hash(k)*self._scale + self._shift) % self._prime \
                % len(self._table)

    def __len__(self):
        return self._size
    
    def __getitem__(self, k):
        i = self._hash_function(k)
        return self._bucket_getitem(i, k)
    
    def __setitem__(self, k, v):
        i = self._hash_function(k)
        self._bucket_setitem(i, k, v)
        if self._size / len(self._table) > 0.5:
            self._resize(2 * len(self._table) - 1)
    
    def __delitem__(self, k):
        i = self._hash_function(k)
        self._bucket_delitem(i, k)
        self._size -= 1                             # will this execute if previous line raises KeyError
    
    def _resize(self, new_capacity):
        old_table = list(self.items())
        self._table = new_capacity * [None]
        self._size = 0
        for (k, v) in old_table:
            self[k] = v

    @abstractmethod
    def _bucket_setitem(self, i, k, v):
        pass
    
    @abstractmethod
    def _bucket_getitem(self, i, k):
        pass
    
    @abstractmethod
    def _bucket_delitem(self, i, k):
        pass

class ChainHashMap(HashMapBase):

    def _bucket_setitem(self, i, k, v):
        if self._table[i] is None:
            self._table[i] = UnsortedTableMap()
            old_size = 0
        else:
            old_size = len(self._table[i])
        self._table[i][k] = v
        if len(self._table) > old_size:
            self._size += 1

    def _bucket_getitem(self, i, k):
        bucket = self._table[i]
        if bucket is None:
            raise KeyError('Key Error: ', repr(k))
        return bucket[k]

    def _bucket_delitem(self, i, k):
        bucket = self._table[i]
        if bucket is None:
            raise KeyError('Key Error: ', repr(k))
        del bucket[k]
    
    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:
                for key in bucket:
                    yield key
    
    def __str__(self):
        result = '{\n'
        for bucket in self._table:
            if bucket is not None:
                if len(bucket) > 1:
                    result += '['
                    for (k, v) in bucket.items():
                        result += str(k) + ': ' + str(v) + ', '
                    result += '],\n'
                else:
                    for key in bucket:
                        result += str(key) + ': ' + str(bucket[key]) + ',\n'
        result += '}'
        return result

    def __repr__(self):
        return self.__str__()



            

class TestChainHashMap(TestCase):
    def test_constructor(self):
        pass
    
    def test_setitem(self):
        pass

    def test_getitem(self):
        pass
    
    def test_delitem(self):
        pass

    def test_setitem_on_existing_key(self):
        pass
    
    def test_getitem_with_nonexistent_key(self):
        pass

    def test_delitem_with_nonexistent_key(self):
        pass
    
    def test_resize(self):
        pass
    
    def test_bucket_setitem(self):
        pass

    def test_bucket_getitem(self):
        pass

    def test_bucket_delitem(self):
        pass


    
    
class ProbeHashMap(HashMapBase):
    
    _VACATED = object()
    
    def __is_available(self, i):
        return self._table[i] is None or self._table[i] is ProbeHashMap._VACATED

    def __linearprobe(self, i, k):
        """
            returns (found, next_bucket) where
            found is boolean: True if k was found, False if an empty slot was found
            next is an integer: bucket index that contains k, or next empty bucket
        """
        """
        found, next_bucket = False, i
        while not found or self._table[next_bucket] is not None:
            next_bucket = (next_bucket + 1) % len(self._table)
            if self._table[next_bucket] is not None and self._table[next_bucket]._key == k:
                found = True
        return (found, bucket)
        """

        if self.__is_available(i):
            return (False, i)
        elif self._table[i]._key == k:
            return (True, i)
        else:
            found, next_bucket, next_available = False, i, None
            while not found or self._table[next_bucket] is not None:
                next_bucket = (next_bucket + 1) % len(self._table)
                if self.__is_available(next_bucket):
                    if next_available is None:
                        next_available = next_bucket
                    if self._table[next_bucket] is None:
                        break
                elif self._table[next_bucket]._key == k:
                    found = True
            return (found, next_available)
                        

        
    def _bucket_setitem(self, i, k, v):
        found, next_available = self.__linearprobe(i, k)
        if found:
            self._table[next_available]._value = v
        else:
            self._table[next_available] = self._Item(k, v)
            self._size += 1
    
    def _bucket_getitem(self, i, k):
        found, found_at = self.__linearprobe(i, k)
        if found:
            return self._table[found_at]._value
        else:
            raise KeyError('Key Error: ', repr(k))
    
    def _bucket_delitem(self, i, k):
        found, found_at = self.__linearprobe(i, k)
        if found:
            self._table[found_at] = ProbeHashMap._VACATED
        else:
            raise KeyError('Key Error: ', repr(k))
    
    def __iter__(self):
        for i in range(len(self._table)):
            if not self.__is_available(i):
                yield self._table[i]._key
    
    def __str__(self):
        output = '{\n'
        for (k, v) in self.items():
            output+= str(k) + ': ' + str(v) + ', \n'
        output += '}\n'
        return output
    
    def __repr__(self):
        return self.__str__()