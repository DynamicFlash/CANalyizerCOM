import subprocess
import sys
import string
from ctypes import windll
import os

def anti_fragile(func):
    dataObj = None

    try:
        dataObj = func()
        
    except Exception as error:
        print(error.msg)


def send_command_PS(command):
    p = subprocess.run(["powershell.exe", 
                            '{}'.format(str(command))], capture_output=True
                            )
    return p.stdout, p.stderr

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()

    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives

def check_dir_loc(file_loc):
    if os.path.isdir(file_loc):
        pass
    else:
        os.mkdir(file_loc)