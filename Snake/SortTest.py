import numpy as np

a = [['W0', 1.0], ['W1', 0.9], ['W2', 0.75], ['W3', 0.915], ['W4', 0.8], ['W5', 0.92], ['W6', 0.084], ['W7', 0.99], ['W8', 0.917], ['W9', 0.92]]

print(sorted(a, key=lambda k: k[1])) #key function is used to get the thing tat determines the sorting.