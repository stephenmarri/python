import ctypes
import os.path
from pathlib import Path
import smtplib
from config import *


def msg(message, msg_type):
    if msg_type == "I":
        ctypes.windll.user32.MessageBoxW(0, message, "Information", 1)
    elif msg_type == "E":
        ctypes.windll.user32.MessageBoxW(0, message, "Error", 1)


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        Path(dir_name).mkdir(parents=True, exist_ok=True)


def crete_base_dirs():
    lst = [dir_output, dir_download, dir_intermediate, dir_result]
    for dr in lst:
        create_dir(dr)
