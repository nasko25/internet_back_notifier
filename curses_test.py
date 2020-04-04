import sys
import time
import curses
from signal import signal
from signal import SIGWINCH

# initilize curses
stdscr = curses.initscr()
# do not echo user's keys to the screen
curses.noecho()
# react to key presses instantly (do not require Enter to be pressed)
curses.cbreak()
# interpret function and arrow keys as well
stdscr.keypad(True)

def main(stdscr):
    # disable the cursor
    curses.curs_set(False)
    # Clear screen
    stdscr.clear()
    row = 0
    for i in range(3):
        for i in range(100):
            stdscr.addstr(row, 0, "Trying to connect" + ("." * i))
            stdscr.refresh()
            time.sleep(0.1)
        row += 1


#curses.curs_set(0);

#curses.signal(SIGWINCH, handle_resize())
curses.wrapper(main)

# exit curses
# reverse the curses-friendly terminal settings
curses.nocbreak()
stdscr.keypad(False)
curses.echo()

# restore the terminal to it's workng state
curses.endwin()
