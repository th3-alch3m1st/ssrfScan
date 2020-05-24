import requests

class HttpRun:

    def connection(endpoint, path, method, parameters, headers):
        if method == 'GET':
            endpoint += '?' + parameters
            conn = requests.get(endpoint, headers=headers)
        elif method == 'POST':
            conn = requests.post(endpoint, data=parameters, headers=headers)
        elif method == 'PUT':
            conn = requests.put(endpoint, data=parameters, headers=headers)
        elif method == 'PATCH':
            conn = requests.patch(endpoint, data=parameters, headers=headers)
        elif method == 'DELETE':
            conn = requests.delete(endpoint, data=parameters, headers=headers)
        elif method == 'OPTIONS':
            conn = requests.options(endpoint, headers=headers)

        print(conn)
        conn.close()

