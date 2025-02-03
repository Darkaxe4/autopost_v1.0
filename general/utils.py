class singletone(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(singletone, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = False
        return