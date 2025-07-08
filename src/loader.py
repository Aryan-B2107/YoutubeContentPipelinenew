import time
import sys

def simple_spinner():
    char = ''
    spinner_chars = []
    for i in range(10):
        char += '.'
        spinner_chars.append(char)
    i = 0
    while True:
        sys.stdout.write('\r'+ ' Loading' + spinner_chars[i % len(spinner_chars)] )
        sys.stdout.flush()
        time.sleep(0.3)
        i += 1
simple_spinner()