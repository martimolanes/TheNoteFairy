import datetime
from typing import List, Dict

notes = []

def save_note(username: str, subject: str, content: str):
    '''
    Save note to database
    ## Parameters
    username: str
    content: str
    '''
    note: Dict[str, str] = {
            'username': username,
            'subject': subject,
            'content': content,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    notes.append(note)

def retrieve_notes(username: str) -> List[Dict[str, str]]:
    '''
    Retrieve notes from database
    ## Parameters
    username

    ## Returns
    List of notes
    '''
    return [note for note in notes if note["username"] == username]

def delete_notes(date: str):
    '''
    Delete notes from database
    ## Parameters
    username
    '''
    global notes
    notes = [note for note in notes if note["date"] != date]

