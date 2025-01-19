import logging


logging.basicConfig(level=logging.INFO)


class AttrLoggingMeta(type):

    def __new__(cls, name, bases, attrs):
        
        for key, attr in attrs.items():
            if callable(attr) and key != '__init__':
                attrs[key] = AttrLoggingMeta.log_access(attr)

        return super().__new__(cls, name, bases, attrs)     
    
    def __init__(cls, name, bases, attrs, **extra_kwargs): 
        cls.__setattr__ = AttrLoggingMeta.log_write(cls.__setattr__)
        cls.__getattribute__ = AttrLoggingMeta.log_read(cls.__getattribute__)

        super().__init__(cls, bases, attrs, **extra_kwargs)   


    @staticmethod
    def log_access(f):
        def wrapper(*args, **kwargs):
            logging.info(f'Calling method {f.__name__}')

            return f(*args, **kwargs)
        
        return wrapper
    @staticmethod
    def log_read(f):
        def wrapper(*args, **kwargs):

            if args[1] in ('__getattribute__', '__dict__'):
                return object.__getattribute__(*args)
            
            if not callable(object.__getattribute__(*args)):
                logging.info(f'Reading attribute {args[1]}')

            return f(*args, **kwargs)
 
        return wrapper 
    
    @staticmethod
    def log_write(f):
        def wrapper(*args, **kwargs):
            logging.info(f'Writing attribute {args[1]}')

            return f(*args, **kwargs)
        
        return wrapper  

    def __call__(cls, *args, **kwargs):  
        return super().__call__(*args, **kwargs)


class LoggedClass(metaclass = AttrLoggingMeta):

    def meth(self):
        return 'method 1'

    def meth_2(self):
        return 'method 2'


a = LoggedClass()
a.test = 1
print(a.test)
print(a.meth())
