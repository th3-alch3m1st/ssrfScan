import csv
import core.Config

class CSVParser:

    def __init__(self, config, fcsv, domain):
        self.config = config
        self.fcsv = fcsv
        self.domain = domain

    def parse(self):
        readCSV = open(self.fcsv, 'r')
        data = csv.DictReader(readCSV)
        for row in data:
            if row['Request.Hostname'] == self.domain:
                # Run the HTTP Headers Scan
                # HttpHeaders.process(config, row)
                method = row['Request.Method']
                if method == 'GET':
                    pass
                    #HttpMethods.getBuilder(self.config, row)
                elif method == 'POST':
                    pass
                    #postParamsBuilder(row)
                elif method == 'PUT':
                    pass
                    #putParamsBuilder(row)
                elif method == 'OPTIONS':
                    pass
                    #optionsParamsBuilder(row)
