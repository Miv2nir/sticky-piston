
import requests, json, pathlib
from stickypiston import util, traverse
def get_prism_meta(save=False):
    '''Pulls https://meta.prismlauncher.org/v1/. The full directory info can be seen at https://github.com/PrismLauncher/meta-launcher'''
    response=requests.get('https://meta.prismlauncher.org/v1/')
    if response.status_code==200:
        if save: #instructed to write the file down
            util.generate_meta_dir('meta_prism')
            p=pathlib.Path('./meta_prism/')
            filepath = p/"index.json"
            with filepath.open("w",encoding="utf-8") as f:
                json.dump(response.json(),f)
        return response.json()
    else:
        raise ('MetaPrismUnreachableError')

def parse_prism_meta(meta_json):
    '''Turns the provided json into dictionary and a list of versions'''
    base_url='https://meta.prismlauncher.org/v1/'
    l=[]
    for i in meta_json['packages']:
        l.append(''.join([base_url,i['uid']]))
    return l

def download(meta_json):
    '''Initiates the recursive download process with additional help specific to the prism's meta api formats'''
    base_url='https://meta.prismlauncher.org/v1/'
    url_list=parse_prism_meta(meta_json)
    #for i in url_list:
        #this is a mess generally speaking so there's gonna be another parsing round for each
        #the resolution of all names is done by following the structure of i['version'] in json['versions']
        #net.fabricmc.intermediary (some jsons contain spaces, remember to use %20 encoding)
    #    pass