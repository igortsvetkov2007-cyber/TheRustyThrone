import os

path='main/TRT_main.py'

if os.path.exists('main/TRT_main.py'):
    os.system(f'python {path}')
else:
    print(f'Target main bot file on path {path} does not exist!')
