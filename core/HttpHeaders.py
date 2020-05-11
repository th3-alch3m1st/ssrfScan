class HttpHeaders:

    def headersBuilder(config, data):
        headers = data['Request.Headers'].split(', ')[2:]

        old_headers = {}
        new_headers = {}
        for header in headers:
            if header.find(':') > -1:
                name, value = header.split(':')[0], header.split(':')[1]
                value = value.replace(' ', '')
                old_headers[name] = value
                new_headers[name] = value

        for header in config.headers:
            new_headers[header] = config.ssrfpayload
        print(old_headers)
        print(new_headers)
        return old_headers, new_headers
