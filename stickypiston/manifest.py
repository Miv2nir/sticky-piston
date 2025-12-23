#this file houses functions that will pull version_manifest_v2.json for later processing, as well as the actual downloader logic

import requests
def get():
    '''Pulls https://piston-meta.mojang.com/mc/game/version_manifest_v2.json'''
    response=requests.get('https://piston-meta.mojang.com/mc/game/version_manifest_v2.json')
    if response.status_code==200:
        return response.json()
    else:
        raise ('PistonMetaUnreachableError')
    