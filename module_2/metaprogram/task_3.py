from types import FunctionType 
from typing import List

function_name = 'complex_function'
parameters = ['x','y']
function_body = """
    if x > y:
        return x-y
    else:
        return y-x
"""

def generate_complex_function(name:str, args:List, code:str):
    '''function for generate function from source code'''
    func_code = compile(f'def f({", ".join(args)}):' + code, "file.py", "exec")

    return FunctionType(func_code.co_consts[0], globals(), name)


complex_func = generate_complex_function(function_name, parameters, function_body)

print(complex_func.__name__)

print(complex_func(10, 5))
print(complex_func(5, 10))



