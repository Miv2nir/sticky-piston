#helper functions for other things

import pathlib, requests, json
#from stickypiston.traverse import _extract_urls
import re
from stickypiston import util

def generate_meta_dir(name='meta'):
    '''Creates a meta directory'''
    pathlib.Path('./'+name).mkdir(parents=True, exist_ok=True)
    
def substitute_urls(json_obj,target_url):
    s=json.dumps(json_obj)
    #urls=set(_extract_urls(s))
    #for i in urls:
    #s=s.replace('http://',target_url).replace('https://',target_url)
    pattern=r"(https://)|(http://)"
    return json.loads(re.sub(pattern,target_url,s))
    
    

def download_json(url,cwd,save=False,filename=None,substitute_url=True,url_target='http://localhost/'):
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
                if not substitute_url:
                    json.dump(response.json(),f)
                else:
                    json.dump(util.substitute_urls(response.json(),url_target),f)
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
    
def path_from_url(url,mkdir=False,prism=False):
    #url is a string
    #piston-meta.mojang.com goes in its own directory
    #libraries.minecraft.net goes in its own directory as well
    if prism:
        cwd='./meta-prism/'
    else:
        cwd='./meta/'
    #parse the url
    if prism and 'meta.prismlauncher.org/v1/' in url:
        url=url.replace('https://meta.prismlauncher.org/v1/','')
        l=url.split('/')[:-1]
    else:
        l=url.split('/')[2:-1] #trim out the https:// part and the filenameWS
    for i in l:
        cwd+=(i+'/')
    if mkdir:
        pathlib.Path(cwd).mkdir(parents=True,exist_ok=True)
    return pathlib.Path(cwd)
    