"""
Program to perform algebra operations using efficient algorithms.
Can operate with numbers from radix 2 to radix 16. Without converting between radix.

Supported operations:
    - Addition
    - Subtraction
    - Multiplication (Normal "primary school method" + Karatsuba algorithm)
    - Division
    - GCD of 2 numbers (Extended Euclidean algorithm)
    - Modular Arithmetic:
        - Reduction
        - Addition
        - Subtraction
        - Inversion
        - Multiplication

Author: Rodrigo Martín Núñez

Date: 2021-2024
"""

addCount = 0
mulCount = 0
symbols = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
]


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


def divide(x: str, y: str, r: int) -> str:
    """
    Divides one integer by another (both as str) and returns the quotient in the specified radix.

    Parameters:
        x (str): The dividend.
        y (str): The divisor.
        r (int): The radix in which to express the quotient. Must be between 2 and 16, inclusive.

    Preconditions:
        r must be at least 2 and no more than 16.

    Returns:
        str: The quotient of x divided by y, expressed in radix r.
    """

    q = "-1"
    while not (x[0] == "-"):
        q = add(q, "1", r)
        x = subtract(x, y, r)
    return q


def elementaryAdd(x: str, y: str, c: str, r: int) -> str:
    """
    Adds two single-character numbers and a carry character in a specified radix and returns the
    rightmost character of the result along with the carry.

    Parameters:
        x (str): The first number as a single character.
        y (str): The second number as a single character.
        c (str): The carry as a single character.
        r (int): The radix in which the addition is performed, must be between 2 and 16.

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


def elementarySub(x: str, y: str, c: str, r: int) -> str:
    """
    Subtracts y and a carry c from x in a specified radix and returns the rightmost character
    of the result along with the carry.

    Parameters:
        x (str): The minuend as a single character.
        y (str): The subtrahend as a single character.
        c (str): The carry (or borrow) as a single character.
        r (int): The radix in which the subtraction is performed, must be between 2 and 16.

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


