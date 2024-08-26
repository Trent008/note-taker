import os
from datetime import datetime
import subprocess
import curses

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
    
    # Open the file with nano
    try:
        subprocess.run(["nano", file_path])
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

    # attempt to open the notes directory in explorer
    try:
        subprocess.call(["explorer", directory])
    except FileNotFoundError:
        return "explorer could not be opened or filepath does not exist"
    return "opened notes path"

def main(stdscr):
    # Clear screen and initialize
    stdscr.clear
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