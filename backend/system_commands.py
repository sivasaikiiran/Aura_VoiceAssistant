import os
from speak_engine import speak, listen
import time

CONFIRM_WORDS = ["yes", "ok", "okay", "alright", "confirm"]
TIMEOUT = 5  # Timeout for listening

def shutdown():
    speak("Are you sure you want to shut down the computer? You can say yes, okay, alright, or confirm — or say no to cancel.")
    
    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        confirm = listen()
        if confirm:
            if any(word in confirm.lower() for word in CONFIRM_WORDS):
                speak("Shutting down in 5 seconds.")
                os.system("shutdown /s /t 5")
                return
            elif "no" in confirm.lower():
                speak("Shutdown cancelled.")
                return
        speak("I didn't catch that. Please say yes, okay, alright, or confirm to proceed, or no to cancel.")
    
    speak("No response detected. Shutdown cancelled.")

def restart():
    speak("Are you sure you want to restart the computer? You can say yes, okay, alright, or confirm — or say no to cancel.")
    
    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        confirm = listen()
        if confirm:
            if any(word in confirm.lower() for word in CONFIRM_WORDS):
                speak("Restarting your computer in 5 seconds.")
                os.system("shutdown /r /t 5")
                return
            elif "no" in confirm.lower():
                speak("Restart cancelled.")
                return
        speak("I didn't catch that. Please say yes, okay, alright, or confirm to proceed, or no to cancel.")
    
    speak("No response detected. Restart cancelled.")
