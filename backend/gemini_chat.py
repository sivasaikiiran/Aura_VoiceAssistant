import google.generativeai as genai
from speak_engine import speak, listen

def start_gemini_chat():
    genai.configure(api_key="Api_key")
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat()

    speak("Gemini chat started. Say 'exit' to stop.")

    while True:
        user_input = listen()
        if user_input is None:
            print("⚠️ [System] No input detected.")
            speak("Sorry, I didn't catch that. Please try again or say 'exit' to quit.")
            continue
            
        if "exit" in user_input:
            speak("Exiting Gemini chat.")
            break
            
        response = chat.send_message(user_input)
        print("Gemini:", response.text)
        speak(response.text)