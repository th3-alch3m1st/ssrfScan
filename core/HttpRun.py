import requests

class HttpRun:

    def connection(host, path, method, parameters, headers):
        print(host + path)
        if method == 'GET':
            url = host + path + '?' + parameters
            conn = requests.get(url, headers=headers)
        elif method == 'POST':
            url = host + path
            conn = requests.post(url, data=parameters, headers=headers)
        elif method == 'PUT':
            url = host + path
            conn = requests.put(url, data=parameters, headers=headers)
        elif method == 'PATCH':
            url = host + path
            conn = requests.patch(url, data=parameters, headers=headers)
        elif method == 'DELETE':
            url = host + path
            conn = requests.delete(url, headers=headers)
        elif method == 'OPTIONS':
            url = host + path
            conn = requests.options(url, headers=headers)

        print(conn)
        conn.close()

