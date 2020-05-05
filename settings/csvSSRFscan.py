import csv, os, sys, json
import http.client
from subprocess import Popen, STDOUT, PIPE

options = sys.argv[1:]
if len(options) < 2:
    sys.stderr.write("Usage: %s csv_file headers\n" % sys.argv[0])
    sys.exit(1)

if len(options) >= 2 :
    headers2 = sys.argv[2]

collaborator = 'test'

def isJSON(data):
    try:
        json_object = json.loads(data)
    except ValueError as e:
        return False
    return True

def getParamsBuilder(row):
    url = row['Request.Host'] + row['Request.Path']
    method = '--get'
    params = ''
    if row['Request.HasParams'] == 'TRUE':
        params = row['Request.Query']
    arjun(url, method, params)

def postParamsBuilder(row):
    url = row['Request.Host'] + row['Request.Path']
    method = '--post'
    params = ''
    if row['Request.HasParams'] == 'TRUE':
        params = row['Request.Body']
        if isJSON(params):
            method = '--json'
    arjun(url, method, params)

def putParamsBuilder(row):
    print('PUT DATA\n')

def optionsParamsBuilder(row):
    print('OPTIONS Request\n')

def headersFuzzer(row):
    httpHeaders = open('./http-headers.txt', 'r')
    headers = {'X-Forwarded-For': "'" + row['Request.Hostname'] + "." + collaborator + "'"}

    connection = http.client.HTTPSConnection(row['Request.Hostname'],row['Request.Port'], timeout=5)
    connection.request(row['Request.Method'], row['Request.Path'], body=None, headers=headers)

    response = connection.getresponse()
    print(response.status, response.reason, headers)
    connection.close()


def arjun(url, method, params):
    print('Run Arjun on %s with %s method and --include %s parameters and %s headers' % (url, method, params, headers2))


fcsv = open(sys.argv[1], 'r')

data = csv.DictReader(fcsv)
for row in data:
    if row['Request.Hostname'] == 'app.wavecell.com':
        headersFuzzer(row)
        method = row['Request.Method']
        if method == 'GET':
            getParamsBuilder(row)
        elif method == 'POST':
            postParamsBuilder(row)
        elif method == 'PUT':
            putParamsBuilder(row)
        elif method == 'OPTIONS':
            optionsParamsBuilder(row)
