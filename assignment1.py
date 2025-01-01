# Name: Aadil Ali
# OSU Email: aliaad@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 1
# Due Date: 10/20/2024
# Description: This assignment reviews Python fundamentals by implementing StaticArray class based algorithms with
# efficient time complexity, typically O(N), using Big O notation.


import random
from static_array import *


# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------


def min_max(arr: StaticArray) -> tuple:
    """
    Return a tuple with the minimum and maximum values of the static array.
    """
    length = arr.length()
    min_value = arr.get(0)
    max_value = arr.get(0)
    for i in range(length):
        min_value = arr.get(i) if arr.get(i) < min_value else min_value
        max_value = arr.get(i) if arr.get(i) > max_value else max_value
    return (min_value, max_value)



# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------


def fizz_buzz(arr: StaticArray) -> StaticArray:
    """
    Return a new StaticArray where each element is replaced with 'fizz', 'buzz', or 'fizzbuzz' according to divisibility rules.
    """
    length = arr.length()
    result = StaticArray(length)
    for i in range(length):
        if arr.get(i) % 15 == 0:
            result.set(i, 'fizzbuzz')
        elif arr.get(i) % 3 == 0:
            result.set(i, 'fizz')
        elif arr.get(i) % 5 == 0:
            result.set(i, 'buzz')
        else:
            result.set(i, arr.get(i))
    return result



# ------------------- PROBLEM 3 - REVERSE -----------------------------------


def reverse(arr: StaticArray) -> None:
    """
    Reverse the elements of the StaticArray in place.
    """
    length = arr.length()
    mid = length // 2
    for i in range(mid):
        left = arr.get(i)
        right = arr.get(length - i - 1)
        arr.set(i, right)
        arr.set(length - i - 1, left)



# ------------------- PROBLEM 4 - ROTATE ------------------------------------


def rotate(arr: StaticArray, steps: int) -> StaticArray:
    """
    Return a new StaticArray with elements rotated by the specified number of steps.
    """
    length = arr.length()
    result = StaticArray(length)
    steps %= length
    for i in range(length):
        result.set((i + steps) % length, arr.get(i))
    return result



# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------


def sa_range(start: int, end: int) -> StaticArray:
    """
    Create a StaticArray with consecutive integers from start to end (inclusive).
    """
    length = abs(end - start) + 1
    result = StaticArray(length)
    step = 1 if start <= end else -1
    for i in range(length):
        result.set(i, start + i * step)
    return result



# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------

def is_sorted(arr: StaticArray) -> int:
    """
    Determine if an array is strictly ascending, strictly descending, or unsorted.
    Return 1 if strictly ascending, -1 if strictly descending, and 0 otherwise.
    """
    length = arr.length()

    # Handle single-element array
    if length == 1:
        return 1

    ascending = True
    descending = True

    # Loop to check the order of elements
    for i in range(1, length):
        if arr.get(i) < arr.get(i - 1):
            ascending = False
        if arr.get(i) > arr.get(i - 1):
            descending = False
        # If we find consecutive equal elements, it's neither strictly ascending nor descending
        if arr.get(i) == arr.get(i - 1):
            ascending = False
            descending = False

    # Return result based on findings
    if ascending:
        return 1
    elif descending:
        return -1
    else:
        return 0


# ------------------- PROBLEM 7 - FIND_MODE -----------------------------------


def find_mode(arr: StaticArray) -> tuple:
    """
    Return the mode (most frequent element) and its frequency in the sorted array.
    """
    length = arr.length()
    current_value = arr.get(0)
    current_frequency = 1
    mode, frequency = current_value, 1
    for i in range(1, length):
        if arr.get(i) == current_value:
            current_frequency += 1
        else:
            if current_frequency > frequency:
                mode, frequency = current_value, current_frequency
            current_value = arr.get(i)
            current_frequency = 1
    if current_frequency > frequency:
        mode, frequency = current_value, current_frequency
    return (mode, frequency)



# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------


