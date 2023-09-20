'''
This is the core file of our simple note app.
'''
import sys
import menu

def main() -> int:
    '''
    Entry point.
    '''
    args = sys.argv
    print(args)

    # Welcome message
    print('Welcome to the Simple Note App!')
    # User autentication
    print('Please enter your username:')
    username = input()
    print('Please enter your password:')
    password = input()
    
    if not check_user(username, password):
        print('Wrong username or password!')
        return 1
    menu.run()
    return 0

def check_user(username: str, password: str) -> bool:
    '''
    Check if the user is valid.
    '''
    if username == 'admin' and password == 'admin':
        return True
    return False

if __name__ == '__main__':
    sys.exit(main())



