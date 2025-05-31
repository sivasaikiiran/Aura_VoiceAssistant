from PyQt5.QtWidgets import QApplication, QFileDialog
from speak_engine import speak, listen
import pdfplumber
import docx
import os
import sys
from colorama import Fore
from rich.console import Console
from rich.table import Table

# File picker
def get_file(file_types):
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    file_path, _ = QFileDialog.getOpenFileName(None, "Select a File", "", file_types)
    return file_path

# Display book metadata
def book_details(author, title, total_pages):
    table = Table(title="Book Details", show_lines=True)
    table.add_column("No.", style="magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("1", "Title", title)
    table.add_row("2", "Author", author)
    table.add_row("3", "Pages", str(total_pages))
    console = Console()
    console.print(table)

# Extract page number from spoken command
def extract_page_number(command):
    try:
        return next(int(word) for word in command.split() if word.isdigit())
    except Exception:
        return None

# Read PDF using pdfplumber
def pdf_read():
    try:
        location = get_file("PDF Files (*.pdf)")
        if not location or not os.path.isfile(location):
            speak("File not found.")
            return

        with pdfplumber.open(location) as pdf:
            total_pages = len(pdf.pages)
            title = os.path.basename(location)
            author = "Unknown"  # pdfplumber doesn't extract metadata well

            book_details(author, title, total_pages)
            speak(f"Title: {title}")
            speak(f"Author: {author}")
            speak(f"Pages: {total_pages}")
            speak("Would you like a single page, a range, or the whole book?")

            while True:
                choice = listen()
                if not choice:
                    speak("Please say your choice again.")
                    continue

                choice = choice.lower()
                if "page" in choice:
                    speak("Which page number?")
                    page_no = extract_page_number(listen())
                    if page_no and 1 <= page_no <= total_pages:
                        text = pdf.pages[page_no - 1].extract_text()
                        print(f"\nPage {page_no}:\n{text}")
                        speak(text)
                        break
                    else:
                        speak("Invalid page number.")
                elif "range" in choice:
                    speak("Start page?")
                    start = extract_page_number(listen())
                    speak("End page?")
                    end = extract_page_number(listen())
                    if start and end and 1 <= start <= end <= total_pages:
                        for i in range(start - 1, end):
                            text = pdf.pages[i].extract_text()
                            print(f"\nPage {i+1}:\n{text}")
                            speak(text)
                        break
                    else:
                        speak("Invalid range.")
                elif "whole" in choice or "all" in choice:
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        print(f"\nPage {i+1}:\n{text}")
                        speak(text)
                    break
                else:
                    speak("Please say one page, range, or whole book.")
    except Exception as e:
        print(Fore.YELLOW + f"PDF Read Error: {e}")
        speak("Failed to read PDF.")

# Read Word DOCX
def ms_word():
    try:
        location = get_file("Word Documents (*.docx)")
        if not location or not os.path.isfile(location):
            speak("File not found.")
            return

        doc = docx.Document(location)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        total = len(paragraphs)

        speak(f"The document has {total} paragraphs.")
        speak("Would you like a specific paragraph, a range, or the whole document?")

        while True:
            choice = listen()
            if not choice:
                speak("Please say your choice again.")
                continue

            choice = choice.lower()
            if "paragraph" in choice or "single" in choice:
                speak("Which paragraph number?")
                p_no = extract_page_number(listen())
                if p_no and 1 <= p_no <= total:
                    text = paragraphs[p_no - 1]
                    print(f"\nParagraph {p_no}:\n{text}")
                    speak(text)
                    break
                else:
                    speak("Invalid paragraph number.")
            elif "range" in choice:
                speak("Start paragraph?")
                start = extract_page_number(listen())
                speak("End paragraph?")
                end = extract_page_number(listen())
                if start and end and 1 <= start <= end <= total:
                    for i in range(start - 1, end):
                        text = paragraphs[i]
                        print(f"\nParagraph {i+1}:\n{text}")
                        speak(text)
                    break
                else:
                    speak("Invalid range.")
            elif "whole" in choice or "all" in choice:
                for i, p in enumerate(paragraphs):
                    print(f"\nParagraph {i+1}:\n{p}")
                    speak(p)
                break
            else:
                speak("Please say paragraph number, range, or whole document.")
    except Exception as e:
        print(Fore.YELLOW + f"Word read error: {e}")
        speak("Could not read Word file.")

# Ask user to pick Word or PDF
def choose_doc_reader():
    speak("Would you like to read a Word document or a PDF?")
    while True:
        choice = listen()
        if not choice:
            speak("Please say PDF or Word.")
            continue
        choice = choice.lower()
        if "pdf" in choice:
            pdf_read()
            break
        elif "word" in choice:
            ms_word()
            break
        else:
            speak("Say either PDF or Word.")

# Run the reader
if __name__ == "__main__":
    choose_doc_reader()
