from core.HttpParameters import HttpParameters

class HttpMethods:

    def processBuilder(config, data):
        # Below will return all payloads in a list
        parameters = HttpParameters(config, data)
        return parameters.payloads[0]

    def postBuilder(config, data):
        url = data['Request.Host'] + data['Request.Path']
        # Below will return all payloads in a list
        parameters = HttpParameters(config, data)
        return parameters.payloads[0]


