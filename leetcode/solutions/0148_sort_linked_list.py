"""
148. Given the head of a linked list, return the list after sorting it in ascending order.

Example 1:
Input: head = [4,2,1,3]
Output: [1,2,3,4]

Example 2:
Input: head = [-1,5,3,4,0]
Output: [-1,0,3,4,5]

Example 3:
Input: head = []
Output: []

Constraints:
The number of nodes in the list is in the range [0, 5 * 104].
-105 <= Node.val <= 105

Follow up: Can you sort the linked list in O(n logn) time and O(1) memory (i.e. constant space)?

Tags: Divide and Conquer, Two Pointers, Merge Sort, Linked List

TODO: Bottom-up iterative variation for improved memory consumption
"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return self.mergeSortBottomUp(head)

    def mergeSortBottomUp(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Bottom up merge sort
        Runtime: beats ~70%
        Memory: beats ~ 89%
        """
        if head == None:
            return head
        elif head.next == None:
            return head
        (left, right) = self.splitList(head)
        left_sorted = self.sortList(left)
        right_sorted = self.sortList(right)
        return self.merge(left_sorted, right_sorted)

    def splitList(self, head: Optional[ListNode]):
        # print('splitting list', self.getListString(head))
        if head == None:
            return (None, None)
        elif head.next == None:
            return (head, None)

        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        mid = slow.next
        slow.next = None
        # print('left=', self.getListString(head), 'right=', self.getListString(mid))
        return (head, mid)

    def merge(self, left: Optional[ListNode], right: Optional[ListNode]) -> Optional[ListNode]:
        merged = ListNode()
        itr = merged
        while left and right:
            if left.val < right.val:
                itr.next = left
                tmp = left.next
                left.next = None
                left = tmp
            else:
                itr.next = right
                tmp = right.next
                right.next = None
                right = tmp
            itr = itr.next
        if left:
            itr.next = left
        elif right:
            itr.next = right
        return merged.next
    
    def getListString(self, head):
        ar = []
        itr = head
        while itr:
            ar.append(itr.val)
            itr = itr.next
        return ar.__str__()