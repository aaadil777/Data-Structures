# Name: Aadil Ali
# OSU Email: aliaad@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: November 4, 2024
# Description: From SL Node, chain will be used to implement a stack class.

from SLNode import SLNode

class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass

class Stack:
    def __init__(self):
        """
        Initialize new stack with a head node.
        """
        self._head = None  # Changed from head to _head

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        """
        out = 'STACK ['
        if not self.is_empty():
            node = self._head
            out += str(node.value)
            node = node.next
            while node:
                out += ' -> ' + str(node.value)
                node = node.next
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True if the stack is empty, False otherwise
        """
        return self._head is None

    def size(self) -> int:
        """
        Return the number of elements currently in the stack
        """
        node = self._head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    def push(self, value: object) -> None:
        """
        Add a new element to the top of the stack.
        """
        node = SLNode(value)
        node.next = self._head
        self._head = node  # Update _head to the new node

    def pop(self) -> object:
        """
        Remove and return the top element from the stack.
        """
        if self.is_empty():
            raise StackException("Stack is empty")
        value = self._head.value
        self._head = self._head.next  # Update _head to the next node
        return value

    def top(self) -> object:
        """
        Return the value of the top element without removing it.
        """
        if self.is_empty():
            raise StackException("Stack is empty")
        return self._head.value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# push example 1")
    s = Stack()
    print(s)
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    print(s)


    print("\n# pop example 1")
    s = Stack()
    try:
        print(s.pop())
    except Exception as e:
        print("Exception:", type(e))
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    for i in range(6):
        try:
            print(s.pop())
        except Exception as e:
            print("Exception:", type(e))


    print("\n# top example 1")
    s = Stack()
    try:
        s.top()
    except Exception as e:
        print("No elements in stack", type(e))
    s.push(10)
    s.push(20)
    print(s)
    print(s.top())
    print(s.top())
    print(s)