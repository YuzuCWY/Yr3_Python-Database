#Wk 6 before lesson
#Q1 check number if in range 1-99

global input_list
global ans_list
global default_num
global input_num
global ans

input_list = []
ans_list = []
default_num = 1,1,1,1,1,1,1,1,1,1
input_num = default_num
i = 0
ans = "Yes"

def AskForInput():
    global input_list
    global ans_list
    global default_num
    global input_num
    global ans
    while (input_num != 0 and len(input_num)==10):
        input_num = eval(input("Pls enter 10 numbers within 1-99, pls add comma between the nums: "))

        if (type(input_num)==int):
            if (input_num==0):
                break
            print("You just input a number only," +
                  "pls enter 10 nums, and this num will not be recorded.")
            input_num = default_num
            continue
        elif(type(input_num)==tuple):
            if (len(input_num)==10):
                input_list.append(input_num)
            else:
                print("You didn't input 10 numbers ," +
                "pls enter 10 nums, and these nums will not be recorded. "+
                "Pls re-enter.")
            input_num = default_num 

def do_check():
    global input_list
    global ans_list
    global default_num
    global input_num
    global ans
    for i in range(len(input_list)):
        for j in range (len(input_list[i])):
            #print(input_list[i][j])
            if (1>input_list[i][j] or input_list[i][j]>99):
                ans = "No"
                ans_list.append(input_list[i])
                i+=1

AskForInput()
do_check()

print()
print("Your input are as followings:" )
print(input_list)
print()
print("Do all the input numbers within 1-99? " + ans)

if (ans=="No"):
    print("Below is the set(s) which contain(s) numbers out of 1-99: ")
    print(ans_list)
