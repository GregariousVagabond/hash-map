# Author: Leon Samuel
# Date: May 28, 2020
# Description: Implementing a hash map with chaining

# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================


class SLNode: #for storing individual links during collisions
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value) #creates node object to place in linked list
        new_node.next = self.head #assigning current head node to newly created node's next
        self.head = new_node
        self.size = self.size + 1 #increase linked list size, and put() from hash class will increase hash map size

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key): #the function for getting the placment on the hash_map
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList()) #appends a linked list item with a size 0 and head None
        self.capacity = capacity
        self._hash_function = function
        self.size = 0



    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """

        for bucket in self._buckets:  # clears each bucket individually
            if bucket.head is not None:  # node present in bucket
                self.size -= bucket.size  # reduce hash map size by bucket size before emptying bucket
                bucket.size = 0  # resets bucket size to 0
                bucket.head = None  # changes head to None, which means python will remove unreachable nodes

        """
        #not ideal, but was running into an issue of a sizing value being incorrect, tried to more manually code clear
        #ended up being that I was resizing the node.size and not the bucket.size 
        for bucket in self._buckets:
            node = bucket.head
            if bucket.head is not None:
                while node is not None:
                    node = node.next
                    bucket.remove(node)
                    self.size -= bucket.size
                bucket.size = 0
        return
        """

        """
        #manually coded bucket information and size of table to ensure they are all cleared 
        for bucket in self._buckets:
            #node = bucket.head
            print(bucket.size)
            if bucket.head is not None:
                while node is not None:
                    node = node.next
                    bucket.remove(node)
                    self.size -= bucket.size
    
            print("hash table size, ",self.size)
        return
        """

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """

        value = None
        for bucket in self._buckets:
            if bucket.contains(key) is not None: #returns none or the found node
                value = bucket.contains(key)

        if value is None:
            return value
        return value.value

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """

        prev_buckets = self._buckets #storing array copy into new variable

        self._buckets = [] #reset to blank array for resizing
        self.size = 0 #reset to 0 size for resizing
        self.capacity = capacity  # assigning new capacity

        for i in range(capacity): #creating new blank resized hash table
            self._buckets.append(LinkedList())

        for bucket in prev_buckets: #reassigning buckets and nodes into new hash table
            if bucket.head is not None:
                node = bucket.head
                while node is not None:
                    self.put(node.key,node.value)
                    node = node.next
        return

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """

        place = self._hash_function(key) % self.capacity #uses hash function and capacity to determine node's bucket

        if self._buckets[place].contains(key) is None: #if this is the first time the key is being placed
            self._buckets[place].add_front(key, value) #add node to front of linked list
            self.size = self.size + 1 #increases size of hash map, add_front will increase size of key's bucket
            return
        else: #if key already exists, this will update the value of the key
            self._buckets[place].contains(key).value = value #locates bucket, returns node with key, updates node's value
            return



    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """

        for bucket in self._buckets: #checking each bucket for the key node to remove
            if bucket.contains(key) is not None: #returns none or the found node
                if bucket.head.key == key: #if head is the node to remove
                    self.size -= 1
                    bucket.head = bucket.head.next #makes head the next node, even if it is None
                    return
                node = bucket.head #head is not key at this point, will search other nodes
                while node is not None: #will exit and simply return if no key is found
                    if node.next.key == key: #finding here to skip over next node
                        node.next = node.next.next
                        self.size -= 1
                        return
                    node = node.next #goes to next node if node.next does not contain key
        return


    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """

        if self._buckets == []: #save search time
            return False

        value = None #saving value since linkedlists contains() returns the node, making boolean difficult
        for bucket in self._buckets:
            if bucket.contains(key) is not None:
                value = bucket.contains(key) #stores node that has key or None

        if value is None:
            return False
        return True

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """

        counter = 0
        for i in self._buckets:
            if i.size == 0: #bucket is empty
                counter += 1

        return counter


    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        #items in table divided by container size
        #average number of elements in each bucket

        num_of_elements = 0

        for i in self._buckets:
            if i.head is not None: #bucket has at least 1 item
                num_of_elements += 1
                cur = i.head
                while cur.next is not None:
                    cur = cur.next
                    num_of_elements += 1


        load_factor = num_of_elements / self.capacity

        return load_factor



    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out

    @property
    def buckets(self):
        return self._buckets

    @property
    def hash_function(self):
        return self._hash_function


"""
#num of empty_buckets
m = HashMap(100, hash_function_1)
print(m.empty_buckets(), m.size, m.capacity)
m.put('key1', 10)
print(m.empty_buckets(), m.size, m.capacity)
m.put('key2', 20)
print(m.empty_buckets(), m.size, m.capacity)
m.put('key1', 30)
print(m.empty_buckets(), m.size, m.capacity)
m.put('key4', 40)
print(m.empty_buckets(), m.size, m.capacity)
"""

"""
#table_load
m = HashMap(100, hash_function_1)
print(m.table_load())
m.put('key1', 10)
print(m.table_load())
m.put('key2', 20)
print(m.table_load())
m.put('key1', 30)
print(m.table_load())


