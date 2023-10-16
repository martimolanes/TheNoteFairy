'''
This is the core file of our simple note app.
'''
import sys
import getpass
import tui.app as tui
from core import user

def main() -> int:
    '''
    Entry point.
    '''
    print('\nWelcome to the TheNoteFairy!')
    while True:
        try:
            username, password = login_info()
            if not user.manage_login(username, password):
                print('Wrong password!')
                return 1
            tui.run(username)
        except KeyboardInterrupt:
            print('\nGoodbye!')
            break
    return 0

def login_info():
    '''
    Get username and password from user.
    '''
    print('\nUsername: ', end='')
    username = input()
    password = getpass.getpass('Password: ')
    return username, password

if __name__ == '__main__':
    sys.exit(main())
