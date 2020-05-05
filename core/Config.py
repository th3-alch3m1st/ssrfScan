import configparser
import sys

globalVariables = {}

class Config:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')

        self.getHeaders()
        self.getParameters()

    def getParameters(self):
        file = self.config["files"]["Parameters"]

        if not os.path.exists(file):
            sys.exit("Parameters list not found")

        parameters = open(file, "r").read().splitlines()

        if len(parameters) == 0:
            sys.exit("Parameters list is empty")

        self.parameters = parameters

    def getHeaders(self):
        file = self.config["files"]["Headers"]

        if not os.path.exists(file):
            sys.exit("Headers list not found")

        headers = open(file, "r").read().splitlines()

        if len(headers) == 0:
            sys.exit("Headers list is empty")

        self.headers = headers

