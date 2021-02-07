import logging

from simple_salesforce import util
from simple_salesforce.exceptions import SalesforceAuthenticationFailed

class LeadClient:
    def __init__(self, sfdc_client):
        self.client = sfdc_client
        self.converted_status = ''

    def get_converted_status(self):
        soql = 'SELECT Id, MasterLabel FROM LeadStatus WHERE IsConverted=true LIMIT 1'

        results = self.client.query_all(soql)['results']

        if results:
            return results[0]['MasterLabel']
        else:
            raise Exception('Converted Status could not be found')

    def convert_leads(self, lead_ids: list, account_id: str, converted_lead_status: str=None,
                     create_opp: bool=False, send_email: bool=False):
        for l_id in lead_ids:
            self.convert_lead(l_id, account_id, converted_lead_status, create_opp, send_email)

    def convert_lead(self, lead_id: str, account_id: str,  converted_lead_status: str=None,
                     create_opp: bool=False, send_email: bool=False):
        sf_instance = self.client.sf_instance
        sf_version = self.client.sf_version
        session_id = self.client.session_id
        session = self.client.session

        if not converted_lead_status and not self.converted_status:
            converted_lead_status = self.converted_status = self.get_converted_status()

        soap_url = f'https://{sf_instance}/services/Soap/u/{sf_version}'

        login_soap_request_headers = {
            'content-type': 'text/xml',
            'charset': 'UTF-8',
            'SOAPAction': 'convertLead'
        }

        login_soap_request_body = f"""
            <soapenv:Envelope
                        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:urn="urn:partner.soap.sforce.com">
              <soapenv:Header>
                 <urn:SessionHeader>
                    <urn:sessionId>{session_id}</urn:sessionId>
                 </urn:SessionHeader>
              </soapenv:Header>
              <soapenv:Body>
                 <urn:convertLead> 
                    <urn:leadConverts> <!-- Zero or more repetitions -->
                       <urn:convertedStatus>{converted_lead_status}</urn:convertedStatus>
                       <urn:leadId>{lead_id}</urn:leadId>
                       <urn:accountId>{account_id}</urn:accountId>
                       <urn:sendNotificationEmail>{send_email}</urn:sendNotificationEmail>
                       <urn:doNotCreateOpportunity>{not create_opp}</urn:doNotCreateOpportunity>
                    </urn:leadConverts>
                 </urn:convertLead>
              </soapenv:Body>
            </soapenv:Envelope>
            """

        response = session.post(
            soap_url, login_soap_request_body, headers=login_soap_request_headers)

        if response.status_code != 200:
            except_code = util.getUniqueElementValueFromXmlString(response.content, 'sf:exceptionCode')
            except_msg = util.getUniqueElementValueFromXmlString(response.content, 'sf:exceptionMessage')
            raise SalesforceAuthenticationFailed(except_code, except_msg)
        else:
            contact_id = util.getUniqueElementValueFromXmlString(response.content, 'contactId')
            success = util.getUniqueElementValueFromXmlString(response.content, 'success')
            status_code = util.getUniqueElementValueFromXmlString(response.content, 'statusCode')

            if success == 'true':
                logging.info(f"Lead Id {lead_id} converted to Contact Id {contact_id}")
                return True, contact_id
            else:
                logging.error(f"Unable to convert Lead Id {lead_id}. Status Code: {status_code}")
                return False, status_code