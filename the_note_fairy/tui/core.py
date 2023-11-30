import curses
from typing import Dict
from tui.constants import *
from tui.utils import refresh_searchbox, refresh_subwindow, refresh_keybinding_box, update_term_size
import core.data as data
import core.web as web
from tui.windows import Windows

def input_and_display(windows: Windows):
    windows.keybinding_box.clear()
    windows.keybinding_box.addstr(0, 2, "Press ENTER to save subject, + to save the note")
    refresh_keybinding_box(windows.keybinding_box)
    windows.subwin.clear()
    refresh_subwindow(windows.subwin)
    subject = _read_subject(windows)
    content, www = _read_content(windows)

    return subject, content

def _read_subject(windows: Windows) -> str:
    windows.subwin.addstr(DEFAULT_Y, DEFAULT_X, "Subject: ")
    x = DEFAULT_X + len("Subject: ")
    refresh_subwindow(windows.subwin)
    subject = ""
    while True:
        if curses.is_term_resized(curses.LINES, curses.COLS):
            update_term_size(windows)
        char = chr(windows.subwin.getch())
        if char == '\n':
            break
        elif ord(char) == DELETE_KEY:
            if x > DEFAULT_X + len("Subject: "):
                x -= 1
                subject = subject[:-1]
                windows.subwin.addstr(DEFAULT_Y, x, ' ')
                refresh_subwindow(windows.subwin)
            continue
        subject += char
        x += 1
        windows.subwin.addstr(DEFAULT_Y, DEFAULT_X + len("Subject: "), subject)
        refresh_subwindow(windows.subwin)
    return subject

def _read_content(windows: Windows):
    x, y = DEFAULT_X, DEFAULT_Y * 2
    str_acc = ""
    new_line_pos_x = []
    while True:
        if curses.is_term_resized(curses.LINES, curses.COLS):
            update_term_size(windows)
        char = chr(windows.subwin.getch())
        if char == '\n':
            y += 1
            new_line_pos_x.append(x)
            x = DEFAULT_X
            str_acc += '\n'
            continue
        elif char == '\t':
            x += 4
            str_acc += '\t'
            continue
        # delete
        elif ord(char) == DELETE_KEY:
            if x > DEFAULT_X:
                x -= 1
                str_acc = str_acc[:-1]
                windows.subwin.addstr(y, x, ' ')
                refresh_subwindow(windows.subwin)
            else:
                if new_line_pos_x == []:
                    continue
                y -= 1
                x = new_line_pos_x.pop()
                if x == DEFAULT_X:
                    str_acc = str_acc[:-1]
                else:
                    str_acc = str_acc[:-2]
                    x -= 1
                windows.subwin.addstr(y, x, ' ')
                refresh_subwindow(windows.subwin)
            continue
        elif char == '+':
            break
        
        windows.subwin.addstr(y, x, char)
        x += 1
        refresh_subwindow(windows.subwin)
        str_acc += char

    www = read_www(windows, y)
        
    return str_acc, www

def read_www(windows: Windows, y: int):
    www_help = "www: "
    windows.subwin.addstr( y + DEFAULT_Y, DEFAULT_X, www_help)
    x = DEFAULT_X + len("Subject: ")
    refresh_subwindow(windows.subwin)
    www = ""
    while True:
        if curses.is_term_resized(curses.LINES, curses.COLS):
            update_term_size(windows)
        char = chr(windows.subwin.getch())
        if char == '\n':
            break
        elif ord(char) == DELETE_KEY:
            if x > DEFAULT_X + len(www_help):
                x -= 1
                www = www[:-1]
                windows.subwin.addstr(y + DEFAULT_Y, x, ' ')
                refresh_subwindow(windows.subwin)
            continue
        www += char
        x += 1
        windows.subwin.addstr(y + DEFAULT_Y, DEFAULT_X + len(www_help), www)
        refresh_subwindow(windows.subwin)
    return www


