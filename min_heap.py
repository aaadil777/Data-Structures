# Name: Aadil Ali
# OSU Email: aliaad@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 8
# Due Date: 11/25/2024
# Description: Implement a dynamic array-backed for MinHeap data structure in Python using
# heap manipulation, including insertion, deletion, and sorting using the heapsort algorithm.


from dynamic_array import *

class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass

class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap.
        """
        self._heap = DynamicArray()

        # Populate MH with initial values (if provided)
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form.
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    def is_empty(self) -> bool:
        """
        Returns True if the heap is empty, False otherwise.
        """
        return self._heap.is_empty()

    def add(self, node: object) -> None:
        """
        Adds a new object to the MinHeap while maintaining heap property.
        """
        self._heap.append(node)
        index = self._heap.length() - 1
        while index > 0:
            parent_index = (index - 1) // 2
            if self._heap[parent_index] > node:
                self.swap(index, parent_index)
                index = parent_index
            else:
                break

    def get_min(self) -> object:
        """
        Returns the minimum key without removing it. Raises exception if the heap is empty.
        """
        if self.is_empty():
            raise MinHeapException("Heap is empty.")
        return self._heap.get_at_index(0)

    def swap(self, index1: int, index2: int) -> None:
        """
        Swaps two elements in the heap.
        """
        temp = self._heap.get_at_index(index1)
        self._heap.set_at_index(index1, self._heap.get_at_index(index2))
        self._heap.set_at_index(index2, temp)

    def remove_min(self) -> object:
        """
        Removes and returns the minimum key from the heap. Raises exception if empty.
        """
        if self.is_empty():
            raise MinHeapException("Heap is empty.")

        min_val = self.get_min()
        last_index = self._heap.length() - 1

        # Replace root with the last element and remove the last element
        self._heap.set_at_index(0, self._heap.get_at_index(last_index))
        self._heap.remove_at_index(last_index)

        # Percolate down the new root to maintain heap property
        index = 0
        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index

            if left_child < self._heap.length() and self._heap.get_at_index(left_child) < self._heap.get_at_index(smallest):
                smallest = left_child

            if right_child < self._heap.length() and self._heap.get_at_index(right_child) < self._heap.get_at_index(smallest):
                smallest = right_child

            if smallest == index:
                break

            self.swap(index, smallest)
            index = smallest

        return min_val

    def build_heap(self, da: DynamicArray) -> None:
        """
        Builds a MinHeap from the given DynamicArray.
        """
        self._heap = DynamicArray()
        for i in range(da.length()):
            self._heap.append(da[i])

        for i in range((self._heap.length() - 2) // 2, -1, -1):
            index = i
            while True:
                left_child = 2 * index + 1
                right_child = 2 * index + 2
                smallest = index

                if left_child < self._heap.length() and self._heap.get_at_index(left_child) < self._heap.get_at_index(smallest):
                    smallest = left_child

                if right_child < self._heap.length() and self._heap.get_at_index(right_child) < self._heap.get_at_index(smallest):
                    smallest = right_child

                if smallest == index:
                    break

                self.swap(index, smallest)
                index = smallest

    def size(self) -> int:
        """
        Returns the number of items currently stored in the heap.
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears the contents of the heap.
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Sorts the DynamicArray in non-ascending order using the Heapsort algorithm.
    """
    heap = MinHeap()
    heap.build_heap(da)

    for i in range(da.length() - 1, -1, -1):
        da.set_at_index(i, heap.remove_min())



# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
