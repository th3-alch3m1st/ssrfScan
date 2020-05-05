class HttpMethods:

    '''
    def __init__(self, config, data):
        self.config = config
        self.data = data
    '''

    def getBuilder(config, data):
        url = data['Request.Host'] + data['Request.Path']
        # Below will return all payloads in a list
        params = HttpParameters.process(config, data)

    def postBuilder(self):
        url = data['Request.Host'] + data['Request.Path']


