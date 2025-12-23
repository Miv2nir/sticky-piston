#helper functions for other things

import pathlib

def generate_meta_dir():
    '''Creates a meta directory'''
    pathlib.Path('./').mkdir(parents=True, exist_ok=True)