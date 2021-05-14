import shopdata
balance = int(100)
bag = []
item1 =  shopdata.Item()
item2 = shopdata.Item()

while True:
    shopdata.clear()
    print("Shop: ")
    print(item1.displayinfo())
    print(item2.displayinfo())
    print("Your Balance:",balance)

    text = input("Action:").lower()
    if text == "buy "+ item1.name:
            balance -= item1.value
            bag.append(item1.name.title())
            print("Balance: ",balance)
            print("Bag:")
            print(*bag ,sep = ", ")
            shopdata.Wait(1.5)
    elif text == "buy "+ item2.name.lower():
            balance -= item2.value
            bag.append(item2.name.title())
            print("Balance: ",balance)
            print("Bag:")
            print(*bag,sep = ", ")
            shopdata.Wait(1.5)
    elif text == "sell "+ item1.name.lower():
            balance += item1.value
            bag.remove(item1.name.title())
            print("Balance: ",balance)
            print("Bag:")
            print(*bag ,sep = ", ")
            shopdata.Wait(1.5)
    elif text == "sell "+ item2.name.lower():
            balance += item2.value
            bag.remove(item2.name.title())
            print("Balance: ",balance)
            print("Bag:")
            print(*bag,sep = ", ")
            shopdata.Wait(1.5)
    elif text == "exit":
           shopdata.Quit()
    elif text == "new stock":
        item1 =  shopdata.Item()
        item2 = shopdata.Item()
        print("We have new stock!")
        shopdata.Wait(1)
    elif "buy " in text:
        print(text.replace("buy ",""),"isn't in stock.")
    else:
        print(text,"isn't an action or you have mistyped it.")
        shopdata.Wait(1.5)
        

