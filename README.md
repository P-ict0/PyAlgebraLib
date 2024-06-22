# 😁 Welcome!!

# Contents

- [😁 Welcome!!](#-welcome)
- [Contents](#contents)
- [🧮 PyAlgebraLib](#-pyalgebralib)
- [🚀 Quick start](#-quick-start)
- [✨ Features](#-features)
- [📦 Installation and Usage](#-installation-and-usage)
- [📜 Supported operations:](#-supported-operations)


# 🧮 PyAlgebraLib

Simple Python program to perform algebra operations using efficient algorithms like Karatsuba's algorithm for multiplication or Extended Euclidean Algorithm for great common divisor (GCD).

This program is intended to be lighweight (no dependencies) and very efficient.

# 🚀 Quick start

```bash
pip install PyAlgebraLib
```

You can import the module:
```python
import PyAlgebraLib as pa
```

# ✨ Features

Can operate with numbers from base 2 to base 16. Without converting between bases in each operation.

Note: _**Each number has to be inputted and will be returned as a string, except the base.**_

# 📦 Installation and Usage

```bash
pip install PyAlgebraLib
```

You can import the module:
```python
import PyAlgebraLib as ap
```

Then, you can perform operations like:
```python
pa.karatsuba("364da","-13f", 16)      # Multiplication (karatsuba algorithm)
pa.extEuclid("-1460","44321521", 7)   # GCD (Extended)
```

The output is either a string or a tuple with the result(s), look into the specific function docstrings for more information.

Example:
```python
pa.extEuclid("-1460","44321521", 7)
# Output: ('1', '-20066304', '511')

pa.modularInversion("9a1aa8a02232", "a6a722a", 11)
# Output: '3293845'
```

# 📜 Supported operations:

    - Addition
    - Subtraction 
    - Multiplication (Normal "primary school method" + Karatsuba algorithm)
    - Division
    - GCD of 2 numbers (Extended Euclidean algorithm)
    - Modular Arithmetic:
        - Reduction
        - Addition
        - Subtraction
        - Multiplication
        - Inversion

<hr>

| Function Name          | Input                                                                                      | Output                                                            |
|------------------------|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| removeLeadingZeros     | a (str)                                                                                    | str: The modified string with all leading zeros removed           |
| greaterOrEqual         | x (str), y (str)                                                                           | bool: True if x is greater than or equal to y, False otherwise    |
| divide                 | x (str), y (str), r (int) = 10                                                             | str: The quotient of x divided by y, expressed in radix r         |
| elementaryAdd          | x (str), y (str), c (str), r (int) = 10                                                    | tuple: (result (str), carry (str))                                |
| elementarySub          | x (str), y (str), c (str), r (int) = 10                                                    | tuple: (result (str), carry (str))                                |
| elementaryMult         | x (str), y (str), z (str), c (str), r (int) = 10                                           | tuple: (result (str), carry (str))                                |
| add                    | x (str), y (str), r (int) = 10                                                             | str: Result of x + y in radix r                                   |
| subtract               | x (str), y (str), r (int) = 10                                                             | str: Result of x - y in radix r                                   |
| multiply               | x (str), y (str), r (int) = 10                                                             | str: Result of x * y in radix r                                   |
| karatsuba              | x (str), y (str), r (int) = 10                                                             | str: Result of x * y using Karatsuba algorithm in radix r         |
| extEuclid              | x (str), y (str), r (int) = 10                                                             | tuple: (gcd (str), a (str), b (str))                              |
| modularReduction       | n (str), m (str), r (int) = 10                                                             | str: Result of n mod m in radix r                                 |
| modularAddition        | x (str), y (str), m (str), r (int) = 10                                                    | str: Result of (x + y) mod m in radix r                           |
| modularSubtraction     | x (str), y (str), m (str), r (int) = 10                                                    | str: Result of (x - y) mod m in radix r                           |
| modularMultiplication  | x (str), y (str), m (str), r (int) = 10                                                    | str: Result of (x * y) mod m in radix r                           |
| modularInversion       | a (str), m (str), r (int) = 10                                                             | str: Inverse of a mod m in radix r, or prints "Inverse does not exist" |
