'''
Functions for saving, retrieving and deleting notes from json file.
'''
import datetime
import json
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
    ## Parameters
    username : str

    ## Returns
    List of notes
    '''
    notes = _retrieve_all_notes()
    return [note for note in notes if note["username"] == username]

def delete_note(note_id: str) -> None:
    '''
    Delete note from database
    ## Parameters
    date : str
    '''
    notes = _retrieve_all_notes()
    notes = [note for note in notes if note["id"] != note_id]
    with open('notes.json', 'w') as f:
        json.dump(notes, f)

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

def _retrieve_all_notes() -> List[Dict[str, str]]:
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


