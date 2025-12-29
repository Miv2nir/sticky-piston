#this file houses functions that will pull version_manifest_v2.json for later processing, as well as the actual downloader logic

import requests, json, pathlib
from stickypiston import util, traverse
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
    l=[]
    for i in manifest_json['versions']:
        l.append(i)
    return l

def download(manifest_json):
    '''Initiates the recursive download process'''
    #cwd=pathlib.Path('./meta/')
    #mojang_path=pathlib.Path('./meta/piston-meta.mojang.com/')
    #mojang_path.mkdir(parents=True, exist_ok=True)
    #libraries_path=pathlib.Path('./meta/libraries.minecraft.net/')
    #libraries_path.mkdir(parents=True, exist_ok=True)
    #manifest is already assumed to be given
    version_list=parse_manifest(manifest_json)
    for i in version_list:
        print('Downloading',i['id'])
        cwd=util.path_from_url(i['url'],True)
        traverse.recursive_download(i['url'],cwd) #handles the downloading
    return 'The download has finished successfully!'