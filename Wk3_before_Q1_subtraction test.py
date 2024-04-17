#Wk3 before lesson
#Q1 create several questions regarding subtraction
# record total test time and number of correct

#import library
import time
import random

#Generate the quantity of questions randomly
NumOfQ = random.randint(1,10)
print(NumOfQ, " questions are generated.")

#default setting and start the timer
Round = 0
Correct = 0
start = time.time()

#using while loop to ask for answers
while (Round<NumOfQ):
    minuend = random.randint(1,100)
    subtractend = random.randint(1,100)
    print("Question", Round+1 , ": ", minuend , "-", subtractend, "= ")
    ans = int(input())


    if (ans==minuend-subtractend):
        Correct+=1
    Round+=1

#stop the timer after questions are completed 
end = time.time()
elapsed_time = int(end-start)
formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

#print result
print("Correct: ", Correct)
print("You took ", formatted_time, " to finish the test.")
