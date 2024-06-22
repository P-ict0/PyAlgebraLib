# 😁 Welcome!!

# Contents

- [😁 Welcome!!](#-welcome)
- [Contents](#contents)
- [🧮 AlgebraPy](#-algebrapy)
- [✨ Features](#-features)
- [📜 Supported operations:](#-supported-operations)
- [📦 Installation and Usage](#-installation-and-usage)


# 🧮 AlgebraPy

Simple Python program to perform algebra operations using efficient algorithms like Karatsuba's algorithm for multiplication or Extended Euclidean Algorithm for great common divisor (GCD).

This program is intended to be lighweight (no dependencies) and very efficient.

# ✨ Features

Can operate with numbers from base 2 to base 16. Without converting between bases in each operation.

Note: _**Each number has to be inputted and will be returned as a string, except the base.**_

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

# 📦 Installation and Usage

```bash
pip install AlgebraPy
```

You can import the module:
```python
import AlgebraPy as ap
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
