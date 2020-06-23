import win32com
from win32com.client import DispatchEx
from utils.resilience import *
from utils.exception_PT import *
from ctypes import windll

import time
import sys
import subprocess
import os

os.path.isfile
class CANalyzerAUD:

    #private 
    __CANanlyzer = None
    __Measurement = None

    def __init__(self, config_path):

        try : 
            CANalyzerAUD.__CANanlyzer = DispatchEx('CANalyzer.Application')
            CANalyzerAUD.__CANanlyzer.Open(config_path)
        
        except Exception as e:
            raise CANalyzerExpection("Couldn't create COM object")



    def init_measurements(self):
        CANalyzerAUD.__Measurement = CANalyzerAUD.__CANanlyzer.Measurement


    def start_measurements(self):
        status = False
        CANalyzerAUD.__Measurement.Start()

        if self.is_measurements_runing:
            status = True

        return status

    def stop_measurements(self):
        status = False
        CANalyzerAUD.__Measurement.Stop()

        if not self.is_measurements_runing():
            status = True

        return status

    def is_measurements_runing(self):
        return CANalyzerAUD.__Measurement.Running

    def cleanup(self):
        CANalyzerAUD.__CANanlyzer.Quit()
        CANalyzerAUD.__CANanlyzer = None
        CANalyzerAUD.__Measurement = None

    def check_if_CANalyser(self):

        status = False

        res, err = send_command_PS('Get-Process')
        res = res.decode('utf-8')
        
        if not err:
            if 'CANw64' in res:
                status = True

        return status


    def close_CANanlyser(self):
        status = False

        res, err = send_command_PS('Get-Process -Name "CANw64" | Stop-Process -Force')
        res = res.decode('utf-8')
        
        if not self.check_if_CANalyser():
            status = True

        return status


    def set_logging(self, log_name, file_loc='PTBLFLogs', log_type='.blf', logging_block_num=1):
        #get logging block
        status = False
        logging = CANalyzerAUD.__CANanlyzer.Configuration.OnlineSetup.LoggingCollection(logging_block_num)
        drives = get_drives()

        if 'D' in drives:
            file_loc = r'D:\\'+file_loc

        else:
            file_loc = r'C:\\'+file_loc

        check_dir_loc(file_loc)
        new_file_loc = file_loc+ "\\" + log_name+log_type

        if not os.path.isfile(new_file_loc):
            logging.FullName = new_file_loc
            log_name = new_file_loc

        else:
            count = 0 
            while True and count<1000:
                new_file_loc = file_loc+ "\\" +log_name+str(count)+log_type

                if not os.path.isfile(new_file_loc):
                    logging.FullName = new_file_loc
                    log_name = new_file_loc

        if logging.FullName == log_name:
            status = True

        return status
       


if __name__ == "__main__":
    
    
    App = CANalyzerAUD('PT_config.cfg')

    '''
    App.init_measurements()
    #print(App.start_measurements())
    #time.sleep(5)
    #print(App.stop_measurements())
    #time.sleep(3)
    App.check()
    #App.cleanup()
    '''
    
    #App.check_if_CANalyser()
    print(App.set_logging(log_name='Flexray'))

    #print(App.close_CANanlyser())