import os, sys, argparse
from core.Config import Config
import core.HttpHeaders
import core.HttpRun
from core.CSVParser import CSVParser

def main():

    parser = argparse.ArgumentParser(description='Parse .csv export from Burp Suite using Logger++ and run SSRF scanner')

    parser.add_argument('-i', type=str, help='.csv file to process', dest='fcsv')
    parser.add_argument('-d', type=str, help='domain to run scans on', dest='domain')
    parser.add_argument('-C', type=str, help='cookies to update existing ones in .csv', dest='cookies', default='')
    parser.add_argument('-H', type=str, help='Is there an Authorization header you want to update?', dest='bearer', default='')

    args = parser.parse_args()

    fcsv = args.fcsv
    domain = args.domain
    cookies = args.cookies
    bearer = args.bearer

    Config.globalVariables = vars(args)
    print(core.Config.globalVariables['fcsv'])

    config = Config()

    csvparser = CSVParser(config, fcsv, domain)
    csvparser.parse()

if __name__ == '__main__':
    main()
