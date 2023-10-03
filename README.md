# TheNoteFairy

A TUI(text/terminal user interface) from scratch using [curses](https://docs.python.org/3/library/curses.html#module-curses).

## CAPABILITIES
- Create and retrieve notes
- Search for date and text in the notes

## KEY BINDINGS
- Arrows and Enter in the main menu
- Press Enter when you finish your Subject in 'Create note'
- To save your note press '+' and it returns to the main menu
- To iterate over your 'retrieved notes' press 'h' and 'l'
- To return to the menu from 'retrieved notes' press '+'
- To search for a note you need to be in retrieve notes and press '/'
- To delete a note you need to be in retrieve notes and press 'd' in the desired note

DEFAULT USERNAME, PASSWD: admin admin

## KNOWN PROBLEMS
- application may NOT function well with some sizes of screen terminal -> recommended to launch it fullscreen
- when deleting in the content of a note that have \n, you cannot delete more than the line you are writing
