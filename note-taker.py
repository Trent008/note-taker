import os
from datetime import datetime, timedelta
import subprocess
import curses
import shutil

def find_last_existing_file():
    current_date = datetime.now()
    # Start searching from the previous day
    search_date = current_date - timedelta(days=1)

    while True:
        year = search_date.year
        month = search_date.month
        day = search_date.day

        last_file_path = os.path.join(os.path.expanduser("~"), "notes", str(year), str(month), f"{day}.txt")
        if os.path.exists(last_file_path):
            return last_file_path
        
        # Move one day back
        search_date -= timedelta(days=1)
        
        # Stop searching after one year
        if search_date.year < current_date.year - 1:
            break
    
    return None

def open_daily_notes():
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day

    # Create the directory structure based on the current date
    directory = os.path.join(os.path.expanduser("~"), "notes", str(year), str(month))
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")
    
    # File name based on the current day
    filename = f"{day}.txt"
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
        subprocess.run(["notepad", file_path])
        print(f"Opening '{file_path}' in nano.")
    except FileNotFoundError:
        print("Nano not found. Make sure it is installed.")
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
        subprocess.call(["explorer", directory])
    except FileNotFoundError:
        return "explorer could not be opened or filepath does not exist"
    return "opened notes path"

def main(stdscr):
    # Clear screen and initialize
    stdscr.clear()
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Set a timeout for input

    # Menu options
    options = ["Open Daily Notes", "Open Notes Path", "Exit"]
    functions = [open_daily_notes, open_notes_path, None]
    
    current_selection = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        for idx, option in enumerate(options):
            x = w // 2 - len(option) // 2
            y = h // 2 - len(options) // 2 + idx
            if idx == current_selection:
                stdscr.attron(curses.A_REVERSE)  # Highlight selected option
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, option)

        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_DOWN:
            current_selection = (current_selection + 1) % len(options)
        elif key == curses.KEY_UP:
            current_selection = (current_selection - 1) % len(options)
        elif key == 10:  # Enter key
            selected_function = functions[current_selection]
            if selected_function is None:
                break
            result = selected_function()
            stdscr.clear()
            stdscr.addstr(h // 2, w // 2 - len(result) // 2, result)
            stdscr.refresh()
            stdscr.getch()  # Wait for user input to return to the menu

if __name__ == "__main__":
    curses.wrapper(main)
