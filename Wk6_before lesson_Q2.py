#Wk6 before lesson
#Q2 Use Slicing to shift left or right

def shiftLeft(LIST, seq):
    for j in range (seq):
        temp = LIST[0]
        for i in range (1, len(LIST)):
            LIST[i-1] = LIST[i]
        LIST[len(LIST)-1] = temp
    print(LIST)

def shiftRight(LIST, seq):
    for j in range (seq):
        temp = LIST[-1]
        for i in range (1,len(LIST)):
            LIST[-i] = LIST[-i-1]
        LIST[0] = temp
    print(LIST)

mylist = [0,1,2,3,4,5,6,7,8,9]

print()
print(mylist)
seq = int(input("Shift left: "))
shiftLeft(mylist, seq)

seq = int(input("Shift right: "))
shiftRight(mylist, seq)

