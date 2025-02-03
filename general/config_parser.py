from general.utils import singletone
import os
#-------------------------#config(.ini)_parsing#--------------------------------#


from configparser import ConfigParser

class parser(singletone):
    def __init__(self):
        super().__init__()
        if not self.initialized:
            self.parser = ConfigParser()
            self.currentfile = None
            self.initialized = True
        return
    
    def parsefile(self, path: str, encode = 'utf-8'):
        if not os.path.exists(path):
            raise ValueError
        elif self.currentfile == path:
            return
        self.parser.clear()
        self.currentfile = path        
        self.parser.read(path, encode)
        return self.parser
    
    def getSection(self, name: str):
        return self.parser.items(name)