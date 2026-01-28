#helper functions for other things

import pathlib, requests, json

def generate_meta_dir(name='meta'):
    '''Creates a meta directory'''
    pathlib.Path('./'+name).mkdir(parents=True, exist_ok=True)
    
def download_json(url,cwd,save=False,filename=None):
    '''Pulls any given json over a url'''
    response=requests.get(url)
    if filename==None:
        local_filename = url.split('/')[-1]
    else:
        local_filename=filename
    if response.status_code==200:
        if save: #instructed to write the file down
            filepath = cwd/local_filename
            with filepath.open("w",encoding="utf-8") as f:
                json.dump(response.json(),f)
        return response.json()
    else:
        raise ('UrlUnreachableError')

#def download_json_prism(url,cwd,local_filename='index.json',save=False):
#    '''Pulls any given json over a url and stores it at ./meta_prism/'''
#    response=requests.get(url)
#    base_url='https://meta.prismlauncher.org/v1/'
#    if response.status_code==200:
#        if save: #instructed to write the file down
#            filepath = cwd/local_filename
#            with filepath.open("w",encoding="utf-8") as f:
#                json.dump(response.json(),f)
#        return response.json()
#    else:
#        raise ('UrlUnreachableError')
    
def path_from_url(url,mkdir=False):
    #url is a string
    #piston-meta.mojang.com goes in its own directory
    #libraries.minecraft.net goes in its own directory as well
    cwd='./meta/'
    #parse the url
    l=url.split('/')[2:-1] #trim out the https:// part and the
    for i in l:
        cwd+=(i+'/')
    if mkdir:
        pathlib.Path(cwd).mkdir(parents=True,exist_ok=True)
    return pathlib.Path(cwd)
    