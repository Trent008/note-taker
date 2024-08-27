import os
from sys import platform
import time
from datetime import datetime, timedelta
import subprocess
import shutil

def find_last_existing_file():
    current_date = datetime.now()
    # Start searching from the previous day
    search_date = current_date - timedelta(days=1)

    while True:
        year = search_date.year
        month = search_date.month
        day = search_date.day

        last_file_path = os.path.join(os.path.expanduser("~"), "notes", str(year), f"{month}-{day}.txt")
        if os.path.exists(last_file_path):
            return last_file_path
        
        # Move one day back
        search_date -= timedelta(days=1)
        
        # Stop searching after one year
        if search_date.year < current_date.year - 1:
            break
    
    return None

def open_todays_notes():
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day

    # Create the directory structure based on the current date
    directory = os.path.join(os.path.expanduser("~"), "notes", str(year))
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")
    
    # File name based on the current day
    filename = f"{month}-{day}.txt"
    file_path = os.path.join(directory, filename)
    
    # Check if the file already exists
    if not os.path.exists(file_path):
        last_file_path = find_last_existing_file()
        if last_file_path:
            # Copy the contents of the last existing file to the new file
            shutil.copy(last_file_path, file_path)
            print(f"Copied contents from '{last_file_path}' to '{file_path}'.")
        else:
            # Create a new empty file
            open(file_path, 'w').close()
            print(f"Created new empty file '{file_path}'.")
    
    # Open the file with nano
    try:
        text_editor = None
        if platform == "linux": text_editor = 'nano'
        elif platform == "win32": text_editor = 'notepad'
        subprocess.run([text_editor, file_path])
        print(f"Opening '{file_path}' in {text_editor}.")
    except FileNotFoundError:
        return "Nano not found. Make sure it is installed."
    return "opened daily notes"

def open_notes_path():
    # Create the directory structure based on the current date
    directory = os.path.join(os.path.expanduser("~"), "notes")
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")

    # Attempt to open the notes directory in explorer
    try:
        file_manager = None
        if platform == "linux": file_manager = 'thunar'
        elif platform == "win32": file_manager = 'explorer'
        subprocess.run([file_manager, directory])
        print(f"Opening '{directory}' in {file_manager}.")
    except FileNotFoundError:
        return f"{file_manager} could not be opened or filepath does not exist"
    return "opened notes path"

while True:
    user_selection = input("\nenter to take notes\n"
                           "f then enter to see note files\n"
                           "q then enter to quit\n")
    if user_selection == "": print(open_todays_notes())
    elif user_selection == "f": print(open_notes_path())
    elif user_selection == "q": break