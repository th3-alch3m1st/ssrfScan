import configparser
import sys
import os
import argparse

globalVariables = {}

class Config:

    def __init__(self):
        self.set_config()
        self.getHeaders()
        self.getParameters()
        self.getArgs()

    def set_config(self):
        self.chunkSize = 5
        self.ssrfpayload = 'http://test'
        self.timeout = 5

    def getParameters(self):
        file = "./db/parameters.txt"

        if not os.path.exists(file):
            sys.exit("Parameters list not found")

        parameters = open(file, "r").read().splitlines()

        if len(parameters) == 0:
            sys.exit("Parameters list is empty")

        self.parameters = parameters

    def getHeaders(self):
        file = "./db/headers.txt"
        if not os.path.exists(file):
            sys.exit("Headers list not found")

        headers = open(file, "r").read().splitlines()

        if len(headers) == 0:
            sys.exit("Headers list is empty")

        self.headers = headers

    def getArgs(self):
        parser = argparse.ArgumentParser(description='Parse .csv export from Burp Suite using Logger++ and run SSRF scanner')

        parser.add_argument('-i', type=str, help='.csv file to process', dest='fcsv')
        parser.add_argument('-d', type=str, help='domain to run scans on', dest='domain')
        parser.add_argument('-C', type=str, help='cookies to update existing ones in .csv', dest='cookies', default='')
        parser.add_argument('-H', type=str, help='Is there an Authorization header you want to update?', dest='bearer', default='')

        args = parser.parse_args()

        self.fcsv = args.fcsv
        self.domain = args.domain
        self.cookies = args.cookies
        self.bearer = args.bearer


