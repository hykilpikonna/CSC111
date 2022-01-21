"""CSC111 Winter 2022 Prep 3: Programming Exercises

Instructions (READ THIS FIRST!)
===============================

This Python module contains a few functions that you should implement.
Each function represents a recursively-defined mathematical function,
corresponding to one in the starter file prep3_functions.pdf.
(You do not need to modify or submit prep3_functions.pdf, but you'll
need to read it to complete this programming exercise.)

We have marked each place you need to write code with the word "TODO".
As you complete your work in this file, delete each TODO comment.

You do not need to add additional doctests. However, you should test your work carefully
before submitting it!

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2022 Mario Badr and David Liu.
"""


def formula(n: int) -> float:
    """Return the value given by Definition 1 in prep3_functions.py.

    Preconditions:
        - n >= 0

    >>> formula(0)
    4.0
    >>> formula(1) == 4 - 4/3
    True
    >>> formula(2) == 4 - 4/3 + 4/5
    True
    """
    if n == 0:
        return 4.0
    elif n > 0:
        return formula(n - 1) + ((4 * (-1) ** n) / (2 * n + 1))
    else:
        raise ValueError(f'Precondition n >= 0 is violated. (n = {n})')


def formula_multiple_args(n: int, a: float, b: float) -> float:
    """Return the value given by Definition 2 in prep3_functions.py.

    Preconditions:
        - n >= 0

    >>> formula_multiple_args(0, -1, -1)
    0.0
    >>> formula_multiple_args(1, 3, 2)
    2.0
    """
    if n == 0:
        return 0.0
    elif n > 0:
        return a * formula_multiple_args(n - 1, a, b) + b
    else:
        raise ValueError(f'Precondition n >= 0 is violated. (n = {n})')


def formula_double_recursion(n: int, m: int) -> int:
    """Return the value given by Definition 3 in prep3_functions.py.

    Preconditions:
        - n >= 0
        - m >= 0

    >>> formula_double_recursion(0, 155)
    155
    >>> formula_double_recursion(1, 1) == 3 + (2 * 1)
    True
    """
    if n == 0:
        return m
    elif n > 0:
        if m == 0:
            return 2 * formula_double_recursion(n - 1, n)
        elif m > 0:
            return 3 + formula_double_recursion(n, m - 1)
        else:
            raise ValueError(f'Precondition m >= 0 is violated. (m = {m})')
    else:
        raise ValueError(f'Precondition n >= 0 is violated. (n = {n})')


# Note: the type annotation list[int] requires that you have Python 3.9 installed!
# If you haven't upgraded already, now is an excellent time to do so (check the
# "Software Installation/Upgrading Instructions" page on Quercus).
def create_list1(n: int) -> list[int]:
    """Return the value given by Definition 4 in prep3_functions.py.

    Preconditions:
        - n >= 0

    >>> create_list1(0)
    [0]
    >>> create_list1(1)
    [0, 0, 1]
    >>> create_list1(2)
    [0, 0, 1, 0, 0, 1, 2]
    """
    if n == 0:
        return [0]
    elif n > 0:
        return 2 * create_list1(n - 1) + [n]
    else:
        raise ValueError(f'Precondition n >= 0 is violated. (n = {n})')


def create_list2(n: int, m: int) -> list:
    """Return the value given by Definition 5 in prep3_functions.py.

    Preconditions:
        - n >= 0
        - m >= 0

    TESTING NOTE: because this function makes two recursive calls instead of
    just one, it will be a lot slower than your other functions!
    We recommend testing your work with very small numbers, e.g. m, n <= 5.

    >>> create_list2(0, 155)
    [155]
    >>> create_list2(155, 0)
    [155]
    >>> create_list2(1, 1)
    [[1], [1]]
    >>> create_list2(2, 2)
    [[[2], [[1], [1]]], [[[1], [1]], [2]]]
    """
    if n == 0:
        return [m]
    elif m == 0:
        return [n]
    elif n > 0 and m > 0:
        return [create_list2(n - 1, m), create_list2(n, m - 1)]
    else:
        raise ValueError(f'Precondition (n >= 0 and m >= 0) is violated. (n = {n}, m = {m})')


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100
    })
