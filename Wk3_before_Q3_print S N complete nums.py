#Wk3 before lesson
#Q3 user can keep input an integer to find whether
#   that integer is belong to 盈數/虧數/完全數

input_num = eval(input("Pls input an integer greater than 0: "))

while (input_num>0):
    
    temp_list = [0]
    temp_sum = 0

    for i in range (1, input_num):
        if (input_num%i==0):
            temp_list.append(i)
    
    for i in range(len(temp_list)):
        temp_sum = temp_sum + temp_list[i]
    
    if (temp_sum>input_num):
        print("Your input integer is a 盈數")
    elif(temp_sum==input_num):
        print("Your input integer is a 完全數")
    else:
        print("Your input integer is a 虧數")
    input_num = eval(input("Pls input an integer greater than 0: "))
