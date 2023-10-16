import curses
from typing import Dict
from tui.constants import *
from tui.utils import refresh_searchbox, refresh_subwindow, refresh_keybinding_box
import core.data as data
import core.web as web

def input_and_display(subwin: curses.window):
    subwin.clear()
    refresh_subwindow(subwin)
    subject = _read_subject(subwin)
    content = _read_content(subwin)

    return subject, content

def _read_subject(subwin: curses.window) -> str:
    subwin.addstr(DEFAULT_Y, DEFAULT_X, "Subject: ")
    x = DEFAULT_X + len("Subject: ")
    refresh_subwindow(subwin)
    subject = ""
    while True:
        char = chr(subwin.getch())
        if char == '\n':
            break
        elif ord(char) == DELETE_KEY:
            if x > DEFAULT_X + len("Subject: "):
                x -= 1
                subject = subject[:-1]
                subwin.addstr(DEFAULT_Y, x, ' ')
                refresh_subwindow(subwin)
            continue
        subject += char
        x += 1
        subwin.addstr(DEFAULT_Y, DEFAULT_X + len("Subject: "), subject)
        refresh_subwindow(subwin)
    return subject

def _read_content(subwin: curses.window) -> str:
    x, y = DEFAULT_X, DEFAULT_Y * 2
    str_acc = ""
    new_line_pos_x = []
    while True:
        char = chr(subwin.getch())
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
                subwin.addstr(y, x, ' ')
                refresh_subwindow(subwin)
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
                subwin.addstr(y, x, ' ')
                refresh_subwindow(subwin)
            continue
        elif char == '+':
            break
        
        subwin.addstr(y, x, char)
        x += 1
        refresh_subwindow(subwin)
        str_acc += char
        
    return str_acc

def _read_search(search_box: curses.window) -> str:
    x = 1 
    refresh_searchbox(search_box)
    search_box.addstr(1, x, ' >  ')
    x += 4
    search_str = ""
    while True:
        key = search_box.getch()
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
                search_box.addstr(1, x, ' ')
                refresh_searchbox(search_box)
            continue
        search_str += char
        search_box.addstr(1, x, char)
        x += 1
        refresh_searchbox(search_box)
    return search_str

def display_notes(subwin: curses.window, search_box: curses.window, keybinding_box: curses.window, notes: list):
    if len(notes) == 0:
        subwin.clear()
        refresh_subwindow(subwin)
        subwin.addstr(DEFAULT_Y, DEFAULT_X, "No notes found")
        return
    n = 0
    subwin.clear()
    refresh_subwindow(subwin)
    _diplay_note(subwin, notes[n])
    while True:
        keybinding_box.clear()
        keybinding_box.addstr(0, 2, "Press ←/→ to navigate between notes (or h/l) , / to search, d to delete, q to quit")
        refresh_keybinding_box(keybinding_box)
        key = subwin.getch()
        char = chr(key)
        if char == 'q':
            break
        elif char == 'h' or key == curses.KEY_LEFT:
            subwin.clear()
            refresh_subwindow(subwin)
            n = (n - 1) % len(notes)
            _diplay_note(subwin, notes[n])
        elif char == 'l' or key == curses.KEY_RIGHT:
            subwin.clear()
            refresh_subwindow(subwin)
            n = (n + 1) % len(notes)
            _diplay_note(subwin, notes[n])
        elif char == 'd':
            data.delete_note(notes[n]["id"])
            subwin.clear()
            refresh_subwindow(subwin)
            subwin.addstr(DEFAULT_Y, DEFAULT_X, "Deleted")
            break
        elif char == '/':
            search_box.clear()
            keybinding_box.clear()
            keybinding_box.addstr(0, 2, "Search, press ESC to cancel, ENTER to search")
            refresh_keybinding_box(keybinding_box)
            search_str = _read_search(search_box)
            if search_str == "":
                search_box.clear()
                refresh_searchbox(search_box)
                continue
            notes = data.search_notes(notes, search_str)
            if len(notes) == 0:
                subwin.clear()
                refresh_subwindow(subwin)
                subwin.addstr(DEFAULT_Y, DEFAULT_X, "No notes found containing: " + search_str)
                break
            subwin.clear()
            refresh_subwindow(subwin)
            n = 0
            _diplay_note(subwin, notes[n])


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
