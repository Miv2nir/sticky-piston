import sys
from stickypiston import manifest

def display_help():
    print('stickypiston - a tool for downloading piston-meta.mojang.com API content.\n\
            Version 0.1.1\n\
            Usage:\n\
            ./main.py download - downloads the release and old versions content from the API.\n\
            ./main.py download all - downloads all content from the API.\n\
            ./main.py - displays this message.')

def main():
    print(sys.argv)
    #parse cli args
    #no args - display help
    #download - performs the whole download routine (redownloading should fail unless approved, then make a backup of the old directories and perform the whole routine again)
    #start - spins up a web server that mimicks piston-meta, prompts the user to subsitute the ip address in hosts file
    try:
        if sys.argv[1]=='download':
            print('Initiating download...')
            manifest_json=manifest.get_manifest(save=True)
            print('version_manifest_v2.json has been successfully downloaded.')
            print('Starting the download...')
            status=manifest.download(manifest_json)
            print(status)
            return True
        else:
            display_help()
    except IndexError: #no argument was passed
        display_help()

if __name__ == '__main__':
    main()