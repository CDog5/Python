import sys,time,signal
loop = True
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
def getMessage():
   msg = input('Please enter a message: ')
   msg = msg.lower()
   return msg
while loop:
        time.sleep(1)
        print("Choose an option:")
        print("\n1 - Encrypt")
        print("2 - Decrypt")
        print("3 - Force Decrypt")
        print("4 - Exit\n")
        mode = input("")
         

        if "1" in mode:
                loop = False
                newMessage = ''
                message = getMessage()
                key = int(input('Please enter a key: '))
                for character in message:
                 if character in ALPHABET:
                  position = ALPHABET.find(character)
                  newPosition = (position + key) % 26
                  newCharacter = ALPHABET [newPosition]
                  newMessage += newCharacter
                 else:
                        newMessage += character
                print('Your new message is: ' + newMessage)
                loop = True

        elif "2" in mode:
                loop = False
                newMessage = ''
                message = getMessage()
                key = int(input('Please enter a key: '))
                for character in message:
                 if character in ALPHABET:
                  position = ALPHABET.find(character)
                  newPosition = (position - key) % 26
                  newCharacter = ALPHABET[newPosition]
                  newMessage += newCharacter
                 else:
                        newMessage += character

                print('Your new message is: ' + newMessage)
                loop = True

        elif "3" in mode:
                loop = True
                newMessage = ''
                message = getMessage()

                for key in range(1,25):
                        for character in message:
                         if character in ALPHABET:
                                position = ALPHABET.find(character)
                                newPosition = (position + key) % 26
                                newCharacter = ALPHABET[newPosition]
                                newMessage += newCharacter
                         else:
                                newMessage += character
                        print(str(key) + ":" + newMessage)
                        newMessage = ""
                        loop = True

        elif "4" in mode:
                loop = False
                time.sleep(0.5)
                sys.exit(0)
        else:
                print("Unknown input. Please try again.")
