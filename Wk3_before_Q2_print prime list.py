#Wk3 before lesson
#Q2 print 50 prime numbers
#5 rows 10 columns, 50 in total

#setting up variables
counter = 0     #count for prime numbers
i = 1           #counter
primelist = []  #build an array to store prime numbers

#while loop will stop if it got 50 prime numbers
while (counter<50):
    if (i<10):
        if (i==2 or i==3 or i==5 or i==7):
            counter+=1
            primelist.append(i)
        i+=1
    elif (i>=10):
        jcounter=0
        jlist=[]
        for j in range (1,i+1):
            if (i%j==0):
                jcounter+=1
                jlist.append(j)
        if jcounter<3:
            counter+=1
            primelist.append(i)
        i+=1

#print the prime numbers with format
#the greater the digits, with less space at front       
for i in range (5):
    for j in range (10):
        print(format(primelist[i*10+j], '4d'), end =' ')
    print()
