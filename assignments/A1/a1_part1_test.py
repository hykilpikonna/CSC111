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

if __name__ == '__main__':
    pytest.main(['a1_part1_test.py', '-v'])
