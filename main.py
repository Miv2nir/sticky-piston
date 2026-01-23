import sys
from stickypiston import manifest,prism_meta

def display_help():
    print('stickypiston - a tool for downloading piston-meta.mojang.com API content.\n\
            Version 0.2.0\n\
            Usage:\n\
            ./main.py download-mojang - downloads the release and old versions content from the API.\n\
            ./main.py download-mojang all - downloads all content from the API.\n\
            ./main.py download-prism - downloads the release and old versions content from the PrismLauncher API.\n\
            ./main.py - displays this message.')

def main():
    print(sys.argv)
    #parse cli args
    #no args - display help
    #download - performs the whole download routine (redownloading should fail unless approved, then make a backup of the old directories and perform the whole routine again)
    #start - spins up a web server that mimicks piston-meta, prompts the user to subsitute the ip address in hosts file
    try:
        if sys.argv[1]=='download-mojang':
            print('Initiating download of mojang\'s API...')
            manifest_json=manifest.get_manifest(save=True)
            print('version_manifest_v2.json has been successfully downloaded.')
            print('Starting the download...')
            try:
                download_all=sys.argv[2]=='all'
            except:
                download_all=False
            status=manifest.download(manifest_json,download_all)
            print(status)
            return True
        elif sys.argv[1]=='download-prism':
            print('Initiating the download of PrismLauncher\'s metadata API...')
            meta_json=prism_meta.get_prism_meta(save=True)
            print('index.json has been successfully downloaded.')
            print('Starting the download...')
            status=prism_meta.download(meta_json)
            return True
        else:
            display_help()
    except IndexError: #no argument was passed
        display_help()

if __name__ == '__main__':
    main()