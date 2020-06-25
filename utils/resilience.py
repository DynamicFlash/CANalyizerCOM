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

    proc = subprocess.Popen(["powershell.exe", 
                            '{}'.format(str(command))],
                        shell= False,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        )
    stdout_value, stderr_value = proc.communicate()
    #print(stdout_value)
    return stdout_value, stderr_value

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


def pack_device_dictionary(friendlyString):
    command = 'Get-PnpDevice -FriendlyName "*{}*" | ft -wrap -autosize friendlyname, instanceid'.format(friendlyString)
    stdout, stderr = send_command_PS(command)
    dict_values = []
    dict_keys = []
    dict_data = {}

    if not stderr:
        raw_data = stdout.decode('utf-8')

        with open('process.txt', 'w') as fp:
            fp.write(raw_data)
    
        with open('process.txt', 'r') as fp:
            lines = fp.readlines()

            for line in range(2,len(lines)-1):
                
                read_data = lines[line].strip()

                if read_data and (friendlyString in read_data):
                    data = read_data.split(' ')
                    data = [ x for x in data if x != '']
                    dict_values.append(data[len(data)-1].strip())

        dict_keys = ['{x}({y})'.format(x=friendlyString, y=i) for i in range(len(dict_values))]
        dict_data = {k:v for (k,v) in zip(dict_keys, dict_values)}
 
    return dict_data

def toggle_device(data_dict):
    
    for key,value in data_dict.items():

        command = 'gf'



#print(pack_device_dictionary("JBL"))