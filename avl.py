# Name: Aadil Ali
# OSU Email: aliaad@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 11/19/2024
# Description: Implement a self-balancing AVL tree with efficient insertion, deletion, and traversal.

import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Overrides string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Return content of AVL in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super().str_helper(self.root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self.root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self.root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def get_root(self) -> AVLNode:
        """
        Returns the root of the AVL tree.
        """
        return self.root

    def add(self, value: object) -> None:
        """
        Adds a new value to the AVL tree.
        Rebalances the tree after insertion if needed.
        """
        new_node = AVLNode(value)

        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            while True:
                if value < current.value:
                    if current.left is None:
                        current.left = new_node
                        new_node.parent = current
                        break
                    current = current.left
                elif value > current.value:
                    if current.right is None:
                        current.right = new_node
                        new_node.parent = current
                        break
                    current = current.right
                else:
                    # Ignore duplicate values
                    return

        # Rebalance and update heights
        self._rebalance(new_node)

    def remove(self, value: object) -> bool:
        """
        Removes a value from the AVL tree and rebalances if needed.
        Returns True if the value was removed, False otherwise.
        """
        node_to_remove = self._find_node(self.root, value)
        if not node_to_remove:
            return False

        def _remove_node(node):
            if node.left and node.right:
                # Node with two children: Replace with in-order successor
                successor = self._find_min_node(node.right)
                node.value = successor.value
                _remove_node(successor)
            elif node.left or node.right:
                # Node with one child
                child = node.left if node.left else node.right
                if node == self.root:
                    self.root = child
                    self.root.parent = None
                else:
                    if node.parent.left == node:
                        node.parent.left = child
                    else:
                        node.parent.right = child
                    child.parent = node.parent
            else:
                # Leaf node
                if node == self.root:
                    self.root = None
                else:
                    if node.parent.left == node:
                        node.parent.left = None
                    else:
                        node.parent.right = None

            # Rebalance from the parent of the removed node
            self._rebalance(node.parent)

        _remove_node(node_to_remove)
        return True

    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalances the tree starting from the given node.
        """
        while node:
            self._update_height(node)
            balance_factor = self._get_balance(node)

            if balance_factor > 1:
                if self._get_balance(node.right) < 0:
                    node.right = self._rotate_right(node.right)
                node = self._rotate_left(node)
            elif balance_factor < -1:
                if self._get_balance(node.left) > 0:
                    node.left = self._rotate_left(node.left)
                node = self._rotate_right(node)

            if node.parent is None:
                self.root = node
            node = node.parent

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Performs a left rotation on the given node.
        """
        new_root = node.right
        node.right = new_root.left
        if new_root.left:
            new_root.left.parent = node
        new_root.left = node
        new_root.parent = node.parent
        node.parent = new_root

        if new_root.parent:
            if new_root.parent.left == node:
                new_root.parent.left = new_root
            else:
                new_root.parent.right = new_root

        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Performs a right rotation on the given node.
        """
        new_root = node.left
        node.left = new_root.right
        if new_root.right:
            new_root.right.parent = node
        new_root.right = node
        new_root.parent = node.parent
        node.parent = new_root

        if new_root.parent:
            if new_root.parent.left == node:
                new_root.parent.left = new_root
            else:
                new_root.parent.right = new_root

        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height of the node based on its children.
        """
        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1
        node.height = max(left_height, right_height) + 1

    def _get_balance(self, node: AVLNode) -> int:
        """
        Returns the balance factor of the node.
        """
        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1
        return right_height - left_height

    def _find_node(self, node: AVLNode, value: object) -> AVLNode:
        """
        Finds a node with the given value.
        """
        while node:
            if value < node.value:
                node = node.left
            elif value > node.value:
                node = node.right
            else:
                return node
        return None

    def _find_min_node(self, node: AVLNode) -> AVLNode:
        """
        Finds the node with the smallest value in the subtree.
        """
        while node.left:
            node = node.left
        return node

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
