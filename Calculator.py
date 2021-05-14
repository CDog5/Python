import sys, time, os
def mult(a,b):
    return a*b
def div(a,b):
    return a/b
def add(a,b):
    return a+b
def sub(a,b):
    return a-b

while True:
    print("Select an option: ")
    print("1-Division")
    print("2-Multiplication")
    print("3-Addition")
    print("4-Subtraction")
    print("5-Fibonacci")
    print("6-Exit")
    print("7-Clear Screen")
    print("8-Percentage Calculator")
    choice = int(input("Choice: "))
    if choice == 1:
            num1 = float(input("First number: "))
            num2 = float(input("Second number: "))
            print(num1,"/",num2,"=",div(num1,num2))
    elif choice == 2:
            num1 = float(input("First number: "))
            num2 = float(input("Second number: "))
            print(num1,"*",num2,"=",mult(num1,num2))

    elif choice == 3:
            num1 = float(input("First number: "))
            num2 = float(input("Second number: "))
            print(num1,"+",num2,"=",add(num1,num2))

    elif choice == 4:
            num1 = float(input("First number: "))
            num2 = float(input("Second number: "))
            print(num1,"-",num2,"=",sub(num1,num2))

    elif choice == 5:
            maxterms = 80
            print("The max amount of terms is",maxterms,".")
            nterms = int(input("How many terms?: "))
            n1 = float(input("Start no: "))
            fibonacci = []
            if nterms > maxterms:
                nterms = 80
            # first two terms
            n2 = n1
            count = 0

            # check if the number of terms is valid
            if nterms <= 0:
               print("Please enter a positive integer")
            elif nterms == 1:
               print("Fibonacci sequence up to",nterms,":")
               fibonacci.append(n1)
            else:
               print("Fibonacci sequence:")
               while count < nterms:
                   fibonacci.append(n1)
                   nth = n1 + n2
                   
                   n1 = n2
                   n2 = nth
                   count += 1
            if count == nterms:
                print(*fibonacci, sep = ", ")
                print("\n")
              
    elif choice == 6:
              sys.exit(0)

    elif choice == 7:
            os.system("cls")
    elif choice == 8:
        num1 = float(input("Number: "))
        num2 = float(input("What percent?: "))
        print(num2,"% of is ",(num1/100)*num2)
