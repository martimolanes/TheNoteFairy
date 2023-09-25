'''
display menu and get user input
'''
import curses

ENTER_KEY = 10

def menu(stdscr: curses.window, username: str):
    # Clear screen
    stdscr.clear()

    # Set colors
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Set outline
    stdscr.border()

    # Set options
    options = ["1. Create a note", "2. Retrieve a note", "3. Log out"]
    current_option = 0

    # Loop until user presses Enter
    while True:
        # Print options
        for i, option in enumerate(options):
            if i == current_option:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i+1, 2, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(i+1, 2, option)
                stdscr.attroff(curses.color_pair(2))

        # Get user input
        key = stdscr.getch()

        # Move up or down
        if key == curses.KEY_UP:
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(options)
        elif key == ENTER_KEY:
            break


    # Clear screen and exit
    stdscr.clear()
    curses.endwin()

# Run main function
def run(username: str):
    curses.wrapper(menu, username)
