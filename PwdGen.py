import random
while True:
    usable="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890?!_*#"
    amount = int(input("How long is your password going to be?: "))
    print("1 - Slow, print as you go.")
    print("2 - Fast, print when done.")
    version = input("Which Version no: ")
    if version == "1":
        for a in range(1,amount + 1):
            i = random.randint(0,len(usable)-1)
            print(usable[i],end="")
        print("\n")
    elif version == "2":
        generatedpwd = ""
        for b in range(1,amount + 1):
            i = random.randint(0,len(usable)-1)
            generatedpwd += usable[i]
        print(generatedpwd,"\n")
    else:
        print("Error. Please try again.")


