#Wk4 before lesson
#Q1 3n+1

global counter
counter = 0

def print3n1(n):
    global counter
    print(int(n), end=" ")
    if (n==1):
        return "program exit"
    elif (n%2==1):
        n = 3*n+1
        print3n1(n)
        counter += 1
    elif (n%2==0):
        n = n/2
        counter += 1
        print3n1(n)
        
input_num1, input_num2 = eval(input("pls enter an integer: "))
print (input_num1, input_num2)
print3n1(input_num)
print()
print("cycle is ", counter+1)
