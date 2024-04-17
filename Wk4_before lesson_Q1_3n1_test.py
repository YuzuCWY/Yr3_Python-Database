def checkseq(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

contin = "T"

# Test the code
while (contin == "T"):
    number1, number2 = eval(input("Enter a pair positive integers seperate with comma: (i.e. 1,10) "))
    temp = 0
    longest = 0
    if number1>number2:
        temp = number1
        number1 = number2
        number2 = temp
    for i in range (number1, number2):
        sequence = checkseq(i)
        #print("sequence:", sequence)
        #print("length: ", len(sequence))
        if (longest<len(sequence)):
            longest = len(sequence)

    print("longest length is: ", longest)
    contin = input("pls enter T to continue of F to exit: ")
