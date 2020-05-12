import csv
from core.HttpHeaders import HttpHeaders
from core.HttpParameters import HttpParameters
from core.HttpRun import HttpRun

class HttpParser:

    def __init__(self, config):
        self.config = config
        self.parse()

    def parse(self):
        readCSV = open(self.config.fcsv, 'r')
        data = csv.DictReader(readCSV)
        for row in data:
            if row['Request.Hostname'] == self.config.domain:
                # Build Request
                method  = row['Request.Method']
                host    = row['Request.Host']
                path    = row['Request.Path']
                # Grab Headers
                old_headers, new_headers = HttpHeaders.headersBuilder(self.config, row)
                # Grab Parameters
                Parameters = HttpParameters(self.config, row)
                old_parameters, new_parameters = Parameters.processParameters()
                # Headers Fuzzing
                HttpRun.connection(host, path, method, old_parameters, new_headers)
                # Parameters Fuzzing
                print('[*] Start Fuzzing on %s via a %s Request' % (path, method))
                for parameters in new_parameters:
                    print(parameters)
                    HttpRun.connection(host, path, method, parameters, old_headers)
