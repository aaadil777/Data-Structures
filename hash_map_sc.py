# Name: Aadil Ali
# OSU Email: aliaad@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/5/2024
# Description: Implement a HashMap data structure using separate chaining

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Insert or update a key-value pair. Resize if load factor >= 1.0.
        """
        hash = self._hash_function(key)
        if self.table_load() >= 1:
            new_capacity = self._capacity * 2
            if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)
            index = hash % new_capacity
            self.resize_table(new_capacity)
        else:
            index = hash % self._capacity
        if self._buckets[index].contains(key):
            self._buckets[index].remove(key)
        else:
            self._size += 1
        self._buckets[index].insert(key, value)


    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets.
        """
        counter = 0
        for bucket in range(0, self._buckets.length()):
            if self._buckets[bucket].length() == 0:
                counter += 1
        return counter

    def table_load(self) -> float:
        """
        Return the current load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clear the map without changing capacity.
        """
        for bucket in range(0, self._buckets.length()):
            if self._buckets[bucket].length() != 0:
                self._buckets[bucket] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash table to a new capacity. The new capacity must be a prime number,
        and all existing key/value pairs are rehashed.
        """
        if new_capacity < 1:
            return

        # Ensure the new capacity is a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create a new DynamicArray of buckets
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        # Rehash all existing key-value pairs into the new buckets
        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            for node in bucket:
                new_index = self._hash_function(node.key) % new_capacity
                new_buckets[new_index].insert(node.key, node.value)

        # Update the hash map attributes
        self._buckets = new_buckets
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """
        Return the value associated with the key, or None if not found.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index] is not None:
            if self._buckets[index].contains(key) is not None:
                return self._buckets[index].contains(key).value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Return True if the key exists, False otherwise.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        bucket = self._buckets[index]
        if bucket is not None:  # if the bucket is not none then do the following
            for item in bucket:
                if item.key == key:
                    return True
        return False

    def remove(self, key: str) -> None:
        """
        Remove a key-value pair if the key exists.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a DynamicArray of all key-value pairs.
        """
        DA = DynamicArray()
        for i in range(self._buckets.length()):
            for node in self._buckets.get_at_index(i):
                DA.append((node.key, node.value))
        return DA

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Find the mode(s) in the dynamic array and return a tuple containing:
    - A DynamicArray of the mode(s)
    - The frequency of the mode(s)
    """
    # Initialize a HashMap to track the frequency of each element
    frequency_map = HashMap()

    # Count the occurrences of each element in the DynamicArray
    for i in range(da.length()):
        element = da[i]
        if not frequency_map.contains_key(element):
            frequency_map.put(element, 1)  # Add new element with initial count of 1
        else:
            frequency_map.put(element, frequency_map.get(element) + 1)  # Increment count

    # Determine the maximum frequency and collect all elements with that frequency
    max_frequency = 0
    mode_elements = DynamicArray()

    for i in range(frequency_map.get_keys_and_values().length()):
        key, frequency = frequency_map.get_keys_and_values()[i]

        if frequency > max_frequency:
            # Update max frequency and reset the mode elements array
            max_frequency = frequency
            mode_elements = DynamicArray()
            mode_elements.append(key)
        elif frequency == max_frequency:
            # Add additional elements with the same max frequency
            mode_elements.append(key)

    return mode_elements, max_frequency

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
