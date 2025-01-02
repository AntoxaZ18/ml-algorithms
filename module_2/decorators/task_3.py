#Задание 3
class safe_write:
    '''context manager for safety writing to file
        works in both binary and text modes
        rollback file if exception occures
    '''
    def __init__(self, file_path, mode='a'):
        self.file_path = file_path
        self.mode = mode
        self.file_handle = None #file handler
        self.pos = 0    #position in open file

    def __enter__(self):
        if self.mode == 'a':
            self.file_handle = open(self.file_path, self.mode, encoding='utf-8') 
        elif self.mode == 'ab':
            self.file_handle = open(self.file_path, self.mode)
        else:
            raise RuntimeError(f'cannot open file with mode {self.mode}') 
            
        self.pos = self.file_handle.tell()
        return self

    def write(self, data):
        try:
            self.file_handle.write(data)
        except Exception:
            self.file_handle.truncate(self.pos)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f'Во время записи в файл было возбуждено исключение {exc_type}')
        self.file_handle.close()


with safe_write('undertale.txt') as file:
    file.write('Язнаю,что ничего не знаю, но другие не знают и этого.')

try:
    with safe_write('undertale.txt') as file:
        file.write('Если ты будешь любознательным, то будешь много знающим.', flush=True)
        raise ValueError
except Exception:
    pass

with open('undertale.txt', encoding='utf-8') as file:
    print(f'Содержимое файла: "{file.read()}"')