#Wk3 before lesson
#Q4 base on monte carlo simulation to estimate PI

import random

n = int(input("Enter the number of iterations: "))

count = 0
for i in range(n):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    #to check if it is within the circle
    if x**2 + y**2 <= 1: 
        count += 1

pi = 4 * count / n
print("The estimated value of pi is:", pi)
