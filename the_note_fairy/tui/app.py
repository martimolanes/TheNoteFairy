'''
display menu and get user input
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
    
    # Create a subwindow
    subwin_height = curses.LINES * 3 // 4
    subwin_width = curses.COLS
    subwin_y = curses.LINES - subwin_height
    subwin_x = curses.COLS // 2 - subwin_width // 2
    subwin: curses.window = stdscr.subwin(subwin_height, subwin_width, subwin_y, subwin_x)
    refresh_subwindow(subwin)

    # Create a search box on top of the subwindow
    search_box_height = curses.LINES // 12
    if search_box_height < 3:
        search_box_height = 3
    search_box_width = curses.COLS
    search_box_y = curses.LINES - search_box_height - subwin_height 
    search_box_x = curses.COLS // 2 - search_box_width // 2
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
        if key == curses.KEY_UP:
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(options)
        elif key == ENTER_KEY:
            if current_option == LOGOUT_OPTION:
                break
            subwindow_run(subwin, search_box, current_option, username)

    # Clear screen and exit
    stdscr.clear()
    curses.endwin()

def subwindow_run(subwin: curses.window, search_box: curses.window,  option: int, username: str):
    if option == CREATE_OPTION:
        subject, content = input_and_display(subwin)
        data.save_note(username, subject, content)
    elif option == RETRIEVE_OPTION:
        user_notes = data.retrieve_user_notes(username)
        display_notes(subwin, search_box, user_notes)
    subwin.refresh()

# Run main function
def run(username: str):
    curses.wrapper(menu, username)
