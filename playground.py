import win32com
from win32com.client import DispatchEx
from utils.resilience import *
from utils.exception_PT import *
import time

class CANalyzerAUD:

    #private 
    ___CANanlyzer = None
    ___Measurement = None

    def __init__(self, config_path):

        try : 
            CANalyzerAUD.__CANanlyzer = DispatchEx('CANalyzer.Application')
            CANalyzerAUD.__CANanlyzer.Open(config_path)
        
        except Exception as e:
            raise CANalyzerExpection("Couldn't create COM object")



    def init_measurements(self):
        CANalyzerAUD.___Measurement = CANalyzerAUD.__CANanlyzer.Measurement


    def start_measurements(self):
        status = False
        CANalyzerAUD.___Measurement.Start()

        if self.is_measurements_runing:
            status = True

        return status

    def stop_measurements(self):
        status = False
        CANalyzerAUD.___Measurement.Stop()

        if not self.is_measurements_runing():
            status = True

        return status

    def is_measurements_runing(self):
        return CANalyzerAUD.___Measurement.Running

    def cleanup(self):
        CANalyzerAUD.__CANanlyzer.Quit()
        CANalyzerAUD.__CANanlyzer = None
        CANalyzerAUD.___Measurement = None

    def check(self):
        CANalyzerAUD.___Measurement.OnlineMode('Vector Tool Platform')

if __name__ == "__main__":
    
    App = CANalyzerAUD('PT_config.cfg')
    App.init_measurements()
    #print(App.start_measurements())
    #time.sleep(5)
    #print(App.stop_measurements())
    #time.sleep(3)
    App.check()
    #App.cleanup()
