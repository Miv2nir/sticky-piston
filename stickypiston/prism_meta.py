
import requests, json, pathlib
from stickypiston import util, traverse
def get_prism_meta(save=False):
    '''Pulls https://meta.prismlauncher.org/v1/. 
    The full directory info can be seen at https://github.com/PrismLauncher/meta-launcher'''
    response=requests.get('https://meta.prismlauncher.org/v1/')
    if response.status_code==200:
        if save: #instructed to write the file down
            util.generate_meta_dir('meta-prism')
            p=pathlib.Path('./meta-prism/')
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

def _make_top_dir(url):
    base_url='https://meta.prismlauncher.org/v1/'
    dirpath=url.replace(base_url,'./meta-prism/')
    pathlib.Path(dirpath).mkdir(parents=True,exist_ok=True)
    return pathlib.Path(dirpath)

def _maven_to_path_v1(url,name):
    versionless_name='/'.join(name.split(':')[:-1])
    version=name.split(':')[-1]
    base_url=url+versionless_name.replace('.','/')+'/'+version
    jar_filename_other='-'.join(name.split(':')[1:])+'.jar'
    other_jar_url=base_url+'/'+jar_filename_other
    return other_jar_url
    

def download(meta_json,download_all,wishlist=[]):
    '''Initiates the recursive download process with additional help specific to the prism's meta api formats'''
    base_url='https://meta.prismlauncher.org/v1/'
    url_list=parse_prism_meta(meta_json)
    
    root_dir=pathlib.Path('./meta-prism/')
    for url in url_list:
        if not download_all and not (url.replace(base_url,'') in wishlist):
            print(url,'not in wishlist, skipping.')
            continue
        #this is a mess generally speaking so there's gonna be another parsing round for each
        #the resolution of all names is done by following the structure of i['version'] in json['versions']
        #net.fabricmc.intermediary (some jsons contain spaces, remember to use %20 encoding)
        print('Working on',url)
        cwd=_make_top_dir(url)
        print(cwd)
        index_json=util.download_json(url,cwd,save=True,filename='index.json')
        #pull package.json
        util.download_json(url+'/package.json',cwd,save=True)
        #iterate through index.json turning versions into urls
        for i in index_json['versions']:
            version=i['version']
            #get the version json
            print('Downloading',version)
            #the problem here is that sometimes url needs to be resolved manually
            #ill write this part out in a more verbose manner and clean it up later (eventually)
            if 'com.mumfrey.liteloader' in url or\
                'net.fabricmc.fabric-loader' in url:
                #requires a special parsing of the json
                json_obj=util.download_json(url+'/'+version+'.json',cwd,save=True)
                #looking at the case of 1.12.2-SNAPSHOT.json
                #print(json_obj['libraries'])
                for i in range(len(json_obj['libraries'])):
                    if not 'url' in json_obj['libraries'][i].keys():
                        continue
                    else:
                        base_url=json_obj['libraries'][i]['url']
                        #print(base_url)
                        if base_url[-1]!='/':
                            base_url+='/'
                        #print(_maven_to_path_v1(base_url,json_obj['libraries'][i]['name']))
                        new_url=_maven_to_path_v1(base_url,json_obj['libraries'][i]['name'])
                        try:
                            traverse.recursive_download(new_url,\
                            util.path_from_url(new_url,mkdir=True,prism=True),prism=True)
                        except requests.HTTPError as e:
                            #likely the case of 
                            if e.response.status_code==501:
                                #maven wants https
                                traverse.recursive_download(new_url.replace('http://','https://'),\
                            util.path_from_url(new_url,mkdir=True,prism=True),prism=True)
                            else:
                                #it's something else
                                raise e
            elif 'net.minecraft' in url:
                #blind download and also assets
                json_obj=util.download_json(url+'/'+version+'.json',cwd,save=False)
                #not saving it here cuz the rest will be left for the recursive download
                asset_url=json_obj['assetIndex']['url']
                print(asset_url)
                asset_cwd=util.path_from_url(asset_url,mkdir=True,prism=True)
                print(asset_cwd)
                assets_json=util.download_json(asset_url,asset_cwd,save=True)
                print('Downloading assets...')
                for j in assets_json['objects']:
                    #collect the path
                    item=assets_json['objects'][j]
                    print(item)
                    asset_item_url='https://resources.download.minecraft.net/'+item['hash'][:2]+'/'+item['hash']
                    print(asset_item_url)
                    asset_item_path=util.path_from_url(asset_item_url.replace(item['hash'],''),mkdir=True,prism=True)
                    print(asset_item_path)
                    traverse.recursive_download(asset_item_url,asset_item_path,prism=True)
                    #exit(0)
                print('Downloading the rest...')
                traverse.recursive_download(url+'/'+version+'.json',cwd,prism=True)
                exit(0)
            else: #perform a blind download
                traverse.recursive_download(url+'/'+version+'.json',cwd,prism=True)
    return 'The download has finished successfully!'