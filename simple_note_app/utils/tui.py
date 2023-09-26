'''
display menu and get user input
'''
import curses
import utils.data as data

ENTER_KEY = 10
DELETE_KEY = 127
FINNISH_OPTION = 2

DEFAULT_Y = 3
DEFAULT_X = 5

def menu(stdscr: curses.window, username: str):
    '''
    Display menu and get user input
    ## Parameters
    stdscr: curses.window
    username: str

    ## Returns
    None
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
    _border(subwin)

    # Set colors
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    stdscr.refresh()

    # Set options
    options = [" Create a note ", " Retrieve a note ", " Log out "]
    current_option = 0

    while True:
        # Print options
        for i, option in enumerate(options):
            if i == current_option:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i+3, int(curses.COLS/2)-6, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(i+3, int(curses.COLS/2)-6, option)
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
            action(subwin, current_option, username)


    # Clear screen and exit
    stdscr.clear()
    curses.endwin()

def _border(subwin):
    subwin_height = curses.LINES * 3 // 4
    subwin_width = curses.COLS
    subwin.border()
    top_left = "╭"
    top_right = "╮"
    bottom_left = "╰"
    bottom_right = "╯"

    subwin.addch(0, 0, top_left)
    subwin.addch(0, subwin_width-1, top_right)
    subwin.addch(subwin_height-1, 0, bottom_left)
    #FIXME: only bottom right corner not WORKING
    #subwin.addch(subwin_height-1, subwin_width-1, bottom_right)


    subwin.addstr(0, int(curses.COLS/2-6), " TheNoteFairy ")
    # Refresh the subwindow to show its content
    subwin.refresh()

def action(subwin: curses.window, option: int, username: str):
    if option == 0:
        note = read_display(subwin)
        data.save_note(username, note)

    elif option == 1:
        user_notes = data.retrieve_notes(username)
        display_notes(subwin, user_notes)
    subwin.refresh()

def display_notes(subwin: curses.window, notes: list):
    if len(notes) == 0:
        subwin.clear()
        _border(subwin)
        subwin.addstr(DEFAULT_Y, DEFAULT_X, "No notes found")
        return
    n = 0
    subwin.clear()
    _border(subwin)
    _diplay_str(subwin, notes[n]["content"])
    while True:
        char = chr(subwin.getch())
        if char == '+':
            break
        elif char == 'h':
            subwin.clear()
            _border(subwin)
            n = (n - 1) % len(notes)
            _diplay_str(subwin, notes[n]["content"])
        elif char == 'l':
            subwin.clear()
            _border(subwin)
            n = (n + 1) % len(notes)
            _diplay_str(subwin, notes[n]["content"])
        elif char == 'd':
            data.delete_notes(notes[n]["date"])
            subwin.clear()
            _border(subwin)
            subwin.addstr(DEFAULT_Y, DEFAULT_X, "Deleted")
            break

def _diplay_str(subwin: curses.window, str: str):
    y = DEFAULT_Y
    for i, line in enumerate(str.split('\n')):
        subwin.addstr(y+i, DEFAULT_X, line)
        subwin.refresh()

def read_display(subwin: curses.window) -> str:
    subwin.clear()
    _border(subwin)
    x, y = DEFAULT_X, DEFAULT_Y
    str_acc = ""
    while True:
        char = chr(subwin.getch())
        if char == '\n':
            y += 1
            x = DEFAULT_X
            str_acc += '\n'
            continue
        elif char == '\t':
            x += 4
            str_acc += '\t'
            continue
        # delete
        # FIXME: delete not working when there is a tab or newline
        elif ord(char) == DELETE_KEY:
            if x > DEFAULT_X:
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
