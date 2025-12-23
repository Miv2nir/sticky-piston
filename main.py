import sys
from stickypiston import manifest

def main():
    print(sys.argv)
    #parse cli args
    #no args - display help
    #download - performs the whole download routine (redownloading should fail unless approved, then make a backup of the old directories and perform the whole routine again)
    #start - spins up a web server that mimicks piston-meta, prompts the user to subsitute the ip address in hosts file

if __name__ == '__main__':
    main()