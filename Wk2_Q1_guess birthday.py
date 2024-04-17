#By providing 5 sets of data, ask someone which set(s) contain his/her birth day

#Requirements: how I interpret and design the code below
#Input
#Output
#Design code base on ppt 


#print the sets
print(" 1  3  5  7"+ "\n"
      " 9 11 13 15"+ "\n"
      "17 19 21 23"+ "\n"
      "25 27 29 31"+ "\n"
      "Set 1" +"\n")

print(" 2  3  6  7"+ "\n"
      "10 11 14 15"+ "\n"
      "18 19 22 23"+ "\n"
      "26 27 30 31"+ "\n"
      "Set 2" +"\n")

print(" 4  5  6  7"+ "\n"
      "12 13 14 15"+ "\n"
      "20 21 22 23"+ "\n"
      "28 29 30 31"+ "\n"
      "Set 3" +"\n")

print(" 8  9 10 11"+"\n"
      "12 13 14 15"+"\n"
      "24 25 26 27"+"\n"
      "28 29 30 31"+"\n"
      "Set 4" +"\n")

print("16 17 18 19"+"\n"
      "20 21 22 23"+"\n"
      "24 25 26 27"+"\n"
      "28 29 30 31"+"\n"
      "Set 5" +"\n")

#Ask for input
input_counter = eval(input("If the sets below contain your birth day,"+
                    "pls enter the number of sets: "))
  

#check input
if input_counter<=0 or input_counter>5:
    print("Pls enter an integer between 1-5. Program Exited.")
    exit()

#create array base on input num
data = [0]*input_counter

#ask for input: which set(s)
for i in range (input_counter):
    num=eval(input("Set: "))
    if (0<num<=5):
        data[i]=num
    else:
        print("wrong number. Program exited.")
        exit()
    #print(data)

#Start the guess by calculate
guess_day = 0

#set the condition, if true, add the num
for i in range(input_counter):
    #print(i)
    if (data[i]==1):
        guess_day+=1
    elif (data[i]==2):
        guess_day+=2
    elif (data[i]==3):
        guess_day+=4
    elif (data[i]==4):
        guess_day+=8
    elif (data[i]==5):
        guess_day+=16

        
#print result
print("Your birth day is on ", guess_day, ".")
        

    
