'''
This is the core file of our simple note app.
'''
import sys
import getpass
import tui.app as tui

def main() -> int:
    '''
    Entry point.
    '''
    print('\nWelcome to the TheNoteFairy!')
    while True:
        try:
            username, password = login()
            if not check_user(username, password):
                print('Wrong username or password!')
                return 1

            tui.run(username)
        except KeyboardInterrupt:
            print('\nGoodbye!')
            break
    return 0

def login():
    '''
    Get username and password from user.
    '''
    print('\nUsername: ', end='')
    username = input()
    print('Password: ', end='')
    password = getpass.getpass()
    return username, password

def check_user(username: str, password: str) -> bool:
    '''
    Check if the user is valid.
    '''
    if username == 'admin' and password == 'admin':
        return True
    return False

if __name__ == '__main__':
    sys.exit(main())



