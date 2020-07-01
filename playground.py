from win32com.client import DispatchEx
from utils.resilience import *
from utils.exception_PT import *
#from utils.COMLogs import *
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
    __Log = None

    def __init__(self, config_path):

        try : 
            CANalyzerAUD.__CANanlyzer = DispatchEx('CANalyzer.Application')
            CANalyzerAUD.__CANanlyzer.Open(config_path)
        
        except Exception as e:

            if self.check_if_CANalyser():
                self.close_CANanlyser()
                CANalyzerAUD.__CANanlyzer = DispatchEx('CANalyzer.Application')
                CANalyzerAUD.__CANanlyzer.Open(config_path)
            else:
                print("com object couldn't be initialised")

    def init_measurements(self):
        status = False
        CANalyzerAUD.__Measurement = CANalyzerAUD.__CANanlyzer.Measurement

        if CANalyzerAUD.__Measurement!=None:
            status = True
        
        return True

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
        self.close_CANanlyser()
        return True

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


    def set_logging(self, log_name, file_loc='PTBLFLogs', log_type='.blf', logging_block_num=[1]):
        #get logging block
        status = False
        drives = get_drives()

        if 'D' in drives:
            file_loc = 'D:\\'+ file_loc

        else:
            file_loc = 'C:\\'+file_loc

        #scaled up for N number of blocks
        for i in logging_block_num:
            #getting logging block
            logging = CANalyzerAUD.__CANanlyzer.Configuration.OnlineSetup.LoggingCollection(i)

            #Checking if file diretory is present
            check_dir_loc(file_loc)

            #Using Field code{MeasurementStart} to add today's date and time
            logging.FullName = file_loc+ "\\"+ log_name+r'{MeasurementStart}'+log_type
            new_file_loc = logging.FullName
            
            #Check if existing log is present
            if not os.path.isfile(new_file_loc):
                log_name = logging.FullName
                
                with open(log_name, 'w') as fp:
                    fp.write('Task')

            else:
                #custom incremental logging
                count = 1
                while True:
                    logging.FullName = file_loc+ "\\" +log_name+r'{MeasurementStart}'+'_'+str(count)+log_type
                    new_file_loc = logging.FullName
                    #print(new_file_loc)

                    if not os.path.isfile(new_file_loc):
                        log_name = new_file_loc
                        
                        with open(log_name, 'w') as fp:
                            fp.write('Task')
                        break
                    
                    count+=1

            if logging.FullName == log_name:
                status = True

            return status
       
    def get_log_name(self, logging_block_num):
        logging = CANalyzerAUD.__CANanlyzer.Configuration.OnlineSetup.LoggingCollection(logging_block_num)
        return logging.FullName

if __name__ == "__main__":
    
    
    App = CANalyzerAUD('PT_config.cfg')

    print(App.get_log_name(1))
    App.set_logging(log_name='Flexray')
    App.init_measurements()
    
    print(App.get_log_name(1))
    #print(App.start_measurements())
    '''
    #print(App.start_measurements())
    #time.sleep(5)
    #print(App.stop_measurements())
    #time.sleep(3)
    App.check()
    App.cleanup()
    ''' 
    
    App.check_if_CANalyser()
    '''
    for n in range(0, 10):
        print(App.set_logging(log_name='Flexray'))

    '''
    #print(App.stop_measurements())

    #print(App.close_CANanlyser())