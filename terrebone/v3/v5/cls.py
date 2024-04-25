import ctypes


def msg(message, msg_type):
    if msg_type == "I":
        ctypes.windll.user32.MessageBoxW(0, message, "Information", 1)
    elif msg_type == "E":
        ctypes.windll.user32.MessageBoxW(0, message, "Error", 1)
