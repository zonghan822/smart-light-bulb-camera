""""Jarvis" voice assistant.

Listens for the wake word, recognises a spoken command and replies with
text-to-speech. Device commands ("turn on the camera", "light off", ...)
print a fixed reply such as "Camera On." to stdout, which the Node-RED
"Command" switch node maps to the matching dashboard switch.
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import date, timedelta, datetime
import operator  # used for math operations
import random  # will be used throughout for random response choices
import os  # used to interact with the computer's directory

# Speech Recognition Constants
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Python Text-to-Speech (pyttsx3) Constants
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)

# Wake word in Listen Function
WAKE = "Jarvis"
# Initial analysis of words that would typically require a Google search
SEARCH_WORDS = {"who": "who", "what": "what", "when": "when", "where": "where", "why": "why", "how": "how"}


class Jarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    # Used to hear the commands after the wake word has been said
    def hear(self, recognizer, microphone, response):
        try:
            with microphone as source:
                print("Waiting for command...")
                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000
                # May reduce the time out in the future
                audio = recognizer.listen(source, timeout=5.0)
                command = recognizer.recognize_google(audio)
                return command.lower()
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Network error.")

    # Used to speak to the user
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    # Used to control light
    def light_control(self, command):
        # Will need to expand on "light" commands
        if "on" in command or "open" in command:
            print("Light On.", end="")
            s.speak("Light On.")
            pass

        elif "off" in command or "close" in command:
            print("Light Off.", end="")
            s.speak("Light Off.")
            pass

        else:
            print("I don't know how to do that yet.")
            s.speak("I don't know how to do that yet.")
            pass

    # Used to control camera
    def camera_control(self, command):
        # Will need to expand on "camera" commands
        if "on" in command or "open" in command:
            print("Camera On.", end="")
            s.speak("Camera On.")
            pass

        elif "off" in command or "close" in command:
            print("Camera Off.", end="")
            s.speak("Camera Off.")
            pass

        else:
            print("I don't know how to do that yet.")
            s.speak("I don't know how to do that yet.")
            pass

    # Used to control LDR
    def ldr_control(self, command):
        # Will need to expand on "ldr" commands
        if "on" in command or "open" in command:
            print("Light Sensor On.", end="")
            s.speak("Light Sensor On.")
            pass

        elif "off" in command or "close" in command:
            print("Light Sensor Off.", end="")
            s.speak("Light Sensor Off.")
            pass

        else:
            print("I don't know how to do that yet.")
            s.speak("I don't know how to do that yet.")
            pass

    # Used to open the browser or specific folders
    def open_things(self, command):
        # Will need to expand on "open" commands
        if command == "open youtube":
            print("Opening YouTube.")
            s.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
            pass

        elif command == "open facebook":
            print("Opening Facebook.")
            s.speak("Opening Facebook.")
            webbrowser.open("https://www.facebook.com")
            pass

        else:
            print("I don't know how to open that yet.")
            s.speak("I don't know how to open that yet.")
            pass

    # Used to answer time/date questions
    def understand_time(self, command):
        today = date.today()
        now = datetime.now()
        if "today" in command:
            print("Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y"))
            s.speak("Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y"))

        elif command == "what time is it":
            print("It is " + now.strftime("%I") + now.strftime("%M") + now.strftime("%p") + ".")
            s.speak("It is " + now.strftime("%I") + now.strftime("%M") + now.strftime("%p") + ".")

        elif "yesterday" in command:
            date_intent = today - timedelta(days=1)
            return date_intent

        elif "this time last year" in command:
            current_year = today.year

            if current_year % 4 == 0:
                days_in_current_year = 366

            else:
                days_in_current_year = 365
            date_intent = today - timedelta(days=days_in_current_year)
            return date_intent

        elif "last week" in command:
            date_intent = today - timedelta(days=7)
            return date_intent
        else:
            pass

    # If we're doing math, this will return the operand to do math with
    def get_operator(self, op):
        return {
            '+': operator.add,
            '-': operator.sub,
            'x': operator.mul,
            'divided': operator.__truediv__,
            'Mod': operator.mod,
            'mod': operator.mod,
            '^': operator.xor,
        }[op]

    # We'll need a list to perform the math
    def do_math(self, li):
        # passes the second item in our list to get the built-in function operand
        op = self.get_operator(li[1])
        # changes the strings in the list to integers
        int1, int2 = int(li[0]), int(li[2])
        # this uses the operand from the get_operator function against the two intengers
        result = op(int1, int2)
        print(str(int1) + " " + li[1] + " " + str(int2) + " equals " + str(result))
        s.speak(str(int1) + " " + li[1] + " " + str(int2) + " equals " + str(result))

    # Checks "what is" to see if we're doing math
    def what_is_checker(self, command):
        number_list = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        # First, we'll make a list a out of the string
        li = list(command.split(" "))
        # Then we'll delete the "what" and "is" from the list
        del li[0:2]

        if li[0] in number_list:
            self.do_math(li)

        elif "what is the date today" in command:
            self.understand_time(command)

        else:
            self.use_search_words(command)

    # Checks the first word in the command to determine if it's a search word
    def use_search_words(self, command):
        print("Here is what I found.")
        s.speak("Here is what I found.")
        webbrowser.open("https://www.google.com/search?q={}".format(command))

    # Analyzes the command
    def analyze(self, command):
        try:
            if "sensor" in command:
                self.ldr_control(command)

            elif "camera" in command:
                self.camera_control(command)

            elif "light" in command:
                self.light_control(command)

            elif command.startswith('open'):
                self.open_things(command)

            elif command == "introduce yourself" or "who are you" in command:
                print("I am Jarvis. I'm a digital assistant.")
                s.speak("I am Jarvis. I'm a digital assistant.")

            elif command == "what time is it":
                self.understand_time(command)

            elif command == "how are you":
                current_feelings = ["I'm okay.", "I'm doing well. Thank you.", "I am doing okay."]
                # selects a random choice of greetings
                greeting = random.choice(current_feelings)
                print(greeting)
                s.speak(greeting)

            elif "what is" in command:
                self.what_is_checker(command)

            # Keep this at the end
            elif SEARCH_WORDS.get(command.split(' ')[0]) == command.split(' ')[0]:
                self.use_search_words(command)

            elif command == "exit" or "bye" in command:
                print("Good Bye.")
                s.speak("Good Bye.")

            else:
                print("I don't know how to do that yet.")
                s.speak("I don't know how to do that yet.")

        except TypeError:
            print("Warning: You're getting a TypeError somewhere.")
            pass
        except AttributeError:
            print("Warning: You're getting an Attribute Error somewhere.")
            pass

    # Used to listen for the wake word
    def listen(self, recognizer, microphone):
        while True:
            try:
                with microphone as source:
                    print("Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.dynamic_energy_threshold = 3000
                    audio = recognizer.listen(source, timeout=3.0)
                    response = recognizer.recognize_google(audio)

                    if WAKE in response:
                        print("How can I help you?")
                        s.speak("How can I help you?")
                        return response.lower()

                    else:
                        pass
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Network error.")


s = Jarvis()
while True:
    response = s.listen(recognizer, microphone)
    command = s.hear(recognizer, microphone, response)
    s.analyze(command)