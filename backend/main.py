import os
import time
import sys
import pyautogui
import psutil
import requests

from speak_engine import speak, listen as take_command
from gemini_chat import start_gemini_chat
from gmail_sender import send_mail
from doc_reader import choose_doc_reader
from whatsapp import send_whatsapp_message  
from system_commands import shutdown, restart
from maps_navigation import get_directions
from search_assistant import search_youtube, search_google, search_wikipedia  

def get_user_country():
    try:
        ip_info = requests.get("https://ipinfo.io/json").json()
        country_code = ip_info.get("country", "us").lower()
        return country_code
    except:
        return "us"

def get_weather():
    speak("Please tell me the city name.")
    city = take_command()
    if city:
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            geo_response = requests.get(geo_url).json()

            if "results" in geo_response and len(geo_response["results"]) > 0:
                lat = geo_response["results"][0]["latitude"]
                lon = geo_response["results"][0]["longitude"]
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_response = requests.get(weather_url).json()

                temperature = weather_response["current_weather"]["temperature"]
                windspeed = weather_response["current_weather"]["windspeed"]

                speak(f"The temperature in {city} is {temperature} degrees Celsius with a wind speed of {windspeed} kilometers per hour.")
            else:
                speak("City not found. Please try again.")
        except requests.exceptions.RequestException:
            speak("Could not retrieve weather information.")

def get_definition(query):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
        speak(f"The definition of {query} is: {meaning}")
    else:
        speak("Sorry, I couldn't find the definition for that word.")

def answer_question(command):
    if "weather" in command:
        get_weather()
    elif "define" in command:
        word = command.split("define")[-1].strip()
        get_definition(word)
    else:
        speak("Sorry, I couldn't find an answer to your question.")

def put_system_to_sleep():
    speak("Putting the system to sleep. Goodbye!")
    time.sleep(1)
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    sys.exit()

def hibernate_system():
    speak("Hibernating the system. Goodbye!")
    time.sleep(1)
    os.system("shutdown /h")
    sys.exit()

def lock_system():
    speak("Locking the system. Goodbye!")
    time.sleep(1)
    os.system("rundll32.exe user32.dll,LockWorkStation")
    sys.exit()

def check_battery():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = "charging" if battery.power_plugged else "not charging"
        response = f"Battery is at {percent}% and it is {plugged}."
        speak(response)
    else:
        speak("Sorry, I couldn't access the battery status.")

def take_screenshot():
    screenshot_path = os.path.join(os.path.expanduser("~"), "Desktop", f"screenshot_{int(time.time())}.png")
    pyautogui.screenshot(screenshot_path)
    speak("Screenshot taken and saved to your desktop.")

def analyze_command(command):
    if "gemini" in command:
        return "Opening Gemini chat."
    elif "email" in command or "gmail" in command:
        return "Preparing to send an email."
    elif "document" in command or "pdf" in command or "word" in command:
        return "Launching the document reader."
    elif "whatsapp" in command:
        return "Sending a WhatsApp message."
    elif "google" in command:
        return "Searching Google."
    elif "youtube" in command or "play song" in command:
        return "Searching YouTube for a song."
    elif "shutdown" in command:
        return "Preparing to shut down."
    elif "restart" in command:
        return "Preparing to restart."
    elif "sleep" in command:
        return "Putting system to sleep."
    elif "hibernate" in command:
        return "Hibernating the system."
    elif "lock" in command:
        return "Locking the system."
    elif "battery" in command:
        return "Checking battery status."
    elif "screenshot" in command:
        return "Taking a screenshot."
    elif "navigate" in command or "direction" in command or "route" in command:
        return "Getting directions to your destination."
    elif any(kw in command for kw in ["weather", "define"]):
        return "Fetching information for your query."
    elif any(kw in command for kw in ["stop", "quit", "exit"]):
        return "Exiting the assistant."
    elif any(kw in command for kw in ["cancel", "nevermind", "don't"]):
        return "Cancelling the current request."
    else:
        return "Unknown command. Awaiting valid input."

def main():
    speak("Welcome! I am your Aura voice assistant.")

    while True:
        speak("What would you like me to do?")
        print("\n🎤 [System] Listening for a command...")
        command = take_command()

        if not command:
            speak("Sorry, I didn't catch that.")
            continue

        print(f"🧠 Interpreted command: \"{command}\"")
        action_feedback = analyze_command(command)
        print(f"📌 [Intent Recognition] {action_feedback}")

        if any(kw in command for kw in ["cancel", "nevermind", "don't"]):
            speak("Okay, cancelled the current request.")
            continue

        if "gemini" in command:
            start_gemini_chat()
        elif "email" in command or "gmail" in command:
            send_mail()
        elif "document" in command or "pdf" in command or "word" in command:
            choose_doc_reader()
        elif "whatsapp" in command:
            send_whatsapp_message()  
        elif "google" in command:
            speak("What would you like me to search on Google?")
            query = take_command()
            if query:
                search_google(query)  
        elif "youtube" in command or "play song" in command:
            speak("What song or YouTube video would you like me to play on YouTube?")
            query = take_command()
            if query:
                search_youtube(query)  
        elif "wikipedia" in command:
            speak("What would you like me to search on Wikipedia?")
            query = take_command()
            if query:
                search_wikipedia(query)  
        elif "shutdown" in command:
            shutdown()
        elif "restart" in command:
            restart()
        elif "sleep" in command:
            put_system_to_sleep()
        elif "hibernate" in command:
            hibernate_system()
        elif "lock" in command:
            lock_system()
        elif "battery" in command:
            check_battery()
        elif "screenshot" in command:
            take_screenshot()
        elif "navigate" in command or "direction" in command or "route" in command:
            get_directions()
        elif any(kw in command for kw in ["weather", "define"]):
            answer_question(command)
        elif any(kw in command for kw in ["exit", "quit", "stop"]):
            speak("Thank you for using Aura. Goodbye!")
            break
        else:
            speak("Sorry, I don't understand that command.")

if __name__ == "__main__":
    main()

