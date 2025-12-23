#this file houses functions that will pull version_manifest_v2.json for later processing, as well as the actual downloader logic

import requests, json, pathlib
from stickypiston import util
def get_manifest(save=False):
    '''Pulls https://piston-meta.mojang.com/mc/game/version_manifest_v2.json'''
    response=requests.get('https://piston-meta.mojang.com/mc/game/version_manifest_v2.json')
    if response.status_code==200:
        if save: #instructed to write the file down
            util.generate_meta_dir()
            p=pathlib.Path('./meta/')
            filepath = p/"version_manifest_v2.json"
            with filepath.open("w",encoding="utf-8") as f:
                json.dump(response.json(),f)
        return response.json()
    else:
        raise ('PistonMetaUnreachableError')

def parse_manifest(manifest_json):
    '''Turns the provided json into dictionary and a list of versions'''
    