import sys
from core.Config import Config
from core.HttpParser import HttpParser

def main():

    config = Config()

    print(config.fcsv, config.bearer)
    #sys.exit(1)

    HttpParser(config)

if __name__ == '__main__':
    main()
