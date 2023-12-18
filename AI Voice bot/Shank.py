import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = sr.Recognizer()
engine = pyttsx3.init()

#voice changing 
voices = engine.getProperty('voices')

engine.setProperty('voice',voices[0].id)

def intro():
    engine.say("Hii I'm Shank")
    engine.say("What can I do for you")
    engine.runAndWait()

def ans(text):
    engine.say(text)
    engine.runAndWait()

def take_command(n):
    try:
        with sr.Microphone() as source:
            if(n==1):
                intro()
                print("n: ",n)
                n+=1
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            if 'shank'in command:
                command = command.replace('shank','')
                print("n: ",n)
            return (n,command)
    except:
        ans("Sorry, I don't Understand.")
        print("n: ",n)
        return (n,'')
        

def run_shank(n):
    m,command = take_command(n)
    if command == '':
        pass

    try:

        if 'play' in command:
            song = command.replace('play','')
            ans(f"Playing {command}")
            pywhatkit.playonyt(command)
            print("m: ",m)
            return m

        elif 'time' in command:
            time  = datetime.datetime.now().strftime('%I:%M %p')
            ans(f'Current time is {time}')
            print("m: ",m)
            return m
        
        elif 'exit' in command:
            ans(f'Thank you for your time. Visit again')
            print("m: ",m)
            return 0
        else:
            info = wikipedia.summary(command,3)
            ans(info)
            print("m: ",m)
            return m
    except:
        ans("Sorry, I don't Understand.")
        return m


n=1
while True:
    n = run_shank(n)
    if(n==0):
        break