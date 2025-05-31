from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from speak_engine import speak, listen

def collect_contact_and_message():
    contact_name = None
    message = None

    # Collect contact name
    while not contact_name:
        speak("Please say the contact name you want to send a message to.")
        contact_name = listen()
        if not contact_name:
            speak("I didn't catch the contact name. Please try again.")

    # Collect message
    while not message:
        speak("What message would you like to send?")
        message = listen()
        if not message:
            speak("I didn't catch the message. Please try again.")

    return contact_name, message

def whatsapp_send(contact_name, message):
    driver_path = r"path_to_chromedriver"  # Update with your actual path to chromedriver
    service = Service(driver_path)

    options = Options()
    options.add_argument("--user-data-dir=path_to_chrome_user_data")  # Update with your actual path to Chrome user data
    options.add_argument("--profile-directory=Default")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://web.whatsapp.com')

    speak("Please scan the QR code in the browser if not already logged in.")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
    )
    time.sleep(5)  # Give a few extra seconds to fully load

    try:
        search_box_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
        matched_contact = None

        while not matched_contact:
            # Search the contact
            search_box = driver.find_element(By.XPATH, search_box_xpath)
            search_box.clear()
            time.sleep(1)
            search_box.send_keys(contact_name)
            time.sleep(3)  # Let WhatsApp search

            try:
                # Find contact ignoring capital/small letters
                contact_xpath = f'//span[@title][contains(translate(@title, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{contact_name.lower()}")]'
                contact_element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, contact_xpath))
                )
                matched_contact = contact_element.text
                contact_element.click()
                speak(f"Found {matched_contact}. Sending your message.")
            except:
                speak(f"Couldn't find the contact {contact_name}. Deleting the search and asking again.")
                contact_name = None

                # Ask only for the contact name again
                while not contact_name:
                    speak("Please say the contact name you want to send the message to.")
                    contact_name = listen()
                    if not contact_name:
                        speak("I didn't catch the contact name. Please try again.")

        # Send the previously collected message
        msg_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        msg_box.send_keys(message)
        time.sleep(1)

        send_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
        )
        send_btn.click()

        speak(f"Message successfully sent to {matched_contact}!")

    except Exception as e:
        speak("Something went wrong while sending the message.")
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

def send_whatsapp_message():
    contact_name, message = collect_contact_and_message()
    whatsapp_send(contact_name, message)
