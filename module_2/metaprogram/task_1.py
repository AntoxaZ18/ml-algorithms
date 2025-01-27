import logging


logging.basicConfig(level=logging.INFO)


class AttrLoggingMeta(type):

    def __new__(cls, name, bases, attrs):
        for key, attr in attrs.items():
            if not key.startswith('__'):
                attrs[key] = AttrLoggingMeta.log_access(key, attr)

        return super().__new__(cls, name, bases, attrs)     
    
    def __init__(cls, name, bases, attrs, **extra_kwargs): 
        super().__init__(cls, bases, attrs, **extra_kwargs)   


    @staticmethod
    def log_access(key, attr):
        if callable(attr):
            return AttrLoggingMeta.log_call(attr)
        else:
            return property(
                fget = lambda self, k=key: AttrLoggingMeta.log_read(self, k),
                fset = lambda self, value: AttrLoggingMeta.log_write(self, key, value)
            )

    @staticmethod
    def log_call(f):
        def wrapper(*args, **kwargs):
            logging.info(f'Calling method {f.__name__}')

            return f(*args, **kwargs)
        
        return wrapper


    @staticmethod
    def log_read(obj, key):
        print('read', key)
        return obj.__dict__[key]


    @staticmethod
    def log_write(obj, key, value = 0):
        print('write', key, value)
        obj.__dict__[key] = value



class LoggedClass(metaclass = AttrLoggingMeta):
    test = 5
    def meth(self):
        return 'method 1'

    def meth_2(self):
        return 'method 2'


a = LoggedClass()
a.test = 1
print(a.__dict__)
print(a.test)
print(a.meth())
