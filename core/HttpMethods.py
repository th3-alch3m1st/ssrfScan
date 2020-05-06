from core.HttpParameters import HttpParameters

class HttpMethods:

    def getBuilder(config, data):
        url = data['Request.Host'] + data['Request.Path']
        # Below will return all payloads in a list
        parameters = HttpParameters(config, data)
        print(parameters.payloads)

    def postBuilder(config, data):
        url = data['Request.Host'] + data['Request.Path']


