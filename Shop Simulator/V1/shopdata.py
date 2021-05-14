import random,os,sys,time
clear = lambda: os.system("cls")
itemlist=["Strawberry","Banana","Peach","Pear","Plum"]
itemvalues=[10,3,6,9,5]
itemplantable=["Y","N","Y","N","N"]

class Item:
    def __init__(self):
        index = random.randint(0,len(itemlist)-1)
        self.name = itemlist[index].lower()
        self.value = itemvalues[index]
        self.plantable = itemplantable[index]
    def displayinfo(self):
        print("Name:",self.name.title())
        print("Value:",self.value)
        print("Is Plantable:",self.plantable," \n")
        return ""
def Clear():
    os.system("cls")
def Quit():
    sys.exit(0)
def Wait(wt):
    time.sleep(wt)
