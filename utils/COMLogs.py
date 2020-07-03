import logging
from functools import wraps
from datetime import datetime
import string
from ctypes import windll

def get_logic_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()

    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives

def start_app_logs(log_name= 'app', file_loc ='PTBLFLogs'):
    status = False
    drives = get_logic_drives()

    if 'D' in drives:
        file_loc = 'D:\\'+ file_loc
    else:
        file_loc = 'C:\\'+file_loc

    now = datetime.now()
    timestamp = now.strftime(r'%d%m%Y_%H%M%S')
    logging.basicConfig(filename='{x}\\{y}_{z}.txt'.format(x = file_loc, y = log_name, z = timestamp), filemode='a', format='%(asctime)s - %(message)s',  level=logging.DEBUG)

def add_debug(msg):
    logging.debug(msg)

def add_info(msg):
    logging.info(msg)

def add_warning(msg):
    logging.warning(msg)

def add_error(msg):
    logging.error(msg)

def add_critical(msg):
    logging.critical(msg)
