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

Author: Rodrigo Martín Núñez (Technical University of Eindhoven Student)

Date: 2021-2022
"""

addCount = 0
mulCount = 0
symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']


def removeLeadingZeros(a):
    """
    removes all leading 0's of a string, ignores any occurrence of '-' (so also removes 0's after '-')

    :param a: (str) Input int
    :return: (str) Number a without leading 0's
    """

    if len(a) == 0:
        return '0'
    res = ""
    if a[0] == '-':
        res = '-' + a[1:].lstrip('0')
    else:
        res = a.lstrip('0')
    if len(res) == 0:
        res = "0"
    return res


def greaterOrEqual(x, y):
    """
    Returns if x is greater than or equal to y

    :params x,y: (str) Input ints
    pre: x > 0 and y > 0
    returns: (bool) x > y
    """

    if len(x) > len(y):
        return True
    elif len(x) == len(y):
        for i in range(len(x)):
            if symbols.index(x[i]) > symbols.index(y[i]):
                return True
            if symbols.index(x[i]) < symbols.index(y[i]):
                return False
        return True
    return False


def divide(x, y, r):
    """
    Divides x by y

    :params x,y: (str) Imput ints
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16
    :return: (str) x // y in radix r
    """

    q = "-1"
    while not (x[0] == '-'):
        q = add(q, "1", r)
        x = subtract(x, y, r)
    return q


def elementaryAdd(x, y, c, r):
    """
    Adds x, y and a carry c in radix r. Returns single word result and carry

    :params x,y,c: (char) Input chars
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and len(x) == 1 and len(y) == 1 and len(c) == 1
    :return: (str) Rightmost char of x + y + c and (str) the carry in radix r
    """

    # resulting word
    result = symbols[(symbols.index(x) + symbols.index(y) + symbols.index(c)) % r]
    # carry word
    carry = symbols[((symbols.index(x) + symbols.index(y) + symbols.index(c)) // r)]

    global addCount
    addCount += 1

    return result, carry


def elementarySub(x, y, c, r):
    """
    Subtracts y and a carry c from x in radix r. Returns single word result and carry

    :params x,y,c: (char) Input chars
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and len(x) == 1 and len(y) == 1 and len(c) == 1
    :return: (str) Rightmost char of x - y - c and (str) the carry in radix r
    """

    # resulting word
    result = symbols[(symbols.index(x) - symbols.index(y) - symbols.index(c)) % r]
    # carry word
    carry = '1' if (symbols.index(x) - symbols.index(y) - symbols.index(c)) < 0 else '0'

    return result, carry


def elementaryMult(x, y, z, c, r):
    """
    Multiplies x and y and adds a carry c and the current value of the result z in radix r. Returns single word result and carry

    :params x,y,z,c: (char) Input chars
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and len(x) == 1 and len(y) == 1 and len(c) == 1 and len(z) == 1
    :return: (str) Rightmost char of x * y + c + z and (str) the carry in radix r
    """

    t = symbols.index(z) + (symbols.index(x) * symbols.index(y)) + symbols.index(c)
    # carry word
    carry = symbols[t // r]
    # resulting word
    result = symbols[t - ((t // r) * r)]

    global mulCount
    mulCount += 1

    return result, carry


def add(x, y, r):
    """
    Adds two numbers x and y and returns the result, all represented in radix r

    :params x,y: (str) Input ints
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and (negative numbers always start with "-")
    :return: (str) Result of x + y in radix r
    """

    x = removeLeadingZeros(x)
    y = removeLeadingZeros(y)

    bothNegative = False
    # handle negative numbers
    if x[0] == '-' and y[0] == '-':
        # -x + -y = -(x + y)
        x = x[1:]
        y = y[1:]
        bothNegative = True
    elif x[0] == '-':
        # -x + y = y - x
        return subtract(y, x[1:], r)
    elif y[0] == '-':
        # x + -y = x - y
        return subtract(x, y[1:], r)

    result = ""
    carry = '0'
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
        result = '-' + result

    return removeLeadingZeros(result)


def subtract(x, y, r):
    """
    Subtracts two numbers x and y and returns the result, all represented in radix r

    :params x,y: (str) Input ints
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and (negative numbers always start with "-")
    :return: (str) Result of x - y in radix r
    """

    x = removeLeadingZeros(x)
    y = removeLeadingZeros(y)

    # handle negative numbers
    if x[0] == '-' and y[0] == '-':
        # -x - -y = y - x
        return subtract(y[1:], x[1:], r)
    elif x[0] == '-':
        # -x - y = -x + -y 
        return add('-' + y, x, r)
    elif y[0] == '-':
        # x - -y = x + y
        return add(x, y[1:], r)

    if not greaterOrEqual(x, y):
        return '-' + subtract(y, x, r)

    result = ""
    carry = '0'

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


def multiply(x, y, r):
    """
    Multiplies two numbers x and y and returns the result, all represented in radix r

    :params x,y: (str) Input ints
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and (negative numbers always start with "-")
    :return: (str) Result of x * y in radix r
    """

    x = removeLeadingZeros(x)
    y = removeLeadingZeros(y)

    if x[0] == '-' and y[0] == '-':
        # -x * -y = x * y
        return multiply(x[1:], y[1:], r)
    elif x[0] == '-':
        # -x * y = - (x * y) 
        return '-' + multiply(x[1:], y, r)
    elif y[0] == '-':
        # x * -y = - (x * y)
        return '-' + multiply(x, y[1:], r)

    resultList = list(symbols[0] * (len(x) + len(y)))

    for i in range(len(x)):
        carry = '0'
        for j in range(len(y)):
            elemMult = elementaryMult(x[len(x) - 1 - i], y[len(y) - 1 - j], resultList[-1 * (i + j + 1)], carry, r)
            carry = elemMult[1]
            resultList[-1 * (i + j + 1)] = elemMult[0]
        resultList[-1 * (i + len(y) + 1)] = carry

    if resultList[-1 * (len(x) + len(y))] == '0':
        k = len(x) + len(y) - 1
    else:
        k = len(x) + len(y)

    result = ""
    # converting the list to a string
    for i in resultList:
        result += i

    return removeLeadingZeros(result[-1 * k:])


def karatsuba(x, y, r):
    """
    Multiplies two numbers x and y using karatsubas recursive algorithm and returns the result, all represented in radix r

    :params x,y: (str) Input ints
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and (negative numbers always start with "-")
    :return: (str) Result of x * y in radix r
    """

    x = removeLeadingZeros(x)
    y = removeLeadingZeros(y)

    if x[0] == '-' and y[0] == '-':
        # -x * -y = x * y
        return karatsuba(x[1:], y[1:], r)
    elif x[0] == '-':
        # -x * y = - (x * y) 
        return '-' + karatsuba(x[1:], y, r)
    elif y[0] == '-':
        # x * -y = - (x * y)
        return '-' + karatsuba(x, y[1:], r)

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
    ad_Plus_bc = subtract(subtract(karatsuba(add(a, b, r), add(c, d, r), r), ac, r), bd, r)

    return add(add(ac + (symbols[0] * (2 * splitLength)), ad_Plus_bc + (symbols[0] * splitLength), r), bd, r)


def extEuclid(x, y, radix):
    """
    Calculates the greatest common divisor d of the number x and y
    returns gcd(x,y) and values a and b, such that d = ax + by

    :params x,y: (str) Input ints
    :param radix: (int) The radix
    :pre: r >= 2 and r <= 16 and (negative numbers always start with "-")
    :return: (str) Result of gcd(x,y), (str) a, (str) b such that gcd(x,y) = ax + by all in radix r
    """

    x = removeLeadingZeros(x)
    y = removeLeadingZeros(y)

    # use modulus on both x and y to get positive integers
    # a <- |x|
    if x[0] == '-':
        a = x[1:]
    else:
        a = x
    # b <- |y|
    if y[0] == '-':
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
        q = divide(a, b, radix)
        r = subtract(a, multiply(q, b, radix), radix)

        a = b
        b = r

        x3 = subtract(x1, multiply(q, x2, radix), radix)
        y3 = subtract(y1, multiply(q, y2, radix), radix)

        x1 = x2
        y1 = y2
        x2 = x3
        y2 = y3

    result = a

    #
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


def modularReduction(n, m, r):
    """
    Returns n mod m, in radix r

    :params n,m: (str) Input ints
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and m > 0
    :return: (str) Result of n % m in radix r
    """

    n = removeLeadingZeros(n)

    isNegative = False
    if n[0] == '-':
        n = n[1:]
        isNegative = True

    i = len(n) - len(m)
    while i >= 0:
        ri = "1" if i == 0 else "1" + ((i - 1) * '0')
        mri = multiply(m, ri, r)
        while greaterOrEqual(n, mri):
            n = subtract(n, mri, r).lstrip('0')
        i = i - 1
    if (not isNegative) or n == "0":
        return removeLeadingZeros(n)
    return removeLeadingZeros(subtract(m, n, r))


def modularAddition(x, y, m, r):
    """
    Returns z = x + y (mod m)

    :params x,y,m: (str) Input ints
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and m > 0 and (x and y are already in reduced form)
    :return: (str) Result of x + y (mod m) in radix r
    """

    z = add(x, y, r)
    if greaterOrEqual(z, m):
        z = subtract(z, m, r)
    return z


def modularSubtraction(x, y, m, r):
    '''
    Returns z = x - y (mod m)
    
    :params x,y,m: (str) Input ints
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and m > 0 and (x and y are already in reduced form)
    :return: (str) Result of x - y (mod m) in radix r
    '''

    z = subtract(x, y, r)
    # if z<0 then z += m
    if greaterOrEqual("-1", z):
        z = add(z, m, r)
    return z


def modularMultiplication(x, y, m, r):
    """
    Returns z = x * y (mod m)

    :params x,y,m: (str) Input ints
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and m > 0 and (x and y are already in reduced form)
    :return: (str) Result of x * y (mod m) in radix r
    """

    z = multiply(x, y, r)
    z = modularReduction(z, m, r)
    return z


def modularInversion(a, m, r):
    """
    Returns a^(-1) (mod m) if it exists

    :params a,m: (str) Input ints
    :param r: (int) The radix
    :pre: r >= 2 and r <= 16 and m > 0
    :return: (str) Result of a^(-1) (mod m) if it exists or (srt) "Inverse does not exist" if it doesnt exist
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
        x1 = modularReduction(add(modularReduction(x1, originalModulo, r), originalModulo, r), originalModulo, r)
        return x1
    else:
        print("Inverse does not exist")
