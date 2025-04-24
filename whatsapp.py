from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fuzzywuzzy import process
import time
from speak_engine import speak, listen

def get_matching_contact(contact_name, contact_list):
    # Use fuzzy matching to find the closest contact name from the list
    best_match = process.extractOne(contact_name, contact_list)
    
    # If the match score is greater than 40%, return the best match, else return None
    if best_match and best_match[1] >= 40:
        return best_match[0]
    else:
        return None

def whatsapp_send(name, msg):
    driver_path = r"C:\Users\msski\Downloads\project\backend\chromedriver.exe"
    service = Service(driver_path)

    options = Options()
    options.add_argument("--user-data-dir=C:/Users/msski/AppData/Local/Google/Chrome/User Data")
    options.add_argument("--profile-directory=Default")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://web.whatsapp.com')

    speak("Please scan the QR code in the browser if not already logged in.")
    time.sleep(15)  # Give user time to scan QR code (adjustable)

    try:
        # Wait for the search box to become visible (explicit wait with a timeout of 10 seconds)
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.click()
        time.sleep(1)

        # Listen for the contact name
        speak("Please say the contact name you want to send a message to.")
        contact_name = listen()

        if not contact_name:
            speak("I didn't catch the contact name. Please try again.")
            return

        # Search for all contacts on WhatsApp Web (this part might vary based on WhatsApp's structure)
        contact_elements = driver.find_elements(By.XPATH, '//span[@title]')
        contact_list = [contact.text for contact in contact_elements]

        # Find the best match from the contact list
        matched_contact = get_matching_contact(contact_name, contact_list)

        if matched_contact:
            speak(f"Found a match: {matched_contact}. Sending your message.")
            # Type the matched contact name into the search box
            search_box.send_keys(matched_contact)
            time.sleep(3)

            # Wait for the contact to be clickable
            contact_xpath = f'//span[contains(@title, "{matched_contact}")]'
            user = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, contact_xpath))
            )
            user.click()
            time.sleep(2)

            # Wait for the message box to be ready
            msg_box = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            msg_box.send_keys(msg)
            time.sleep(1)

            # Wait for the send button to be clickable
            send_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_btn.click()

            speak(f"Message sent to {matched_contact}.")
        else:
            speak("Sorry, I couldn't find a matching contact.")

    except Exception as e:
        speak("Something went wrong while sending the message.")
        print(f"❌ Error: {e}")
    finally:
        driver.quit()


def askinfo():
    speak("What message would you like to send?")
    message = listen()

    if not message:
        speak("I didn't catch the message. Please try again.")
        return

    whatsapp_send("your contact", message)