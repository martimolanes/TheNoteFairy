'''
Functions for saving, retrieving and deleting notes from json file.
'''
import datetime
import json
import sqlite3
import uuid
from typing import List, Dict

def save_note(username: str, subject: str, content: str, www: str) -> None:
    '''
    Save note to database
    ## Parameters
    username: str
    subject: str
    content: str
    '''
    if www == "":
        www = "https://www.github.com"
    save_note_sqlite(username, subject, content, www=www)
    # save_note_json(username, subject, content)

def save_note_sqlite(
        username: str, subject: str, content: str,
        id=str(uuid.uuid4()),
        date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        www="https://www.github.com"
                     ) -> None:
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

    c.execute("INSERT INTO notes VALUES (?, ?, ?, ?, ?, ?)", (id, username, subject, content, date, www))
    conn.commit()

    conn.close()

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

def import_json() -> None:
    '''
    Import notes from json file
    '''
    try:
        with open('notes.json', 'r') as f:
            data: List[Dict[str,str]] = json.load(f)
    except FileNotFoundError:
        data = []

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS notes (id text, username text, subject text, content text, date text, www text)")
    c.execute("SELECT id FROM notes")
    ids = c.fetchall()
    ids = [id[0] for id in ids]
    for note in data:
        if note["id"] not in ids:
            c.execute("INSERT INTO notes VALUES (?, ?, ?, ?, ?, ?)", (note["id"], note["username"], note["subject"], note["content"], note["date"], note["www"]))
    conn.commit()
    conn.close()
