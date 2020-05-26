import sqlite3
from urllib.parse import urlparse
from os.path import splitext
from core.HttpHeaders import HttpHeaders
from core.HttpParameters import HttpParameters
from core.HttpRun import HttpRun

class HttpParser:

    def __init__(self, config):
        self.config = config
        self.parse()

    def parse(self):
        readSqlite = sqlite3.connect(self.config.fsqlite)
        crsr = readSqlite.cursor()
        extensions = ['.jpg', '.css', '.js', '.jpeg', '.png', '.gif', '.ico', '.svg', '.woff2', '.ttf']
        for row in crsr.execute("SELECT TARGET_URL,HTTP_METHOD,QUERY,BODY,HEADERS FROM ACTIVITY"):
            url, method, query, body, headers = row
            url_parse = urlparse(url)
            protocol = url_parse.scheme
            #netloc = www.site.com:443
            netloc = url_parse.netloc
            host = netloc.split(':')[0]
            path = url_parse.path
            endpoint = protocol + '://' + netloc + path
            print("[*] Start on Headers request is %s", endpoint)
            if host == self.config.domain:
                # Grab Headers
                old_headers, new_headers = HttpHeaders.headersBuilder(self.config, host, path, headers)
                print(old_headers, new_headers)
                # Grab Parameters
                Parameters = HttpParameters(self.config, host, path, query, body)
                old_parameters, new_parameters = Parameters.processParameters()
                # Headers Fuzzing
                HttpRun.connection(endpoint, path, method, old_parameters, new_headers)

                if splitext(path)[1] in extensions or method == 'OPTIONS':
                    continue
                # Parameters Fuzzing
                print('[*] Start Fuzzing on %s via a %s Request' % (path, method))
                for parameters in new_parameters:
                    print(parameters)
                    HttpRun.connection(endpoint, path, method, parameters, old_headers)
