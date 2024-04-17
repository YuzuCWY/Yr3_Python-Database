#Q2 Is it a leap year?

#Ask for a input and identify if it is a leap year

input_year = eval(input("Pls enter a year: "))

if input_year<0:
    print("Wrong input, input should >=0. Program exited.")
    exit()
else:
    #check if it is a leap year
    if (input_year%4==0 and input_year%100!=0):
        print(input_year, " is a leap year.")
    elif (input_year%400==0):
        print(input_year, " is a leap year.")
    else:
        print(input_year, " is not a leap year.")