def _read_search(windows: Windows) -> str:
    x = 1 
    refresh_searchbox(windows.search_box)
    windows.search_box.addstr(1, x, ' >  ')
    x += 4
    search_str = ""
    while True:
        if curses.is_term_resized(curses.LINES, curses.COLS):
            update_term_size(windows)
        key = windows.search_box.getch()
        char = chr(key)
        if char == '\n':
            break
        elif key == ESCAPE_KEY:
            search_str = ""
            break
        elif ord(char) == DELETE_KEY:
            if x > 5:
                x -= 1
                search_str = search_str[:-1]
                windows.search_box.addstr(1, x, ' ')
                refresh_searchbox(windows.search_box)
            continue
        search_str += char
        windows.search_box.addstr(1, x, char)
        x += 1
        refresh_searchbox(windows.search_box)
    return search_str

def display_notes(windows: Windows, notes: list):
    if len(notes) == 0:
        windows.subwin.clear()
        refresh_subwindow(windows.subwin)
        windows.subwin.addstr(DEFAULT_Y, DEFAULT_X, "No notes found")
        return
    n = 0
    windows.subwin.clear()
    refresh_subwindow(windows.subwin)
    _diplay_note(windows.subwin, notes[n])
    while True:
        if curses.is_term_resized(curses.LINES, curses.COLS):
            update_term_size(windows)
        windows.keybinding_box.clear()
        windows.keybinding_box.addstr(0, 2, "Press h/l to navigate between notes, / to search, d to delete, q to quit")
        refresh_keybinding_box(windows.keybinding_box)
        key = windows.subwin.getch()
        char = chr(key)
        if char == 'q':
            break
        elif char == 'h':
            windows.subwin.clear()
            refresh_subwindow(windows.subwin)
            n = (n - 1) % len(notes)
            _diplay_note(windows.subwin, notes[n])
        elif char == 'l':
            windows.subwin.clear()
            refresh_subwindow(windows.subwin)
            n = (n + 1) % len(notes)
            _diplay_note(windows.subwin, notes[n])
        elif char == 'd':
            data.delete_note(notes[n]["id"])
            windows.subwin.clear()
            refresh_subwindow(windows.subwin)
            windows.subwin.addstr(DEFAULT_Y, DEFAULT_X, "Deleted")
            break
        elif char == '/':
            windows.search_box.clear()
            windows.keybinding_box.clear()
            windows.keybinding_box.addstr(0, 2, "Search, press ESC to cancel, ENTER to search")
            refresh_keybinding_box(windows.keybinding_box)
            search_str = _read_search(windows)
            if search_str == "":
                windows.search_box.clear()
                refresh_searchbox(windows.search_box)
                continue
            notes = data.search_notes(notes, search_str)
            if len(notes) == 0:
                windows.subwin.clear()
                refresh_subwindow(windows.subwin)
                windows.subwin.addstr(DEFAULT_Y, DEFAULT_X, "No notes found containing: " + search_str)
                break
            windows.subwin.clear()
            refresh_subwindow(windows.subwin)
            n = 0
            _diplay_note(windows.subwin, notes[n])


def _diplay_note(subwin: curses.window, note: Dict[str, str]):
    subwin.addstr(DEFAULT_Y, DEFAULT_X, "Username: " + note["username"])
    subwin.addstr(DEFAULT_Y + 1, DEFAULT_X, "Date: " + note["date"])
    subwin.addstr(DEFAULT_Y + 3, DEFAULT_X, "Subject: " + note["subject"])

    y = DEFAULT_Y * 2 + 4
    for i, line in enumerate(note["content"].split('\n')):
        subwin.addstr(y+i, DEFAULT_X, line)
        refresh_subwindow(subwin)
    
    title = web.get_title(note["www"])   
    if title:
        subwin.addstr(y + 3 + len(note["content"].split('\n')), DEFAULT_X, "fetch-title: " + title)
