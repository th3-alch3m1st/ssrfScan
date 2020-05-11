import csv
from core.HttpHeaders import HttpHeaders
from core.HttpParameters import HttpParameters
from core.HttpRun import HttpRun

class CSVParser:

    def __init__(self, config):
        self.config = config
        self.parse()

    def parse(self):
        readCSV = open(self.config.fcsv, 'r')
        data = csv.DictReader(readCSV)
        i = 0
        for row in data:
            if row['Request.Hostname'] == self.config.domain:
                # Build Request
                method  = row['Request.Method']
                host    = row['Request.Host']
                path    = row['Request.Path']
                old_headers, new_headers = HttpHeaders.headersBuilder(self.config, row)
                Parameters = HttpParameters(self.config, row)
                old_parameters, new_parameters = Parameters.processParameters()
                # Headers Fuzzing
                HttpRun.connection(host, path, method, old_parameters, new_headers)
                # Parameters Fuzzing
                HttpRun.connection(host, path, method, new_parameters[0], old_headers)
                break

