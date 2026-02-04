import requests, json, pathlib
from stickypiston import util
import validators, re

def _download_file(url,cwd:pathlib.Path):
    '''https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    will skip redownloading existing files'''
    local_filename = url.split('/')[-1]
    target=cwd/local_filename
    if target.is_file():
        #file exists, skip
        return local_filename
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(cwd/local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

def _extract_urls(json_obj:str):
    '''https://stackoverflow.com/a/38731035'''
    #return re.findall("((www\.|http://|https://)(www\.)*.*?(?=(www\.|http://|https://|$)))", str(json_obj))
    return re.findall("http[s]?://(?:(?!http[s]?://)[a-zA-Z]|[0-9]|[$\-_@.&+/]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(json_obj))

def recursive_download(url, cwd:pathlib.Path,prism=False):
    '''Traverses given json files and downloads all files in their respective directories'''
    #handle prism url
    #this must be able to blindly handle all of the given json files
    print(url)
    #get what we are downloading exactly
    is_json=(url[-4:]=='json')
    
    #write the file
    if not is_json:
        #just download the file into cwd and exit
        _download_file(url,cwd)
        return True
    else:
        #must save both the json file for later serving...
        json_obj=util.download_json(url,cwd,save=True)
        #... and process the rest of what it has on offer
        url_list=_extract_urls(json_obj)
        for url in url_list:
            #url contains the domain name where a file is saved at, thus the next cwd must be formed beforehand
            new_cwd=util.path_from_url(url,mkdir=True,prism=prism)
            #recurse through the rest of the json
            recursive_download(url,new_cwd,prism)
            
    