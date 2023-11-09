'''
Functions for saving, retrieving and deleting notes from json file.
'''
import datetime
import json
import sqlite3
import uuid
from typing import List, Dict

def save_note(username: str, subject: str, content: str) -> None:
    '''
    Save note to database
    ## Parameters
    username: str
    subject: str
    content: str
    '''
    save_note_sqlite(username, subject, content)
    # save_note_json(username, subject, content)

def save_note_sqlite(username: str, subject: str, content: str) -> None:
    '''
    Save note to database
    ## Parameters
    username: str
    subject: str
    content: str
    '''
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS notes (id text, username text, subject text, content text, date text, www text)")

    c.execute("INSERT INTO notes VALUES (?, ?, ?, ?, ?, ?)", (str(uuid.uuid4()), username, subject, content, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), 'https://www.google.com'))
    conn.commit()

    conn.close()



def save_note_json(username: str, subject: str, content: str) -> None:
    '''
    Save note to database
    ## Parameters
    username: str
    subject: str
    content: str
    '''
    note: Dict[str, str] = {
            'id': str(uuid.uuid4()),
            'username': username,
            'subject': subject,
            'content': content,
            'date': datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'www': 'https://www.google.com'
            }

    notes = _retrieve_all_notes()
    notes.append(note)
    with open('notes.json', 'w') as f:
        json.dump(notes, f)

def retrieve_user_notes(username: str) -> List[Dict[str, str]]:
    '''
    Retrieve notes from database
    ## Returns
    List of notes
    '''
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS notes (id text, username text, subject text, content text, date text, www text)")
    c.execute("SELECT * FROM notes WHERE username=?", (username,))
    notes = c.fetchall()
    notes = [{'id': note[0], 'username': note[1], 'subject': note[2], 'content': note[3], 'date': note[4], 'www': note[5]} for note in notes]
    conn.close()
    return notes


def delete_note(note_id: str) -> None:
    '''
    Delete note from database
    ## Parameters
    date : str
    '''
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS notes (id text, username text, subject text, content text, date text, www text)")
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

def search_notes(notes: List[Dict[str,str]], search_str: str) -> List[Dict[str, str]]:
    '''
    Search notes 
    ## Parameters
    notes : List[Dict[str, str]]
    search_str : str

    ## Returns
    List of notes
    '''
    if search_str[0].isdigit():
        return [note for note in notes if search_str in note["date"]]
    return [note for note in notes if search_str in note["content"]]

def _retrieve_all_notes_json() -> List[Dict[str, str]]:
    '''
    Retrieve notes from database
    ## Returns
    List of notes
    '''
    try:
        with open('notes.json', 'r') as f:
            notes: List[Dict[str,str]] = json.load(f)
    except FileNotFoundError:
        return []
    return notes