def elementaryMult(x: str, y: str, z: str, c: str, r: int) -> str:
    """
    Multiplies two single-character numbers x and y, adds a single-character carry c,
    and the current single-character result z, all in a specified radix. Returns the
    rightmost character of the result along with the carry.

    Parameters:
        x (str): The first multiplier as a single character.
        y (str): The second multiplier as a single character.
        z (str): The current result value as a single character.
        c (str): The carry as a single character.
        r (int): The radix in which the operations are performed, must be between 2 and 16.

    Preconditions:
        - `r` must be between 2 and 16.
        - `x`, `y`, `z`, and `c` must each be one character long.

    Returns:
        tuple: (result, carry)
    """

    t = symbols.index(z) + (symbols.index(x) * symbols.index(y)) + symbols.index(c)
    # carry word
    carry = symbols[t // r]
    # resulting word
    result = symbols[t - ((t // r) * r)]

    global mulCount
    mulCount += 1

    return result, carry


def add(x: str, y: str, r: int) -> str:
    """
    Adds two numbers represented as strings in a specified radix and returns the resulting sum as a string.

    Parameters:
        x (str): The first number as a string in radix r.
        y (str): The second number as a string in radix r.
        r (int): The radix in which the numbers are expressed and the addition is performed, must be between 2 and 16.

    Preconditions:
        - `r` must be between 2 and 16.
        - Negative numbers are represented by a leading '-' character.

    Returns:
        str: result of x+y in radix r.
    """

    x = removeLeadingZeros(x)
    y = removeLeadingZeros(y)

    bothNegative = False
    # handle negative numbers
    if x[0] == "-" and y[0] == "-":
        # -x + -y = -(x + y)
        x = x[1:]
        y = y[1:]
        bothNegative = True
    elif x[0] == "-":
        # -x + y = y - x
        return subtract(y, x[1:], r)
    elif y[0] == "-":
        # x + -y = x - y
        return subtract(x, y[1:], r)

    result = ""
    carry = "0"
    # determine amount of times we need to do an elementary addition
    length = 0
    if len(x) > len(y):
        length = len(x)
        # add 0's to the front of y to make x and y have equal lengths
        y = symbols[0] * (length - len(y)) + y
    else:
        length = len(y)
        # add 0's to the front of x to make x and y have equal lengths
        x = symbols[0] * (length - len(x)) + x

    # add individual characters and store a carry
    for i in range(length):
        elemRes = elementaryAdd(x[len(x) - 1 - i], y[len(y) - 1 - i], carry, r)
        carry = elemRes[1]
        result = elemRes[0] + result

    # if there is still a carry add it to the start of the result
    if carry != symbols[0]:
        result = carry + result

    if bothNegative:
        result = "-" + result

    return removeLeadingZeros(result)


def subtract(x: str, y: str, r: int) -> str:
    """
     Subtracts two numbers represented as strings in a specified radix and returns the resulting sum as a string.

     Parameters:
         x (str): The first number as a string in radix r.
         y (str): The second number as a string in radix r.
         r (int): The radix in which the numbers are expressed and the subtraction is performed, must be between 2 and 16.

     Preconditions:
         - `r` must be between 2 and 16.
         - Negative numbers are represented by a leading '-' character.

    Returns:
         str: result of x-y in radix r.
    """

    x = removeLeadingZeros(x)
    y = removeLeadingZeros(y)

    # handle negative numbers
    if x[0] == "-" and y[0] == "-":
        # -x - -y = y - x
        return subtract(y[1:], x[1:], r)
    elif x[0] == "-":
        # -x - y = -x + -y
        return add("-" + y, x, r)
    elif y[0] == "-":
        # x - -y = x + y
        return add(x, y[1:], r)

    if not greaterOrEqual(x, y):
        return "-" + subtract(y, x, r)

    result = ""
    carry = "0"

    length = len(x)
    if len(x) > len(y):
        # add 0's to the front of y to make x and y have equal lengths
        y = symbols[0] * (length - len(y)) + y

    # subtract individual characters and store a carry
    for i in range(length):
        elemRes = elementarySub(x[len(x) - 1 - i], y[len(y) - 1 - i], carry, r)
        carry = elemRes[1]
        result = elemRes[0] + result

    return removeLeadingZeros(result)


def multiply(x: str, y: str, r: int) -> str:
    """
    Multiplies two numbers represented as strings in a specified radix and returns the product as a string.

    Parameters:
        x (str): The first number as a string, in radix r.
        y (str): The second number as a string, in radix r.
        r (int): The radix in which the numbers are expressed and the multiplication is performed, must be between 2 and 16.

    Preconditions:
        - `r` must be between 2 and 16.
        - Negative numbers are represented by a leading '-' character.

    Returns:
        str: Result of x*y in radix r.
    """

    x = removeLeadingZeros(x)
    y = removeLeadingZeros(y)

    if x[0] == "-" and y[0] == "-":
        # -x * -y = x * y
        return multiply(x[1:], y[1:], r)
    elif x[0] == "-":
        # -x * y = - (x * y)
        return "-" + multiply(x[1:], y, r)
    elif y[0] == "-":
        # x * -y = - (x * y)
        return "-" + multiply(x, y[1:], r)

    resultList = list(symbols[0] * (len(x) + len(y)))

    for i in range(len(x)):
        carry = "0"
        for j in range(len(y)):
            elemMult = elementaryMult(
                x[len(x) - 1 - i],
                y[len(y) - 1 - j],
                resultList[-1 * (i + j + 1)],
                carry,
                r,
            )
            carry = elemMult[1]
            resultList[-1 * (i + j + 1)] = elemMult[0]
        resultList[-1 * (i + len(y) + 1)] = carry

    if resultList[-1 * (len(x) + len(y))] == "0":
        k = len(x) + len(y) - 1
    else:
        k = len(x) + len(y)

    result = ""
    # converting the list to a string
    for i in resultList:
        result += i

    return removeLeadingZeros(result[-1 * k :])


def karatsuba(x: str, y: str, r: int) -> str:
    """
    Multiplies two numbers x and y using Karatsuba's recursive algorithm and returns the result,
    all represented in a specified radix.

    Parameters:
        x (str): The first number as a string, in radix r.
        y (str): The second number as a string, in radix r.
        r (int): The radix in which the numbers are expressed and the multiplication is performed, must be between 2 and 16.

    Preconditions:
        - `r` must be between 2 and 16.
        - Negative numbers are represented by a leading '-' character.

    Returns:
        str: Result of x*y in radix r.
    """

    x = removeLeadingZeros(x)
    y = removeLeadingZeros(y)

    if x[0] == "-" and y[0] == "-":
        # -x * -y = x * y
        return karatsuba(x[1:], y[1:], r)
    elif x[0] == "-":
        # -x * y = - (x * y)
        return "-" + karatsuba(x[1:], y, r)
    elif y[0] == "-":
        # x * -y = - (x * y)
        return "-" + karatsuba(x, y[1:], r)

    if len(x) < 2 or len(y) < 2:
        return multiply(x, y, r)

    length = max(len(x), len(y))

    # add 0's to the front of x and y to make x and y have equal lengths
    x = symbols[0] * (length - len(x)) + x
    y = symbols[0] * (length - len(y)) + y

    if not (length % 2 == 0):
        # add 0 to the start of x and y so that they are both of even length
        x = symbols[0] + x
        y = symbols[0] + y

    splitLength = len(x) // 2

    a = x[:splitLength]  # x(hi)
    b = x[splitLength:]  # x(lo)
    c = y[:splitLength]  # y(hi)
    d = y[splitLength:]  # y(lo)

    ac = karatsuba(a, c, r)
    bd = karatsuba(b, d, r)
    # ad + bc = [(a + b) * (c + d)] - ac - bd
    ad_Plus_bc = subtract(
        subtract(karatsuba(add(a, b, r), add(c, d, r), r), ac, r), bd, r
    )

    return add(
        add(
            ac + (symbols[0] * (2 * splitLength)),
            ad_Plus_bc + (symbols[0] * splitLength),
            r,
        ),
        bd,
        r,
    )


def extEuclid(x: str, y: str, r: int) -> tuple[str, str, str]:
    """
    Calculates the greatest common divisor (gcd) of two numbers x and y using the Extended Euclidean Algorithm,
    and finds coefficients a and b such that gcd(x, y) = ax + by. All values are represented in a specified radix.

    Parameters:
        x (str): The first number as a string, in radix r.
        y (str): The second number as a string, in radix r.
        r (int): The radix in which the numbers are expressed and calculations are performed, must be between 2 and 16.

    Preconditions:
        - `r` must be between 2 and 16.
        - Negative numbers are represented by a leading '-' character.

    Returns:
        tuple: (gcd(x,y), a, b) in radix r. Where gcd(x,y) = ax + by.
    """

    x = removeLeadingZeros(x)
    y = removeLeadingZeros(y)

    # use modulus on both x and y to get positive integers
    # a <- |x|
    if x[0] == "-":
        a = x[1:]
    else:
        a = x
    # b <- |y|
    if y[0] == "-":
        b = y[1:]
    else:
        b = y

    x1 = "1"
    x2 = "0"
    y1 = "0"
    y2 = "1"

    # use the rule gcd(a,b) = gcd(a-qb, b), as the set of common divisors is invariant
    # stop if b becomes negative, such that gcd(a, b) = gcd(a, 0) = a
    while greaterOrEqual(b, "1"):
        q = divide(a, b, r)
        remainder = subtract(a, multiply(q, b, r), r)

        a = b
        b = remainder

        x3 = subtract(x1, multiply(q, x2, r), r)
        y3 = subtract(y1, multiply(q, y2, r), r)

        x1 = x2
        y1 = y2
        x2 = x3
        y2 = y3

    result = a

    # x is positive
    if greaterOrEqual(x, "0"):
        x = x1
    # remove '-' sign
    else:
        x = x1[1:]

    # remove '-' sign
    if greaterOrEqual(y, "0"):
        y = y1
    else:
        y = y1[1:]

    # returns gcd(x,y) and values a and b, such that d = ax + by
    # note that a and b above are returned as values x and y below
    return result, x, y


def modularReduction(n: str, m: str, r: int) -> str:
    """
    Computes the reduction of a number n modulo m in a specified radix.

    Parameters:
        n (str): The dividend as a string in radix r.
        m (str): The divisor as a string in radix r, must be greater than zero.
        r (int): The radix in which the numbers are expressed and the operation is performed, must be between 2 and 16.

    Preconditions:
        - `r` must be between 2 and 16.
        - `m` must be greater than zero.

    Returns:
        str: Result of n mod m in radix r.
    """

    n = removeLeadingZeros(n)

    isNegative = False
    if n[0] == "-":
        n = n[1:]
        isNegative = True

    i = len(n) - len(m)
    while i >= 0:
        ri = "1" if i == 0 else "1" + ((i - 1) * "0")
        mri = multiply(m, ri, r)
        while greaterOrEqual(n, mri):
            n = subtract(n, mri, r).lstrip("0")
        i = i - 1
    if (not isNegative) or n == "0":
        return removeLeadingZeros(n)
    return removeLeadingZeros(subtract(m, n, r))


def modularAddition(x: str, y: str, m: str, r: int) -> str:
    """
    Computes the sum of two numbers x and y, modulo m, all represented in a specified radix.

    Parameters:
        x (str): The first addend as a string, in radix r, assumed to be already reduced modulo m.
        y (str): The second addend as a string, in radix r, assumed to be already reduced modulo m.
        m (str): The modulus as a string in radix r, must be greater than zero.
        r (int): The radix in which the numbers are expressed and the operation is performed, must be between 2 and 16.

    Preconditions:
        - `r` must be between 2 and 16.
        - `m` must be greater than zero.
        - `x` and `y` should already be in reduced form modulo m.

    Returns:
        str: The result of (x + y) modulo m, in radix r.
    """

    z = add(x, y, r)
    if greaterOrEqual(z, m):
        z = subtract(z, m, r)
    return z


def modularSubtraction(x: str, y: str, m: str, r: int) -> str:
    """
    Computes the subtraction of two numbers x and y, modulo m, all represented in a specified radix.

    Parameters:
        x (str): As string, in radix r, assumed to be already reduced modulo m.
        y (str): As a string, in radix r, assumed to be already reduced modulo m.
        m (str): The modulus as a string in radix r, must be greater than zero.
        r (int): The radix in which the numbers are expressed and the operation is performed, must be between 2 and 16.

    Preconditions:
        - `r` must be between 2 and 16.
        - `m` must be greater than zero.
        - `x` and `y` should already be in reduced form modulo m.

    Returns:
        str: The result of (x - y) modulo m, in radix r.
    """

    z = subtract(x, y, r)
    # if z<0 then z += m
    if greaterOrEqual("-1", z):
        z = add(z, m, r)
    return z


def modularMultiplication(x: str, y: str, m: str, r: int) -> str:
    """
    Computes the product of two numbers x and y, modulo m, all represented in a specified radix.

    Parameters:
        x (str): The first factor as a string, in radix r, assumed to be already reduced modulo m.
        y (str): The second factor as a string, in radix r, assumed to be already reduced modulo m.
        m (str): The modulus as a string in radix r, must be greater than zero.
        r (int): The radix in which the numbers are expressed and the operation is performed, must be between 2 and 16.

    Preconditions:
        - `r` must be between 2 and 16.
        - `m` must be greater than zero.
        - Both `x` and `y` should already be in reduced form modulo m.

    Returns:
        str: The result of (x * y) modulo m, in radix r.
    """

    z = multiply(x, y, r)
    z = modularReduction(z, m, r)
    return z


def modularInversion(a: str, m: str, r: int) -> str:
    """
    Computes the modular inverse of a modulo m, if it exists.

    Parameters:
        a (str): The number whose inverse is to be computed, as a string in radix r.
        m (str): The modulus as a string in radix r, must be greater than zero.
        r (int): The radix in which the numbers are expressed and the operation is performed, must be between 2 and 16.

    Preconditions:
        - `r` must be between 2 and 16.
        - `m` must be greater than zero.

    Returns:
        str: If the inverse exists, the result of a^-1 mod m in radix r.
            Otherwise, prints "Inverse does not exist".
    """

    originalModulo = m
    x1 = "1"
    x2 = "0"
    while greaterOrEqual(m, "1"):
        q = divide(a, m, r)
        # remainder = a - q*m
        remainder = subtract(a, multiply(q, m, r), r)
        a = m
        m = remainder
        # x3 = x1 - q*x2
        x3 = subtract(x1, multiply(q, x2, r), r)
        x1 = x2
        x2 = x3
    if a == "1":
        x1 = modularReduction(
            add(modularReduction(x1, originalModulo, r), originalModulo, r),
            originalModulo,
            r,
        )
        return x1
    else:
        print("Inverse does not exist")
