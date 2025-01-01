# Name: Aadil Ali
# OSU Email: aliaad@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: November 4, 2024
# Description: Implementation of a queue class using a chain of the SL node.


from SLNode import SLNode

class QueueException(Exception):
    """
    Custom exception to be used by Queue class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass

class Queue:
    def __init__(self):
        """
        Initialize new queue with head and tail nodes
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.head = None
        self.tail = None

    def __str__(self):
        """
        Return content of queue in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'QUEUE ['
        if not self.is_empty():
            node = self.head
            out = out + str(node.value)
            node = node.next
            while node:
                out = out + ' -> ' + str(node.value)
                node = node.next
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True if the queue is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.head is None

    def size(self) -> int:
        """
        Return number of elements currently in the queue
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        node = self.head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    # -----------------------------------------------------------------------

    def enqueue(self, value: object) -> None:
        """
        Adds a new value to the end of the queue.
        """
        # Create a new node with the given value
        node = SLNode(value)
        if self.is_empty():
            # If the queue is empty, set both head and tail to the new node
            self.head = node
            self.tail = node
        else:
            # Otherwise, link the current tail to the new node and update the tail
            self.tail.next = node
            self.tail = node

    def dequeue(self) -> object:
        """
        Removes and returns the beginning value of the queue.
        """
        # If the queue is empty, raise exception
        if self.is_empty():
            raise QueueException("Queue is empty")
        # Save the first value to return
        target = self.head.value
        # Remove the first element by updating head
        self.head = self.head.next
        # If the queue is now empty, update tail to None
        if self.head is None:
            self.tail = None
        return target

    def front(self) -> object:
        """
        Returns the front value without removing the element.
        """
        # If the queue is empty, raise exception
        if self.is_empty():
            raise QueueException("Queue is empty")
        return self.head.value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# enqueue example 1")
    q = Queue()
    print(q)
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)

    print("\n# dequeue example 1")
    q = Queue()
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)
    for i in range(6):
        try:
            print(q.dequeue())
        except Exception as e:
            print("No elements in queue", type(e))

    print('\n#front example 1')
    q = Queue()
    print(q)
    for value in ['A', 'B', 'C', 'D']:
        try:
            print(q.front())
        except Exception as e:
            print("No elements in queue", type(e))
        q.enqueue(value)
    print(q)