m = HashMap(50, hash_function_1)
for i in range(50):
    m.put('key' + str(i), i * 100)
    if i % 10 == 0:
        print(m.table_load(), m.size, m.capacity)
"""

"""
#clear buckets
m = HashMap(100, hash_function_1)
print(m.size, m.capacity) #0 100
m.put('key1', 10)
m.put('key2', 20)
m.put('key1', 30)
print(m.size, m.capacity) #2 100
m.clear()
print(m.size, m.capacity) #0 100



m = HashMap(50, hash_function_1)
print(m.size, m.capacity)
m.put('key1', 10)
print(m.size, m.capacity)
m.put('key2', 20)
print(m.size, m.capacity)
m.resize_table(100)
print(m.size, m.capacity)
m.clear()
print(m.size, m.capacity)
"""
"""
#put - update key with new value or add key/value if not in bucket
m = HashMap(50, hash_function_1)
for i in range(150):
    m.put('str' + str(i), i * 100)
    if i % 25 == 24:
        print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
'''
Output:
39 0.5 25 50
37 1.0 50 50
35 1.5 75 50
32 2.0 100 50
30 2.5 125 50
30 3.0 150 50
'''
"""
"""
#contains_key - returns true if key is in hash map 
m = HashMap(50, hash_function_1)
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

m = HashMap(75, hash_function_2)
keys = [i for i in range(1, 1000, 20)]
for key in keys:
    m.put(str(key), key * 42)
print(m.size, m.capacity)
result = True
for key in keys:
    # all inserted keys must be present
    result = result and m.contains_key(str(key))
    # all NOT inserted keys must be absent
    result = result and not m.contains_key(str(key + 1))
print(result)
'''
Output:
False
True
False
True
True
False

Output:
50 75
True
'''
"""
"""
m = HashMap(30, hash_function_1)
print(m.get('key'))
m.put('key1', 10)
print(m.get('key1'))

m = HashMap(150, hash_function_2)
for i in range(200, 300, 7):
    m.put(str(i), i * 10)
print(m.size, m.capacity)
for i in range(200, 300, 21):
    print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
'''
Output:
None
10

Output:
15 150
200 2000 True
201 None False
221 2210 True
222 None False
242 2420 True
243 None False
263 2630 True
264 None False
284 2840 True
285 None False
'''
"""
"""
#remove
m = HashMap(50, hash_function_1)
print(m.get('key1')) #none since none
m.put('key1', 10)
print(m.get('key1')) #10 since 10 is there
m.remove('key1')
print(m.get('key1'))
m.remove('key4')
'''
Output:
None
10
None
'''
"""
"""
#resize_table - pass which capacity to change the internal hash table to and rehash links in current table
m = HashMap(20, hash_function_1)
m.put('key1', 10)
print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
m.resize_table(30)
print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

m = HashMap(75, hash_function_2)
keys = [i for i in range(1, 1000, 13)]
for key in keys:
    m.put(str(key), key * 42)
print(m.size, m.capacity)
for capacity in range(111, 1000, 117):
    m.resize_table(capacity)
    result = True
    for key in keys:
        result = result and m.contains_key(str(key))
        result = result and not m.contains_key(str(key + 1))
    print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

'''
Output:
77 75
111 True 77 111 0.69
228 True 77 228 0.34
345 True 77 345 0.22
462 True 77 462 0.17
579 True 77 579 0.13
696 True 77 696 0.11
813 True 77 813 0.09
930 True 77 930 0.08
'''
"""