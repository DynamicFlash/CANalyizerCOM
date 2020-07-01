import win32evtlog, win32evtlogutil, win32security, win32con, winerror
import time
import re
import string
import sys
import traceback

def log(server):
    logtype='Application'
    hand=win32evtlog.OpenEventLog(server,logtype)
    total=win32evtlog.GetNumberOfEventLogRecords(hand)
    print(total)


log('CANalyzer')