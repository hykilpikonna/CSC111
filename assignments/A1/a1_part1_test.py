"""CSC111 Winter 2021 Assignment 1: Linked Lists, Part 1

Instructions (READ THIS FIRST!)
===============================

Please write your tests for Part 1 in this module. Make sure to review the assignment
instructions carefully for this part! You may find it helpful to consult this
section of the Course Notes:
https://www.teach.cs.toronto.edu/~csc110y/fall/notes/B-python-libraries/02-pytest.html

While you must include unit tests, you may also use property-based tests in your test suite.

We will *not* be running PythonTA on this file; however, you should follow good programming
design and style in this file anyway, just like you would for all other work.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 David Liu and Isaac Waller.
"""
import pytest
from a1_part1 import MoveToFrontLinkedList, SwapLinkedList, CountLinkedList


def test_all_lists_true() -> None:
    movetofront = [MoveToFrontLinkedList(range(i)) for i in range(100)]
    swap = [SwapLinkedList(range(i)) for i in range(100)]
    count = [CountLinkedList(range(i)) for i in range(100)]
    assert(all(all(x in movetofront[i] for x in range(i)) for i in range(100)))
    assert(all(all(x in swap[i] for x in range(i)) for i in range(100)))
    assert(all(all(x in count[i] for x in range(i)) for i in range(100)))


def test_all_lists_false() -> None:
    movetofront = [MoveToFrontLinkedList(range(i)) for i in range(100)]
    swap = [SwapLinkedList(range(i)) for i in range(100)]
    count = [CountLinkedList(range(i)) for i in range(100)]
    assert(all(all(x not in movetofront[i] for x in range(i, i + 100)) for i in range(100)))
    assert(all(all(x not in swap[i] for x in range(i, i + 100)) for i in range(100)))
    assert(all(all(x not in count[i] for x in range(i, i + 100)) for i in range(100)))


def generate_ordering(n: int):
    """generates a pseudorandom ordering of n integers from 0 to n-1, inclusive

    Preconditions:
        - n is prime
    """
    arr = [(2 << i) % n for i in range(1, n)]
    arr.append(0)
    assert set(arr) == set(range(n))
    return arr


def test_movetofront_mutation() -> None:
    lst = MoveToFrontLinkedList(range(101))
    arr = list(range(101))
    operations = generate_ordering(101)

    for x in operations:
        i = arr.index(x)  # find index
        arr.insert(0, arr.pop(i))  # simulate moving to front
        x in lst
        assert lst.to_list() == arr


def test_swap_mutation() -> None:
    lst = SwapLinkedList(range(101))
    arr = list(range(101))
    operations = generate_ordering(101)

    for x in operations:
        i = arr.index(x)  # find index
        if i > 0:  # simulate swapping
            temp = arr[i]
            arr[i] = arr[i - 1]
            arr[i - 1] = temp
        x in lst
        assert lst.to_list() == arr


def test_count_mutation() -> None:
    lst = CountLinkedList(generate_ordering(101))
    operations = list(range(101))

    for x in operations:
        x in lst
    assert lst.to_list() == operations

    for x in reversed(range(50)):
        x in lst
    assert lst.to_list() == list(reversed(range(50))) + list(range(50, 101))


if __name__ == '__main__':
    pytest.main(['a1_part1_test.py', '-v'])
