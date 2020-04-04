import sys
import time
import curses
from signal import signal
from signal import SIGWINCH

# initilize curses
stdscr = curses.initscr()
# add support for colors if the terminal allows of course
curses.start_color()
# initilize the first color pair (foreground, background)
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
# do not echo user's keys to the screen
curses.noecho()
# react to key presses instantly (do not require Enter to be pressed)
curses.cbreak()
# interpret function and arrow keys as well
stdscr.keypad(True)

def main(stdscr):
    # allow key presses to not stop execution of the program
    stdscr.nodelay(True)
    # disable the cursor
    curses.curs_set(False)
    # Clear screen
    stdscr.clear()
    row = 0
    for i in range(3):
        for i in range(100):
            # get user input
            if stdscr.getch() != curses.ERR:
                return
            stdscr.addstr(row, 0, "Trying to connect" + ("." * i), curses.color_pair(1))
            stdscr.refresh()
            time.sleep(0.1)
        row += 1


#curses.curs_set(0);

#try:
curses.wrapper(main)
#except()

# exit curses
# reverse the curses-friendly terminal settings
curses.nocbreak()
stdscr.keypad(False)
curses.echo()

# restore the terminal to it's workng state
curses.endwin()
