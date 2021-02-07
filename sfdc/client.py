from simple_salesforce import Salesforce

import config

import sfdc.sobjects as so

class SalesforceClient:
    def __init__(self):
        self.username = config.Salesforce['username']
        self.password = config.Salesforce['password']
        self.security_token = config.Salesforce['security_token']
        self.domain = get_domain()

        self.client = Salesforce(username=self.username, password=self.password, security_token=self.security_token,
                                 domain=self.domain)

        self.Lead = so.lead.LeadClient(self.client)
        self.Contact = so.contact.ContactClient(self.client)


    def execute_soql_all(self, soql_query: str, include_deleted: bool=False):
        return self.client.query_all(query=soql_query, include_deleted=include_deleted)['records']

def get_domain():
    if 'is_sandbox' in config.Salesforce and config.Salesforce['is_sandbox']:
        return 'test'
    else:
        return 'login'

def get_client_from_config():
    return SalesforceClient()