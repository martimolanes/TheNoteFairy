import curses
import _curses
from tui.constants import TOP_LEFT_CHAR, TOP_RIGHT_CHAR, BOTTOM_LEFT_CHAR, BOTTOM_RIGHT_CHAR

def refresh_subwindow(subwin: curses.window):
    SCREEN_HEIGHT = curses.LINES
    subwin_height = SCREEN_HEIGHT - 9
    subwin_width = curses.COLS
    subwin.border()

    subwin.addch(0, 0, TOP_LEFT_CHAR)
    subwin.addch(0, subwin_width - 1, TOP_RIGHT_CHAR)
    subwin.addch(subwin_height - 1, 0, BOTTOM_LEFT_CHAR)
    # This is a cotrolled crash
    # https://stackoverflow.com/questions/36387625/curses-fails-when-calling-addch-on-the-bottom-right-corner
    try:
        subwin.addch(subwin_height-1, subwin_width-1, BOTTOM_RIGHT_CHAR)
    except _curses.error:
        pass

    subwin.addstr(0, curses.COLS // 2 - 6, " TheNoteFairy ")
    # Refresh the subwindow to show its content
    subwin.refresh()

def refresh_searchbox(searchbox: curses.window):
    search_box_height = 3
    search_box_width = curses.COLS
    searchbox.clear()
    searchbox.border()
    searchbox.addch(0, 0, TOP_LEFT_CHAR)
    searchbox.addch(0, search_box_width - 1, TOP_RIGHT_CHAR)
    searchbox.addch(search_box_height - 1, 0, BOTTOM_LEFT_CHAR)
    # This is a cotrolled crash
    # https://stackoverflow.com/questions/36387625/curses-fails-when-calling-addch-on-the-bottom-right-corner
    try:
        searchbox.addch(search_box_height-1, search_box_width-1, BOTTOM_RIGHT_CHAR)
    except _curses.error:
        pass
    searchbox.addstr(search_box_height - 1, search_box_width - 9 , " Search ")
    searchbox.refresh()

def refresh_keybinding_box(keybinding_box: curses.window):
    keybinding_box.refresh()
