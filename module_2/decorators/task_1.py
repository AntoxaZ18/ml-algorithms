#Задание 1

import functools

user_role = 'user'

def role_required(role: str):

    def check_role(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if user_role == role:
                return f(*args, **kwargs)
            else:
                return 'Permission denied'

        return wrapper

    return check_role            

@role_required('admin')
def secret_source():
    '''func get access to resource'''
    return 'Permission accepted'

user_role = 'admin'
print(secret_source())

user_role = 'user'
print(secret_source())