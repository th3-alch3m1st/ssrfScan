class HttpParameters:

    def process(config, data):
        if data['Request.Query'] == 'null' or data['Request.Body'] == '':
            counter = len(config.parameters) / 5
            for i in counter:
                #par1=url&par2=url&par3=url&par4=url&par5=url
                #par6=url&par7=..



