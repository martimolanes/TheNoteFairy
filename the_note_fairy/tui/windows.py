import curses
class Windows:
    def __init__(self, stdscr: curses.window, subwin: curses.window, search_box: curses.window, keybinding_box: curses.window):
        self.stdscr = stdscr
        self.subwin = subwin
        self.search_box = search_box
        self.keybinding_box = keybinding_box
