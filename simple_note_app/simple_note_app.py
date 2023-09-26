'''
This is the core file of our simple note app.
'''
import sys
import utils.tui as tui

def main() -> int:
    '''
    Entry point.
    '''
    # Welcome message
    print('Welcome to the Simple Note App!')
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
    password = input()
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



