import datetime
from typing import List, Dict

notes = []

def save_note(username: str, subject: str, content: str) -> None:
    '''
    Save note to database
    ## Parameters
    username: str
    subject: str
    content: str
    '''
    note: Dict[str, str] = {
            'username': username,
            'subject': subject,
            'content': content,
            'date': datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

    notes.append(note)

def retrieve_notes(username: str) -> List[Dict[str, str]]:
    '''
    Retrieve notes from database
    ## Parameters
    username : str

    ## Returns
    List of notes
    '''
    return [note for note in notes if note["username"] == username]

def delete_notes(date: str) -> None:
    '''
    Delete notes from database
    ## Parameters
    date : str
    '''
    global notes
    notes = [note for note in notes if note["date"] != date]

def search_notes(search_str: str) -> List[Dict[str, str]]:
    '''
    Search notes from database
    ## Parameters
    search_str : str

    ## Returns
    List of notes
    '''
    if search_str[0].isdigit():
        return [note for note in notes if search_str in note["date"]]
    return [note for note in notes if search_str in note["content"]]

