import csv
from core.HttpHeaders import HttpHeaders
from core.HttpMethods import HttpMethods

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
                # Run the HTTP Headers Scan
                # HttpHeaders.process(config, row)
                method = row['Request.Method']
                if method == 'GET':
                    HttpMethods.getBuilder(self.config, row)
                    print('Step ', i)
                    i += 1
                    if i > 10:
                        break
                elif method == 'POST':
                    pass
                    #postParamsBuilder(row)
                elif method == 'PUT':
                    pass
                    #putParamsBuilder(row)
                elif method == 'OPTIONS':
                    pass
                    #optionsParamsBuilder(row)
