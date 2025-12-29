#helper functions for other things

import pathlib, requests, json

def generate_meta_dir():
    '''Creates a meta directory'''
    pathlib.Path('./meta').mkdir(parents=True, exist_ok=True)
    
def download_json(url,cwd,save=False):
    '''Pulls any given json over a url'''
    response=requests.get(url)
    local_filename = url.split('/')[-1]
    if response.status_code==200:
        if save: #instructed to write the file down
            filepath = cwd/local_filename
            with filepath.open("w",encoding="utf-8") as f:
                json.dump(response.json(),f)
        return response.json()
    else:
        raise ('UrlUnreachableError')
    
def path_from_url(url,mkdir=False):
    #url is a string
    #piston-meta.mojang.com goes in its own directory
    #libraries.minecraft.net goes in its own directory as well
    cwd='./meta/'
    #parse the url
    l=url.split('/')[2:] #trim out the https:// part
    for i in l:
        cwd+=(i+'/')
    if mkdir:
        pathlib.Path(cwd).mkdir(parents=True,exist_ok=True)
    return pathlib.Path(cwd)
    