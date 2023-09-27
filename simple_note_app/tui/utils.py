import curses
from tui.constants import TOP_LEFT_CHAR, TOP_RIGHT_CHAR, BOTTOM_LEFT_CHAR, BOTTOM_RIGHT_CHAR

def refresh_subwindow_border(subwin):
    subwin_height = curses.LINES * 3 // 4
    subwin_width = curses.COLS
    subwin.border()

    subwin.addch(0, 0, TOP_LEFT_CHAR)
    subwin.addch(0, subwin_width - 1, TOP_RIGHT_CHAR)
    subwin.addch(subwin_height - 1, 0, BOTTOM_LEFT_CHAR)
    #FIXME: only bottom right corner not WORKING
    #subwin.addch(subwin_height-1, subwin_width-1, BOTTOM_RIGHT_CHAR)

    subwin.addstr(0, curses.COLS // 2 - 6, " TheNoteFairy ")
    # Refresh the subwindow to show its content
    subwin.refresh()
