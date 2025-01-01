# Name: Aadil Ali
# OSU Email: aliaad@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 11/19/2024
# Description: Implement a Binary Search Tree (BST) data structure with methods for adding,
# removing, searching, and traversing nodes, while maintaining the tree's ordered properties.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value  # to store node's data
        self.left = None  # pointer to root of left subtree
        self.right = None  # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Overrides string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of BST in human-readable form using pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self.str_helper(self.root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self.str_helper(node.left, values)
        self.str_helper(node.right, values)

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Add a new value to the BST while maintaining its properties.
        """
        node = BSTNode(value)
        if self.is_empty():
            self.root = node
        else:
            cur = self.root
            while cur:
                if value < cur.value:
                    if cur.left:
                        cur = cur.left
                    else:
                        cur.left = node
                        return
                else:
                    if cur.right:
                        cur = cur.right
                    else:
                        cur.right = node
                        return

    def remove(self, value: object) -> bool:
        """
        Remove a value from the BST. Return True if successful, False if not found.
        """
        if not self.contains(value):
            return False

        def delete_node(root, key):
            """
            Helper function to delete a node from the BST.
            """
            if not root:
                return None

            if key < root.value:
                root.left = delete_node(root.left, key)
            elif key > root.value:
                root.right = delete_node(root.right, key)
            else:
                if root.left and root.right:
                    # Node with two children: Find in-order successor
                    successor = self.get_min_node(root.right)
                    root.value = successor.value
                    root.right = delete_node(root.right, successor.value)
                elif root.left:
                    return root.left
                elif root.right:
                    return root.right
                else:
                    return None
            return root

        self.root = delete_node(self.root, value)
        return True

    def get_root(self) -> BSTNode:
        """
        Returns the root of the BST.
        """
        return self.root

    def contains(self, value: object) -> bool:
        """
        Check if a value exists in the BST. Return True if found, False otherwise.
        """
        cur = self.root
        while cur:
            if cur.value == value:
                return True
            elif value < cur.value:
                cur = cur.left
            else:
                cur = cur.right
        return False

    def inorder_traversal(self) -> Queue:
        """
        Perform an inorder traversal and return the values in a queue.
        """
        result = Queue()

        def inorder(node):
            if not node:
                return
            inorder(node.left)
            result.enqueue(node.value)
            inorder(node.right)

        inorder(self.root)
        return result

    def find_min(self) -> object:
        """
        Find and return the minimum value in the BST.
        """
        if self.is_empty():
            return None
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.value

    def find_max(self) -> object:
        """
        Find and return the maximum value in the BST.
        """
        if self.is_empty():
            return None
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.value

    def is_empty(self) -> bool:
        """
        Check if the BST is empty.
        """
        return self.root is None

    def make_empty(self) -> None:
        """
        Remove all nodes from the BST, making it empty.
        """
        self.root = None

    def get_min_node(self, node: BSTNode) -> BSTNode:
        """
        Helper function to find the node with the minimum value in a subtree.
        """
        cur = node
        while cur.left:
            cur = cur.left
        return cur
# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        print('INPUT  :', tree, tree.root.value)
        tree.remove(tree.root.value)
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)