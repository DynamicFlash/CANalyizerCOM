import subprocess
import sys

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