import curses
import _curses
from tui.constants import TOP_LEFT_CHAR, TOP_RIGHT_CHAR, BOTTOM_LEFT_CHAR, BOTTOM_RIGHT_CHAR
from tui.windows import Windows

def refresh_subwindow(subwin: curses.window):
    SCREEN_HEIGHT = curses.LINES
    subwin_height = SCREEN_HEIGHT - 9
    subwin_width = curses.COLS
    # move the subwindow to the correct position
    subwin.mvwin(6, 0)
    #subwin.resize(subwin_height, subwin_width)
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
    # move the search box to the correct position
    searchbox.mvwin(3, 0)
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
    keybinding_box_height = 3
    keybinding_box_width = curses.COLS
    # move the keybinding box to the correct position
    keybinding_box.mvwin(curses.LINES - keybinding_box_height, 0)
    #FIX: keybinding_box.resize(keybinding_box_height, keybinding_box_width)
    keybinding_box.refresh()

def update_term_size(windows: Windows):
    y, x = windows.stdscr.getmaxyx()
    windows.stdscr.clear()
    curses.resizeterm(y, x)
    refresh_searchbox(windows.search_box)
    refresh_keybinding_box(windows.keybinding_box)
    refresh_subwindow(windows.subwin)
    windows.stdscr.refresh()
