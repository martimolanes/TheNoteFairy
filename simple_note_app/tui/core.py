import curses
from typing import Dict
from tui.constants import *
from tui.utils import refresh_subwindow
import core.data as data

def input_and_display(subwin: curses.window):
    subwin.clear()
    refresh_subwindow(subwin)
    subject = _read_subject(subwin)
    content = _read_content(subwin)

    return subject, content

def _read_subject(subwin: curses.window) -> str:
    subwin.addstr(DEFAULT_Y, DEFAULT_X, "Subject: ")
    x = DEFAULT_X + len("Subject: ")
    subwin.refresh()
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
                subwin.refresh()
            continue
        subject += char
        x += 1
        subwin.addstr(DEFAULT_Y, DEFAULT_X + len("Subject: "), subject)
        subwin.refresh()
    return subject

def _read_content(subwin: curses.window) -> str:
    x, y = DEFAULT_X, DEFAULT_Y * 2
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

def display_notes(subwin: curses.window, notes: list):
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
        char = chr(subwin.getch())
        if char == '+':
            break
        elif char == 'h':
            subwin.clear()
            refresh_subwindow(subwin)
            n = (n - 1) % len(notes)
            _diplay_note(subwin, notes[n])
        elif char == 'l':
            subwin.clear()
            refresh_subwindow(subwin)
            n = (n + 1) % len(notes)
            _diplay_note(subwin, notes[n])
        elif char == 'd':
            data.delete_notes(notes[n]["date"])
            subwin.clear()
            refresh_subwindow(subwin)
            subwin.addstr(DEFAULT_Y, DEFAULT_X, "Deleted")
            break
        elif char == '/':
            pass


def _diplay_note(subwin: curses.window, note: Dict[str, str]):
    subwin.addstr(DEFAULT_Y, DEFAULT_X, "Username: " + note["username"])
    subwin.addstr(DEFAULT_Y + 1, DEFAULT_X, "Date: " + note["date"])
    subwin.addstr(DEFAULT_Y + 3, DEFAULT_X, "Subject: " + note["subject"])

    y = DEFAULT_Y * 2 + 4
    for i, line in enumerate(note["content"].split('\n')):
        subwin.addstr(y+i, DEFAULT_X, line)
        subwin.refresh()
