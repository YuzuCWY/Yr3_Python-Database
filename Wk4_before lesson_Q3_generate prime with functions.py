#Wk4 before lesson
#Q3 prime numbers in 5 rows , 10 columns

import math
primenum = 50
linenum = 10
count = 0
number = 2

def is_Prime(n):
    if n<=1:
        return False
    for i in range (2, int(math.sqrt(number))+1):
        if number%i==0:
            isPrime = False
            break

print("The first 50 prime numbers are: ")
while count<primenum:
    isPrime = True
    is_Prime(number)
    if isPrime:
        print(format(number, "5d"),end="")
        count+=1
        if count%linenum==0:
            print()
    number+=1

