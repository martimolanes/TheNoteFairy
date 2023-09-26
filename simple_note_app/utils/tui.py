'''
display menu and get user input
'''
import curses

ENTER_KEY = 10
FINNISH_OPTION = 2

def menu(stdscr: curses.window, username: str):
    '''
    Display menu and get user input
    ## Parameters
    stdscr: curses.window
    username: str

    ## Returns
    None
    '''
    curses.curs_set(0)
    # Clear screen
    stdscr.clear()
    
    # make subwindow that occups all of the bottom middle of the screen
    subwin_height = curses.LINES * 3 // 4
    subwin_width = curses.COLS
    subwin_y = curses.LINES - subwin_height
    subwin_x = curses.COLS // 2 - subwin_width // 2

    # Create a subwindow
    subwin: curses.window = stdscr.subwin(subwin_height, subwin_width, subwin_y, subwin_x)
    subwin.border()

    # Add content to the subwindow
    subwin.addstr(1, 1, "This is a subwindow")
    subwin.addstr(3, 1, "Press any key to exit")

    # Refresh the subwindow to show its content
    subwin.refresh()

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
            if current_option == 2:
                break
            action(subwin, current_option)


    # Clear screen and exit
    stdscr.clear()
    curses.endwin()


def action(subwin: curses.window, option: int):
    if option == 0:
        read_display(subwin)

    elif option == 1:
        subwin.addstr(3, 3, "Retrieve a note")
    subwin.refresh()

def read_display(subwin: curses.window) -> str:
    subwin.clear()
    subwin.border()
    x, y = 3, 3
    str_acc = ""
    while True:
        char = chr(subwin.getch())
        if char == '\n':
            y += 1
            x = 3
            continue
        elif char == '\t':
            x += 4
            continue
        elif ord(char) == 127:
            if x > 3:
                x -= 1
                str_acc = str_acc[:-1]
                subwin.addstr(y, x, ' ')
                subwin.refresh()
            continue
        elif char == '+':
            break
        
        subwin.addstr(y, x, char)
        x += 1
        subwin.refresh()
        str_acc += char
        
    return str_acc

# Run main function
def run(username: str):
    curses.wrapper(menu, username)
