"""
23. Merge k Sorted Lists

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.


Example 1:
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted list:
1->1->2->3->4->4->5->6

Example 2:
Input: lists = []
Output: []

Example 3:
Input: lists = [[]]
Output: []
 

Constraints:
k == lists.length
0 <= k <= 104
0 <= lists[i].length <= 500
-104 <= lists[i][j] <= 104
lists[i] is sorted in ascending order.
The sum of lists[i].length will not exceed 104.

Questions:
1. Are list1 and lis2 params in merge2Lists actually altering the original ref that was passed in
"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Runtime: beats ~11%
        Memory: beats ~92%
        """
        ## merging one more list at a time
        # dummy = ListNode(-math.inf)
        # for list in lists:
        #     dummy = self.merge2Lists(dummy, list)
        # return dummy.next

        """
        Runtime: beats ~76%
        Memory: beats ~47%
        Can be improved. Wasting cycles on pruning lists, and filtering. Can just marge based on indices, and return lists[0] in the end. Can also put base case on top.
        """
        ## merging all lists in pairs
        # print(f"orig list = {list(map(lambda l: self.getListString(l), lists))}")
        while len(lists) > 1:
            for i in range(0, len(lists)-1, 2):
                print(f"merging lists[{i}] and lists[{i+1}]; length = {len(lists)}")
                lists[i] = self.merge2Lists(lists[i], lists[i+1])
                lists[i+1] = None
            # lists = list(filter(lambda l: l != None, lists))
            lists[:] = [i for i in lists if i != None]
        # print(f"final list = {list(map(lambda l: self.getListString(l), lists))}")
        return lists[0] if len(lists) > 0 else None

    
    def merge2Lists(self, list1:List[Optional[ListNode]], list2:List[Optional[ListNode]]) -> Optional[ListNode]:
        # print('list1=', self.getListString(list1), 'list2=', self.getListString(list2))
        curr = dummy = ListNode()
        if list1 == None:
            return list2
        elif list2 == None:
            return list1

        # compare nodes
        while list1 and list2:
            # print('curr=', curr)
            # insert smaller node into new list
            if list1.val < list2.val:
                curr.next = list1
                list1 = list1.next
                curr.next.next = None
            else:
                curr.next = list2
                list2 = list2.next
                curr.next.next = None
            curr = curr.next

        # attach remaining list to the tail
        if list1:
            curr.next = list1
        else:
            curr.next = list2

        return dummy.next
    
    def getListString(self, list):
        array = []
        curr = list
        while curr:
            array.append(curr.val)
            curr = curr.next
        return array.__str__()

            