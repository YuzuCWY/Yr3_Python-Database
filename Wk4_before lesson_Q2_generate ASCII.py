#Wk4 before lesson
#Q2 random generate ASCII

import random
import string

def generate_random_ascii(choice):
    if choice == 1:
        # Generate any ASCII code
        return chr(random.randint(33, 127))
    elif choice == 2:
        # Generate a random number (ASCII digits)
        return chr(random.randint(48, 57))
    elif choice == 3:
        # Generate a random capital letter
        return random.choice(string.ascii_uppercase)
    elif choice == 4:
        # Generate a random small letter
        return random.choice(string.ascii_lowercase)
    else:
        return "Invalid choice"

# Input from the user
contin = "T"
while (contin =="T"):
    choice = int(input("Enter your choice (1-4):\n1) Any ASCII code\n2) Any numbers\n3) Any Capital letters\n4) Any small letters\n"))

    if 1 <= choice <= 4:
        random_ascii = generate_random_ascii(choice)
        print("Random ASCII character: " + random_ascii)
    else:
        print("Invalid choice. Please choose between 1 and 4.")
    contin = input("Pls enter T to continue or F to exit: ")
