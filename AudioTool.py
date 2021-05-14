import os,sys,gtts as gTTS
from playsound import playsound
import speech_recognition as sr
def speechtotext(speechtype):
    if speechtype == "Mic":
        print("Speak")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source) 
            audio = r.listen(source)
            
        try:
            data = r.recognize_google(audio)
            print(data)
        except sr.UnknownValueError:
            print("error")
    else:
        file = input("What is the file name?: ")
        r = sr.Recognizer()
        with sr.AudioFile(file) as source:
            r.adjust_for_ambient_noise(source) 
            audio_data = r.listen(source)
            text = r.recognize_google(audio_data)
            print(text)
    
def texttospeech():
    filename = input("What should the file be called?: ")+".mp3"
    text = input("Enter text: ")
    tts = gTTS.gTTS(text=text,lang='en',slow=False)
    tts.save(filename)
    playsound(filename)
while True:
    print("1 - Text to speech")
    print("2 - Speech to text")
    print("3 - Exit")
    print("4 - Clear Screen")
    userinput = input("Choose a number: ")
    if "1" in userinput:
        texttospeech()
    elif "2" in userinput:
        print("1 - Audio file")
        print("2 - Microphone")
        userinput = input("Choose a number: ")
        if "1" in userinput:
            speechtotext("File")
        elif "2" in userinput:
            speechtotext("Mic")
    elif "3" in userinput:
        sys.exit(0)
    elif "4" in userinput:
        try:
            os.system("cls")
        except:
            print("Could not clear screen.")
    else:
        print(userinput," is not a valid option. Please try again.")
