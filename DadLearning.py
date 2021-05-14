#modules are scripts we can import that help with tasks
import time
print(1)
#the program waits for 1 second before continuing
time.sleep(1)
print(2)
#variables can change type in python
testvar = "Hi"
print(testvar)
testvar  = 0
print(testvar)
condition = True
testlist=["a","b","c","d","e"]
#if - else statements
if condition:
    print("This is true!")
else:
    print("This is false!")
time.sleep(3)
#for loop
for item in testlist:
    print(item)
time.sleep(5)
for i in range(1,100):
    print(i)
time.sleep(3)
#while loop (Only runs when condition is true)
while condition:
    # the input function gets user input
    userinput = input("Type exit to break loop:")
    #the .lower and .upper functions convert strings to lower/upper
    if userinput.lower() == "exit":
        #break exits a loop. You could also change condition to false to exit the loop here
        break
#functions use the keyword def and can take in arguments
def examplefunction(example):
    #return sets the result to whatever is written
    return "This is a function with the argument "+example
print(examplefunction("Hi"))
#classes can be used multiple times
class Pet():
    #the init method is called when you create a new instance of the class
    def __init__(self,name,age):
        #self refers to this instance. Each instance has its own values to the variables
        self.name = name
        self.age = age
    def greeting(self):
        print("Hi, I'm ",self.name)
#classes can inherit other classes
class Cat(Pet):
    def __init__(self,name,age,colour):
        #runs the init method from the superclass, which would be Pet
        super().__init__(name,age)
        self.colour = colour
    def speak(self):
        print("Meow")
#create an instance of the Cat class in a variable
cat = Cat("Bob",7,"Brown")
#use the greeting function from the Pet class
cat.greeting()
#use the speak function from the cat class
#if you had a speak function in the pet class, the function in the cat class would override it.
cat.speak()
