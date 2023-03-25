import os
import datetime

class Log:
    def __init__(self, filename, file_mode = "a"):
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok = True)

        self.handle = open(os.path.abspath(filename), file_mode)
    
    def write_error(self, message):
        self.handle.write(f"{datetime.datetime.strftime(datetime.datetime.now(), '[%d/%m/%Y %H:%M:%S]')} ERROR [!] {message}")
        self.handle.flush()
    
    def write_warning(self, message):
        self.handle.write(f"{datetime.datetime.strftime(datetime.datetime.now(), '[%d/%m/%Y %H:%M:%S]')} WARNING [!] {message}")
        self.handle.flush()
    
    def write_information(self, message):
        self.handle.write(f"{datetime.datetime.strftime(datetime.datetime.now(), '[%d/%m/%Y %H:%M:%S]')} INFO [i] {message}")
        self.handle.flush()
    
    def close(self):
        self.handle.close()
    
