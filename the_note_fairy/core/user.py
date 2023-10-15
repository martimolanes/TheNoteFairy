'''
User management functions
'''
import sqlite3
import bcrypt

def manage_login(username: str, password_try: str) -> bool:
    '''
    Check if the user is valid.
    '''
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user(username PRIMARY KEY, password)")

    user = c.execute("SELECT * FROM user WHERE username=?", (username,)).fetchone()
    conn.close()

    if user is None:
        return create_user(username, password_try)
    return bcrypt.checkpw(password_try.encode("utf-8"), user[1])

def create_user(username: str, password: str) -> bool:
    '''
    Create a new user.
    '''
    print("User do NOT exist\n...Creating user...")
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    password_encrypted = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    c.execute("INSERT INTO user VALUES(?, ?)", (username, password_encrypted))
    conn.commit()
    conn.close()
    return True
