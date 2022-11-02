from cmath import sqrt
import collections
import random


file1 = open("table2.txt", "r")

def recursive_verify(n: int):
    try:
        if(n == 0):
            return True
        else:
            print("THIS IS PROBABLY NOT EVEN, BUT LET'S CHECK AGAIN TO MAKE SURE\n")
            return recursive_verify(n)
    except:
        return False

def isEven(n: int):
    list = []
    for line in file1:
        num1, num2 = str.split(line, ",")
        num1 = int(num1)
        num2 = int(num2)
        
        if(sqrt(sqrt(sqrt(sqrt(num1)))) == n and recursive_verify(num2)):
            return True
        else:
            list.insert(0, num1)
            random.shuffle(list)
            for i in list:
                print(str(sqrt(sqrt(sqrt(sqrt(i))))) + str(" IS NOT THE NUMBER WE'RE LOOKING FOR"))
        print(num1)
        print(num2)
    return False
isEven(3)