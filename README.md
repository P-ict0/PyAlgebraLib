# 😁 Welcome!!

# Contents

- [😁 Welcome!!](#-welcome)
- [Contents](#contents)
- [🧮 PyAlgebra](#-pyalgebra)
- [✨ Features](#-features)
- [📜 Supported operations:](#-supported-operations)
- [📦 Installation and Usage](#-installation-and-usage)


# 🧮 PyAlgebra

Python program to perform algebra operations using efficient algorithms like Karatsuba's algorithm for multiplication or Extended Euclidean Algorithm for great common divisor (GCD).

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

Requirements:
```
git python
```

```bash
# Clone in same folder as your project
git clone https://github.com/P-ict0/PyAlgebra.git /path/to/your/project
```
In your project, you can import the module:
```python
import pyAlgebra as pa
```
Then, you can perform operations like:
```python
pa.karatsuba("364da","-13f", 16)      # Multiplication (karatsuba algorithm)
pa.extEuclid("-1460","44321521", 7)   # GCD (Extended)
```

The output is a tuple with the result(s) and the base of the result(s), look into the code for more information.

Example:
```python
pa.extEuclid("-1460","44321521", 7)
# Output: ('1', '-20066304', '511')

pa.modularInversion("9a1aa8a02232", "a6a722a", 11)
# Output: '3293845'
```
