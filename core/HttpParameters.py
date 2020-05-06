import re

class HttpParameters:

    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.processParameters()

    def buildPayloadList(self):
        '''
            Build payloads: par1=attackerURL&par2=attackerURL...
        '''
        payloads = []
        counter = int(len(self.config.parameters) / self.config.chunkSize)
        for i in range(0, counter):
            payload = self.config.parameters[i * self.config.chunkSize] + '=' + self.config.ssrfpayload
            for j in range(1, self.config.chunkSize):
                payload += "&" + self.config.parameters[i * self.config.chunkSize + j] + '=' + self.config.ssrfpayload
            payloads.append(payload)
        # Add the leftover parameters
        if (counter * self.config.chunkSize) < len(self.config.parameters):
            payload = self.config.parameters[counter * self.config.chunkSize] + '=' + self.config.ssrfpayload
            for i in range(counter * self.config.chunkSize + 1, len(self.config.parameters)):
                payload += "&" + self.config.parameters[i] + '=' + self.config.ssrfpayload
            payloads.append(payload)
        return payloads


    def processParameters(self):
        # 1st option - No parameters in the Request, so fuzz for the ones in the parameters.txt file
        # Split the Requests based on the chunkSize, if 5 then it will add 5 parameters per Request
        if self.data['Request.Query'] == 'null' and self.data['Request.Body'] == '':
            payloads = self.buildPayloadList()
            self.payloads = payloads

        # 2nd option - We got GET Request with query parameters
        # Check if a query parameter is in the parameters.txt, if yes change it to our payload/url
        # If not just send the payloads and append the query params too
        if self.data['Request.Query'] != 'null':
            query = self.data['Request.Query']
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
                    query = self.data['Request.Query']
                    for instance in instances:
                        if payload.find(instance+'=') > -1:
                            # If you find url=ex in the payload and in the query, remove it from the query and keep the payload one
                            query = re.sub('&' + instance + '(=[^&]*)?|^' + instance +'(=[^&]*)?&?', '', query)
                    updated_payloads.append(payload + '&' + query)

            self.payloads = updated_payloads