def remove_duplicates(arr: StaticArray) -> StaticArray:
    """
    Create a new StaticArray with duplicates removed, preserving the order, with O(n) complexity.
    """
    length = arr.length()

    # If only one element, return the same array
    if length == 1:
        result = StaticArray(1)
        result.set(0, arr.get(0))
        return result

    # Initialize the result array
    result = StaticArray(length)
    result.set(0, arr.get(0))
    index = 0

    for i in range(1, length):
        if arr.get(i) != result.get(index):
            index += 1
            result.set(index, arr.get(i))

    # Resize result to the correct size based on the number of unique elements
    final_result = StaticArray(index + 1)
    for i in range(index + 1):
        final_result.set(i, result.get(i))

    return final_result


# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------


def count_sort(arr: StaticArray) -> StaticArray:
    """
    Count sort the array in non-ascending order, with O(n+k) complexity.
    """
    length = arr.length()

    # Find the min and max values using the allowed built-in functions
    min_value = arr.get(0)
    max_value = arr.get(0)
    for i in range(1, length):
        value = arr.get(i)
        if value < min_value:
            min_value = value
        if value > max_value:
            max_value = value

    count_length = max_value - min_value + 1

    # Create count array
    count_arr = StaticArray(count_length)
    for i in range(count_length):
        count_arr.set(i, 0)

    # Count the occurrences of each number
    for i in range(length):
        count_arr.set(arr.get(i) - min_value, count_arr.get(arr.get(i) - min_value) + 1)

    # Fill the result array in non-ascending order
    result = StaticArray(length)
    index = 0
    for i in range(count_length - 1, -1, -1):
        while count_arr.get(i) > 0:
            result.set(index, i + min_value)
            index += 1
            count_arr.set(i, count_arr.get(i) - 1)

    return result


# ------------------- PROBLEM 10 - SORTED SQUARES ---------------------------


def sorted_squares(arr: StaticArray) -> StaticArray:
    """
    Return a new StaticArray with the squares of the elements in non-descending order.
    """
    length = arr.length()
    result = StaticArray(length)
    left, right = 0, length - 1
    index = length - 1
    while index >= 0:
        if abs(arr.get(left)) > abs(arr.get(right)):
            result.set(index, arr.get(left) ** 2)
            left += 1
        else:
            result.set(index, arr.get(right) ** 2)
            right -= 1
        index -= 1
    return result


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]: 3}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        result = min_max(arr)
        if result:
            print(f"Min: {result[0]: 3}, Max: {result[1]}")
        else:
            print("min_max() not yet implemented")

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        space = " " if steps >= 0 else ""
        print(f"{rotate(arr, steps)} {space}{steps}")
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-95, -89), (-89, -95)]
    for start, end in cases:
        print(f"Start: {start: 4}, End: {end: 4}, {sa_range(start, end)}")

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = is_sorted(arr)
        space = "  " if result and result >= 0 else " "
        print(f"Result:{space}{result}, {arr}")

    print('\n# find_mode example 1')
    test_cases = (
        [1, 20, 30, 40, 500, 500, 500],
        [2, 2, 2, 2, 1, 1, 1, 1],
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        ["Albania", "Belgium", "Chile", "Denmark", "Egypt", "Fiji"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value

        result = find_mode(arr)
        if result:
            print(f"{arr}\nMode: {result[0]}, Frequency: {result[1]}\n")
        else:
            print("find_mode() not yet implemented\n")

    print('# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(f"Before: {arr}")
        result = count_sort(arr)
        print(f"After : {result}")

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-1_000_000_000, 1_000_000_000 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# sorted_squares example 1')
    test_cases = (
        [1, 2, 3, 4, 5],
        [-5, -4, -3, -2, -1, 0],
        [-3, -2, -2, 0, 1, 2, 3],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(sorted(case)):
            arr[i] = value
        print(arr)
        result = sorted_squares(arr)
        print(result)

    print('\n# sorted_squares example 2')
    array_size = 5_000_000
    case = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(sorted(case)):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = sorted_squares(arr)
    print(f'Finished sorting large array of {array_size} elements')
