import base64

class HttpHeaders:

    def headersBuilder(config, host, path, headers):
        # Remove the Host: example.com line/header
        parse_headers = headers.split(' || ')[1:]

        '''
            Need to do sth with the Referer Header and with the User-Agent
        '''

        old_headers = {}
        new_headers = {}
        for header in parse_headers:
            if header.find(':') > -1:
                name, value = header.split(':')[0], header.split(':')[1]
                value = value.replace(' ', '')
                old_headers[name] = value
                new_headers[name] = value

        '''
            Build payload ssrfpayload + base64(host + path + header)
            It will be easier to identify where the call came from.
        '''
        for header in config.headers:
            payload = host + path + '?' + header
            payload_bytes = payload.encode('ascii')
            base64_bytes = base64.b64encode(payload_bytes)
            payload_base64 = base64_bytes.decode('ascii')
            new_headers[header] = config.ssrfpayload + '/' + payload_base64
        print(old_headers)
        print(new_headers)
        return old_headers, new_headers
