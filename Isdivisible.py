while True:
    print("Check if number 1 is divisible by number 2.")
    no1 = float(input("No 1: "))
    no2 = float(input("No 2: "))
    if no1 % no2 == 0:
        print(no1,"is divisible by",no2)
    else:
        print(no1,"isn't divisible by",no2)
