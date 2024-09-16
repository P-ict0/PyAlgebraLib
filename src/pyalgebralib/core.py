from .helpers import (
    removeLeadingZeros,
    elementaryAdd,
    elementarySub,
    greaterOrEqual,
)
from .config import symbols


"""
Program to perform algebra operations using efficient algorithms.
Can operate with numbers from radix 2 to radix 16. Without converting between radix.

Supported operations:
    - Addition
    - Subtraction
    - Multiplication (efficient recursive Karatsuba algorithm)
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


class pyAlgebraLib:
    def __init__(self):
        pass

    def divide(self, x: str, y: str, r: int = 10) -> str:
        """
        Divides one integer by another (both as str) and returns the quotient in the specified radix.

        Parameters:
            x (str): The dividend.
            y (str): The divisor.
            r (int): The radix in which to express the quotient. Must be between 2 and 16, inclusive.
                        Default is 10.

        Preconditions:
            r must be at least 2 and no more than 16.

        Returns:
            str: The quotient of x divided by y, expressed in radix r.
        """

        q = "-1"
        while not (x[0] == "-"):
            q = self.add(q, "1", r)
            x = self.subtract(x, y, r)
        return q

    def add(self, x: str, y: str, r: int = 10) -> str:
        """
        Adds two numbers represented as strings in a specified radix and returns the resulting sum as a string.

        Parameters:
            x (str): The first number as a string in radix r.
            y (str): The second number as a string in radix r.
            r (int): The radix in which the numbers are expressed and the addition is performed, must be between 2 and 16.
                        Default is 10.

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
            return self.subtract(y, x[1:], r)
        elif y[0] == "-":
            # x + -y = x - y
            return self.subtract(x, y[1:], r)

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

    def subtract(self, x: str, y: str, r: int = 10) -> str:
        """
        Subtracts two numbers represented as strings in a specified radix and returns the resulting sum as a string.

        Parameters:
            x (str): The first number as a string in radix r.
            y (str): The second number as a string in radix r.
            r (int): The radix in which the numbers are expressed and the subtraction is performed, must be between 2 and 16.
                        Default is 10.

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
            return self.subtract(y[1:], x[1:], r)
        elif x[0] == "-":
            # -x - y = -x + -y
            return self.add("-" + y, x, r)
        elif y[0] == "-":
            # x - -y = x + y
            return self.add(x, y[1:], r)

        if not greaterOrEqual(x, y):
            return "-" + self.subtract(y, x, r)

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

    def multiply(self, x: str, y: str, r: int = 10) -> str:
        """
        Multiplies two numbers x and y using Karatsuba's recursive algorithm and returns the result,
        all represented in a specified radix.

        Parameters:
            x (str): The first number as a string, in radix r.
            y (str): The second number as a string, in radix r.
            r (int): The radix in which the numbers are expressed and the multiplication is performed, must be between 2 and 16.
                        Default is 10.

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
            return self.multiply(x[1:], y[1:], r)
        elif x[0] == "-":
            # -x * y = - (x * y)
            return "-" + self.multiply(x[1:], y, r)
        elif y[0] == "-":
            # x * -y = - (x * y)
            return "-" + self.multiply(x, y[1:], r)

        if len(x) < 2 or len(y) < 2:
            return self.multiply(x, y, r)

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

        ac = self.multiply(a, c, r)
        bd = self.multiply(b, d, r)
        # ad + bc = [(a + b) * (c + d)] - ac - bd
        ad_Plus_bc = self.subtract(
            self.subtract(
                self.multiply(self.add(a, b, r), self.add(c, d, r), r), ac, r
            ),
            bd,
            r,
        )

        return self.add(
            self.add(
                ac + (symbols[0] * (2 * splitLength)),
                ad_Plus_bc + (symbols[0] * splitLength),
                r,
            ),
            bd,
            r,
        )

    def extEuclid(self, x: str, y: str, r: int = 10) -> tuple[str, str, str]:
        """
        Calculates the greatest common divisor (gcd) of two numbers x and y using the Extended Euclidean Algorithm,
        and finds coefficients a and b such that gcd(x, y) = ax + by. All values are represented in a specified radix.

        Parameters:
            x (str): The first number as a string, in radix r.
            y (str): The second number as a string, in radix r.
            r (int): The radix in which the numbers are expressed and calculations are performed, must be between 2 and 16.
                        Default is 10.

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
            q = self.divide(a, b, r)
            remainder = self.subtract(a, self.multiply(q, b, r), r)

            a = b
            b = remainder

            x3 = self.subtract(x1, self.multiply(q, x2, r), r)
            y3 = self.subtract(y1, self.multiply(q, y2, r), r)

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

    def modularReduction(self, n: str, m: str, r: int = 10) -> str:
        """
        Computes the reduction of a number n modulo m in a specified radix.

        Parameters:
            n (str): The dividend as a string in radix r.
            m (str): The divisor as a string in radix r, must be greater than zero.
            r (int): The radix in which the numbers are expressed and the operation is performed, must be between 2 and 16.
                        Default is 10.

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
            mri = self.multiply(m, ri, r)
            while greaterOrEqual(n, mri):
                n = self.subtract(n, mri, r).lstrip("0")
            i = i - 1
        if (not isNegative) or n == "0":
            return removeLeadingZeros(n)
        return removeLeadingZeros(self.subtract(m, n, r))

    def modularAddition(self, x: str, y: str, m: str, r: int = 10) -> str:
        """
        Computes the sum of two numbers x and y, modulo m, all represented in a specified radix.

        Parameters:
            x (str): The first addend as a string, in radix r, assumed to be already reduced modulo m.
            y (str): The second addend as a string, in radix r, assumed to be already reduced modulo m.
            m (str): The modulus as a string in radix r, must be greater than zero.
            r (int): The radix in which the numbers are expressed and the operation is performed, must be between 2 and 16.
                        Default is 10.

        Preconditions:
            - `r` must be between 2 and 16.
            - `m` must be greater than zero.
            - `x` and `y` should already be in reduced form modulo m.

        Returns:
            str: The result of (x + y) modulo m, in radix r.
        """

        z = self.add(x, y, r)
        if self.greaterOrEqual(z, m):
            z = self.subtract(z, m, r)
        return z

    def modularSubtraction(self, x: str, y: str, m: str, r: int = 10) -> str:
        """
        Computes the subtraction of two numbers x and y, modulo m, all represented in a specified radix.

        Parameters:
            x (str): As string, in radix r, assumed to be already reduced modulo m.
            y (str): As a string, in radix r, assumed to be already reduced modulo m.
            m (str): The modulus as a string in radix r, must be greater than zero.
            r (int): The radix in which the numbers are expressed and the operation is performed, must be between 2 and 16.
                        Default is 10.

        Preconditions:
            - `r` must be between 2 and 16.
            - `m` must be greater than zero.
            - `x` and `y` should already be in reduced form modulo m.

        Returns:
            str: The result of (x - y) modulo m, in radix r.
        """

        z = self.subtract(x, y, r)
        # if z<0 then z += m
        if greaterOrEqual("-1", z):
            z = self.add(z, m, r)
        return z

    def modularMultiplication(self, x: str, y: str, m: str, r: int = 10) -> str:
        """
        Computes the product of two numbers x and y, modulo m, all represented in a specified radix.

        Parameters:
            x (str): The first factor as a string, in radix r, assumed to be already reduced modulo m.
            y (str): The second factor as a string, in radix r, assumed to be already reduced modulo m.
            m (str): The modulus as a string in radix r, must be greater than zero.
            r (int): The radix in which the numbers are expressed and the operation is performed, must be between 2 and 16.
                        Default is 10.

        Preconditions:
            - `r` must be between 2 and 16.
            - `m` must be greater than zero.
            - Both `x` and `y` should already be in reduced form modulo m.

        Returns:
            str: The result of (x * y) modulo m, in radix r.
        """

        z = self.multiply(x, y, r)
        z = self.modularReduction(z, m, r)
        return z

    def modularInversion(self, a: str, m: str, r: int = 10) -> str:
        """
        Computes the modular inverse of a modulo m, if it exists.

        Parameters:
            a (str): The number whose inverse is to be computed, as a string in radix r.
            m (str): The modulus as a string in radix r, must be greater than zero.
            r (int): The radix in which the numbers are expressed and the operation is performed, must be between 2 and 16.
                        Default is 10.

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
            q = self.divide(a, m, r)
            # remainder = a - q*m
            remainder = self.subtract(a, self.multiply(q, m, r), r)
            a = m
            m = remainder
            # x3 = x1 - q*x2
            x3 = self.subtract(x1, self.multiply(q, x2, r), r)
            x1 = x2
            x2 = x3
        if a == "1":
            x1 = self.modularReduction(
                self.add(
                    self.modularReduction(x1, originalModulo, r), originalModulo, r
                ),
                originalModulo,
                r,
            )
            return x1
        else:
            print("Inverse does not exist")
