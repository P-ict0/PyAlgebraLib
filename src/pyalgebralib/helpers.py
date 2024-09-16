from .config import symbols

"""
Helper functions for the main library
"""


def removeLeadingZeros(a: str) -> str:
    """
    Removes all leading zeros from a given string. The function treats the '-' character
    specially, ignoring its presence and continuing to remove zeros that appear after it.

    Parameters:
        a (str): The string from which leading zeros are to be removed.

    Returns:
        str: The modified string with all leading zeros removed, regardless of the position of '-'.
    """

    if not a:
        return "0"

    # Check if the string represents a negative number
    if a[0] == "-":
        res = "-" + a[1:].lstrip("0")
    else:
        res = a.lstrip("0")

    # If the result is an empty string, return "0"
    return res if res else "0"


def greaterOrEqual(x: str, y: str) -> bool:
    """
    Compares two strings based on a custom ordering defined in the string 'symbols'.

    Parameters:
        x (str): First string to compare.
        y (str): Second string to compare.

    Returns:
        bool: True if x is greater than or equal to y based on the 'symbols' order, False otherwise.
    """
    # Comparing by length and lexicographical order based on 'symbols'
    if len(x) > len(y):
        return True
    elif len(x) < len(y):
        return False
    else:
        # Compare character by character according to the custom order
        for i in range(len(x)):
            if symbols.index(x[i]) > symbols.index(y[i]):
                return True
            elif symbols.index(x[i]) < symbols.index(y[i]):
                return False
        # If all characters are equal
        return True


def elementaryAdd(x: str, y: str, c: str, r: int = 10) -> str:
    """
    Adds two single-character numbers and a carry character in a specified radix and returns the
    rightmost character of the result along with the carry.

    Parameters:
        x (str): The first number as a single character.
        y (str): The second number as a single character.
        c (str): The carry as a single character.
        r (int): The radix in which the addition is performed, must be between 2 and 16.
                    Default is 10.

    Preconditions:
        - `r` must be between 2 and 16.
        - `x`, `y`, and `c` must each be one character long.

    Returns:
        tuple: (result, carry)
    """

    # resulting word
    result = symbols[(symbols.index(x) + symbols.index(y) + symbols.index(c)) % r]
    # carry word
    carry = symbols[((symbols.index(x) + symbols.index(y) + symbols.index(c)) // r)]

    global addCount
    addCount += 1

    return result, carry


def elementarySub(x: str, y: str, c: str, r: int = 10) -> str:
    """
    Subtracts y and a carry c from x in a specified radix and returns the rightmost character
    of the result along with the carry.

    Parameters:
        x (str): The minuend as a single character.
        y (str): The subtrahend as a single character.
        c (str): The carry (or borrow) as a single character.
        r (int): The radix in which the subtraction is performed, must be between 2 and 16.
                    Default is 10.

    Preconditions:
        - `r` must be between 2 and 16.
        - `x`, `y`, and `c` must each be one character long.

    Returns:
        tuple: (result, carry)
    """

    # resulting word
    result = symbols[(symbols.index(x) - symbols.index(y) - symbols.index(c)) % r]
    # carry word
    carry = "1" if (symbols.index(x) - symbols.index(y) - symbols.index(c)) < 0 else "0"

    return result, carry
