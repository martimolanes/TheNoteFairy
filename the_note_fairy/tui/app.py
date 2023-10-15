'''
Display menu and get user input
'''
import curses
import core.data as data
from tui.constants import *
from tui.utils import refresh_subwindow, refresh_searchbox
from tui.core import input_and_display, display_notes

def menu(stdscr: curses.window, username: str):
    '''
    Display menu and get user input
    ## Parameters
    stdscr: curses.window
    username: str
    '''
    # Hide cursor
    curses.curs_set(0)
    # Clear screen
    stdscr.clear()

    # Default window size
    SCREEN_WIDTH = curses.COLS
    SCREEN_HEIGHT = curses.LINES

    # Create a keybinding box on the bottom of the subwindow
    keybinding_box_height = max(SCREEN_HEIGHT // 10, 3)
    keybinding_box_width = SCREEN_WIDTH
    keybinding_box_y = SCREEN_HEIGHT - keybinding_box_height
    keybinding_box_x = SCREEN_WIDTH // 2 - keybinding_box_width // 2
    keybinding_box: curses.window = stdscr.subwin(keybinding_box_height, keybinding_box_width, keybinding_box_y, keybinding_box_x)
    keybinding_box.refresh()

    # Create a subwindow
    subwin_height = SCREEN_HEIGHT * 3 // 4
    subwin_width = SCREEN_WIDTH
    subwin_y = SCREEN_HEIGHT - subwin_height - keybinding_box_height
    subwin_x = SCREEN_WIDTH // 2 - subwin_width // 2
    subwin: curses.window = stdscr.subwin(subwin_height, subwin_width, subwin_y, subwin_x)
    refresh_subwindow(subwin)

    # Create a search box on top of the subwindow
    search_box_height = 3
    search_box_width = SCREEN_WIDTH
    search_box_y = SCREEN_HEIGHT - search_box_height - subwin_height - keybinding_box_height
    search_box_x = SCREEN_WIDTH // 2 - search_box_width // 2
    search_box: curses.window = stdscr.subwin(search_box_height, search_box_width, search_box_y, search_box_x)
    refresh_searchbox(search_box)

    # Set colors
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    stdscr.refresh()

    # Set options
    options = [" Create a note ", " Retrieve a note ", " Log out "]
    current_option = 0

    while True:
        keybinding_box.clear()
        keybinding_box.addstr(1, 1, "Press ↑/↓ to move (or j/k), ENTER to select")
        keybinding_box.refresh()
        # Print options
        option_y = (search_box_y - 3) // 2
        if option_y < 0:
            option_y = 0
        for i, option in enumerate(options):
            if i == current_option:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i+option_y, int(curses.COLS/2)-6, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(i+option_y, int(curses.COLS/2)-6, option)
                stdscr.attroff(curses.color_pair(2))

        # Get user input
        key = stdscr.getch()

        # Move up or down
        if key == curses.KEY_UP or chr(key) == 'k':
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_DOWN or chr(key) == 'j':
            current_option = (current_option + 1) % len(options)
        elif key == ENTER_KEY:
            if current_option == LOGOUT_OPTION:
                break
            subwindow_run(subwin, search_box, keybinding_box, current_option, username)

    # Clear screen and exit
    stdscr.clear()
    curses.endwin()

def subwindow_run(subwin: curses.window, search_box: curses.window, keybinding_box: curses.window, option: int, username: str):
    if option == CREATE_OPTION:
        keybinding_box.clear()
        keybinding_box.addstr(1, 1, "Press ENTER to save subject, + to save the note")
        keybinding_box.refresh()
        subject, content = input_and_display(subwin)
        data.save_note(username, subject, content)
    elif option == RETRIEVE_OPTION:
        user_notes = data.retrieve_user_notes(username)
        display_notes(subwin, search_box, keybinding_box, user_notes)
    subwin.refresh()

# Run main function
def run(username: str):
    curses.wrapper(menu, username)
