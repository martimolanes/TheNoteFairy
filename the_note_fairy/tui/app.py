'''
Display menu and get user input
'''
import curses
from core import data
from tui.constants import *
from tui.utils import refresh_subwindow, refresh_searchbox, refresh_keybinding_box, update_term_size
from tui.core import input_and_display, display_notes
from tui.windows import Windows

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

    # Create subwindow, search box and keybinding box
    windows: Windows = init_windows(stdscr)

    # Set colors
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    stdscr.refresh()

    # Set options
    options = [" Create a note ", " Retrieve a note ", " Log out "]
    current_option = 0

    while True:
        if curses.is_term_resized(curses.LINES, curses.COLS):
            update_term_size(windows)

        windows.keybinding_box.clear()
        windows.keybinding_box.addstr(0, 2, "Press ↑/↓ to move (or j/k), ENTER to select")
        refresh_keybinding_box(windows.keybinding_box)

        # Print options
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
            subwindow_run(windows, current_option, username)

    # Clear screen and exit
    stdscr.clear()
    curses.endwin()


def subwindow_run(
        windows: Windows, option: int, username: str
        ):
    if option == CREATE_OPTION:
        windows.keybinding_box.clear()
        windows.keybinding_box.addstr(0, 2, "Press ENTER to save subject, + to save the note")
        refresh_keybinding_box(windows.keybinding_box)
        subject, content = input_and_display(windows)
        data.save_note(username, subject, content)
    elif option == RETRIEVE_OPTION:
        user_notes = data.retrieve_user_notes(username)
        display_notes(windows, user_notes)
    refresh_subwindow(windows.subwin)

def init_windows(stdscr: curses.window) -> Windows:
    '''
    Create subwindow, search box and keybinding box
    ## Parameters
    stdscr: curses.window
    ## Returns
    SubWindows
    '''
    # Default window size
    SCREEN_WIDTH = curses.COLS
    SCREEN_HEIGHT = curses.LINES

    def create_subwindow(stdscr: curses.window,
                         height: int,
                         width: int,
                         y_offset: int,
                         refresh_func) -> curses.window:
        subwindow_y = y_offset
        subwindow_x = SCREEN_WIDTH // 2 - width // 2
        subwin: curses.window = stdscr.subwin(height, width, subwindow_y, subwindow_x)
        refresh_func(subwin)
        return subwin

    # Create a search box
    search_box_height = 3
    search_box_width = SCREEN_WIDTH
    search_box_y_offset = 3
    search_box: curses.window = create_subwindow(
            stdscr, search_box_height, search_box_width, search_box_y_offset, refresh_searchbox
            )

    # Create a subwindow for displaying notes
    subwin_height = SCREEN_HEIGHT - 10
    subwin_width = SCREEN_WIDTH
    subwin_y_offset = search_box_height + search_box_y_offset
    subwin: curses.window = create_subwindow(
            stdscr, subwin_height, subwin_width, subwin_y_offset, refresh_subwindow
            )

    # Create a keybinding box on the bottom of the subwindow
    keybinding_box_height = 3
    keybinding_box_width = SCREEN_WIDTH
    keybinding_box_y_offset = SCREEN_HEIGHT - keybinding_box_height
    keybinding_box: curses.window = create_subwindow(
            stdscr, keybinding_box_height, keybinding_box_width, keybinding_box_y_offset, refresh_keybinding_box
            )

    windows = Windows(stdscr, subwin, search_box, keybinding_box)

    return windows


def run(username: str):
    curses.wrapper(menu, username)
