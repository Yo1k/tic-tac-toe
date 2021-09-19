import numpy as np
import os

data = np.array([[1, 2], [3, 4]])
ones = np.array([[1, 1], [1, 1]])
result = np.array([[2, 3], [4, 5]])

assert np.array_equal(result, ones + data), "Code is not working."
print("Code is working.", end=os.linesep)
