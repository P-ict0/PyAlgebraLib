# Efficient algebra

Python program to perform algebra operations using efficient algorithms.
Can operate with numbers from radix 2 to radix 16. Without converting between radix in each operation.

Supported operations: 
    * Addition
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

<hr>

# Getting Started
Run python on the same folder as the program and run 
```python
import efficientAlgebra
```
Then, on the same terminal you can perform operations like:
```python
efficientAlgebra.karatsuba("364DA","-13F", 16)
```
The output is not formatted yet in a readable way, look into the code for details.
