import random
import numpy as np
from math import factorial

#list = [7 * factorial(3),11 * factorial(5), 15 * factorial(7) ]
list = [random.randint(1,20) for i in range(10)]
# find the Least Common Multiple of the list
num = 1
while(np.sum([num % i for i in list]) != 0):
    num += 1
print(list)
print(num)