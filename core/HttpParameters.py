import re
import json
import base64
from urllib.parse import parse_qs
from urllib.parse import urlencode

class HttpParameters:

    def __init__(self, config, host, path, query, body):
        self.config = config
        self.host = host
        self.path = path
        self.query = query
        self.body = body

    def is_xml(self, query):
        pass

    def is_json(self, query):
        try:
            json_object = json.loads(query)
        except ValueError as e:
            return False
        return True

    def base64Payload(self, payload):
        payload_bytes = payload.encode('ascii')
        base64_bytes = base64.b64encode(payload_bytes)
        payload_base64 = base64_bytes.decode('ascii')
        return payload_base64

    def buildPayloadList(self):
        '''
            Build payloads: par1=attackerURL&par2=attackerURL...
        '''
        payloads = []
        counter = int(len(self.config.parameters) / self.config.chunkSize)
        for i in range(0, counter):
            parameter = self.config.parameters[i * self.config.chunkSize]
            ssrfpayload = self.config.ssrfpayload + '/' + self.base64Payload(self.host + self.path + '?' + parameter)
            payload = parameter + '=' + ssrfpayload
            for j in range(1, self.config.chunkSize):
                parameter = self.config.parameters[i * self.config.chunkSize + j]
                ssrfpayload = self.config.ssrfpayload + '/' + self.base64Payload(self.host + self.path + '?' + parameter)
                payload += "&" + parameter + '=' + ssrfpayload
            payloads.append(payload)
        # Add the leftover parameters
        if (counter * self.config.chunkSize) < len(self.config.parameters):
            parameter = self.config.parameters[counter * self.config.chunkSize]
            ssrfpayload = self.config.ssrfpayload + '/' + self.base64Payload(self.host + self.path + '?' + parameter)
            payload = parameter + '=' + ssrfpayload
            for i in range(counter * self.config.chunkSize + 1, len(self.config.parameters)):
                parameter = self.config.parameters[i]
                ssrfpayload = self.config.ssrfpayload + '/' + self.base64Payload(self.host + self.path + '?' + parameter)
                payload += "&" + parameter + '=' + ssrfpayload
            payloads.append(payload)
        return payloads


    def processParameters(self):
        # 1st option - No parameters in the Request, so fuzz for the ones in the parameters.txt file
        # Split the Requests based on the chunkSize, if 5 then it will add 5 parameters per Request
        old_parameters = ''
        if self.query == None and self.body == b'':
            new_parameters = self.buildPayloadList()

        # 2nd option - We got GET Request with query parameters or POST Request with parameters in the body in QueryString/JSON format
        # Check if a query parameter is in the parameters.txt, if yes change it to our payload/url
        # If not just send the payloads and append the query params too
        # Convert QueryString to JSON - dict((itm.split('=')[0],itm.split('=')[1]) for itm in query.split('&')) OR json.dumps(parse_qs(query))
        # Convert JSON to QueryString - 
        else:
            if self.query != None:
                query = self.query
            elif self.body != b'':
                # The body is of byte type so decode it using utf-8
                query = self.body.decode('utf-8')
            old_parameters = query

            # If data is in JSON convert it to normal, edit them and change them back to JSON
            json_data = False
            if self.is_json(query):
                json_data = True
                print('[**] JSON data: %s' % query)
                json_query = json.loads(query)
                query = urlencode(json_query)
                print('[**] QueryString data: %s' % query)
                print('[***] converted JSON to QueryString')
            elif self.is_xml(query):
                print('Nothing to see')

            query_params = query.split('&')
            key_list = []
            for entry in query_params:
                key_list.append(entry.split('=')[0])

            # Check if any of the parameters.txt values is in the query parameters
            instances = list(set(key_list)&set(self.config.parameters))
            updated_payloads = []
            payloads = self.buildPayloadList()
            if instances == []:
                for payload in payloads:
                    updated_payloads.append(payload + '&' + query)
            else:
                for payload in payloads:
                    updateQuery = query
                    for instance in instances:
                        if payload.find(instance+'=') > -1:
                            # If you find url=ex in the payload and in the query, remove it from the query and keep the payload one
                            updateQuery = re.sub('&' + instance + '(=[^&]*)?|^' + instance +'(=[^&]*)?&?', '', updateQuery)
                    updated_payloads.append(payload + '&' + updateQuery)

            new_parameters = updated_payloads
            if json_data:
                new_parameters = []
                for payload in updated_payloads:
                    json_payload = dict((itm.split('=')[0],itm.split('=')[1]) for itm in payload.split('&'))
                    new_parameters.append(json_payload)

        return old_parameters, new_parameters
