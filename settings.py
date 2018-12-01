
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Class TaskManager is a Singleton
class Settings(object, metaclass=Singleton):
    def __init__(self):
        self.RES_DIR = 'TwitterImgCrawler_Resources'
        self.CONFIGURE = 'TwitterImgCrawler.ini'
