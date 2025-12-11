import pyperclip
import threading

def copy_to_clipboard(text, clear_after=10):
    pyperclip.copy(text)
    def clear():
        pyperclip.copy('')
    timer = threading.Timer(clear_after, clear)
    timer.start()