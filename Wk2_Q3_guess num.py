#Q3 Create a lottary system

#generate 2 numbers (0-9) randomly with sequence
#require user to enter 2 num
#identify if user win the lotte with the rules below
    #same num and same sequence => 10,000
    #same num but different sequence =>3,000
    #if only 1 num same with the generated num =>1,000

#import library
import random

#generate nums without repeat
gen_num = [0,1,2,3,4,5,6,7,8,9]
random.shuffle(gen_num)
print(gen_num)
input_num=[]*2
input_num = eval(input("Pls enter 2 numbers: "))

#check if 2 numbers inputted
if len(input_num)!=2:
    print("Wrong quantity, pls enter 2 numbers, program exit.")
    exit()

#check if 2 numbers are the same
if input_num[0]==input_num[1]:
    print("You have inputted 2 same numbers, program exit.")
    exit()

#check if numbers out of the range(0-9)
if (input_num[0]>9 or input_num[0]<0 or input_num[1]>9 or input_num[1]<0):
    print("Pls enter numbers within 0-9, program exit")
    exit()

#check if the numbers are in same sequence and same num
prize = 0
if (input_num[0]==gen_num[0] and input_num[1]==gen_num[1]):
    prize = 10000
elif (input_num[0]==gen_num[1] and input_num[1]==gen_num[0]):
    prize = 3000
elif (input_num[0]==gen_num[1] or input_num[1]==gen_num[0] or
      input_num[0]==gen_num[0] or input_num[1]==gen_num[1]):
    prize = 1000

print("Your inputted num are: ", input_num[0], ",", input_num[1])
print("Lucky nums of this term are: ", gen_num[0], ",", gen_num[1])
if prize > 0:
    print("Congratulations! You won " , prize)
else:
    print("Sorry, you didn't win this time.")
