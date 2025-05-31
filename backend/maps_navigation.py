import webbrowser
from speak_engine import speak, listen

def get_directions():
    while True:
        speak("Where are you starting from?")
        origin = listen()
        
        if not origin:
            speak("I couldn't hear the origin. Please try again.")
            continue

        speak("What is your destination?")
        destination = listen()

        if not destination:
            speak("I couldn't hear the destination. Please try again.")
            continue

        # If both origin and destination are valid, exit the loop
        speak(f"Getting directions from {origin} to {destination}. Opening in browser.")
        maps_url = f"https://www.google.com/maps/dir/{origin}/{destination}"
        webbrowser.open(maps_url)
        break  # Exit the loop after the valid input is processed
