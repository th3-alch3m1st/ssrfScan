import sys
from core.Config import Config
from core.CSVParser import CSVParser

def main():

    config = Config()

    print(config.fcsv, config.bearer)
    #sys.exit(1)

    CSVParser(config)

if __name__ == '__main__':
    main()
