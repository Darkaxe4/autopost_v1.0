from general.utils import singletone
from general.config_parser import parser
import os
#--------------------------#logger#---------------------------------------------------#

import datetime

class logger(singletone):
    def __init__(self, path = 'config.ini'):
        super().__init__()
        if not self.initialized:
            self.instance.loadconfig(path)
            self.loglines = []
            self.initialized = True
        return

    def loadconfig(self, path):
        if not os.path.exists(path):
            raise ValueError
        parser.instance.parsefile(path)
        for name, value in parser.instance.getSection("settings"):
            self.__setattr__(name, value)
        match self.logging.lower():
            case "1"|"true"|"on"|"enabled":
                self.logging = True
            case "0"|"false"|"off"|"disabled":
                self.logging = False
            case _:
                raise ValueError("Logging parameter can only be on or off (1/0, True/false)")
        match self.live_log.lower():
            case "1"|"true"|"on"|"enabled":
                self.live_log = True
            case "0"|"false"|"off"|"disabled":
                self.live_log = False
            case _:
                raise ValueError("Logging parameter can only be on or off (1/0, True/false)")
        
    def setArgs(self, args):
        if args.enablelogging:
            self.logging = True
        if args.livelog:
            self.live_log = True
        if not(args.log_path is None):
            self.log_path = args.log_path


    def log(self, *text):
        for line in text:
            self.loglines.append(str(datetime.datetime.now())[:19]+"\t"+ line)
            if self.live_log:
                print(line)

    def savelog(self):
        with open(self.log_path+'log_'+str(datetime.datetime.now().date())+'.txt', 'a') as f:
            for line in self.loglines:
                f.write(line+"\n")



def push_to_log(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except:
            logger.instance.log(f"Program run through an error at {func.__name__} with args: {args, kwargs}")
        logger.instance.log(f"{func.__name__}({args, kwargs}) :\t{result}")
    return wrapper