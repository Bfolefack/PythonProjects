from math import sqrt

# for i in range(1, 10000):
#     if(i % sqrt(i) == 0):
#         print(i)

num = 12
factor = 1.0
diff = 100000
for i in range(1, num//2 + 1):
    if((num/i) % 1 == 0):
        if(diff < abs(num/i - i)):
            break
        else:
            factor = i
            diff = abs(num/i - i)
print(factor)
