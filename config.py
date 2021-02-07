import jsonpickle


with open('./config.json', 'r') as config_file:
    _config = jsonpickle.decode(config_file.read())

Salesforce = _config['salesforce']