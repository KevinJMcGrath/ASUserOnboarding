import logging

from datetime import date, datetime
from simple_salesforce import Salesforce
from typing import List

from sfdc import utility


class ASContact:
    def __init__(self,
                 contact_id: str,
                 opp_id: str,
                 renewal_opp_id: str,
                 username: str,
                 password: str=None,
                 effective_date: date=date.today(),
                 contract_effective_date: date=date.today(),
                 user_status_contract: str='Paying User (Original ID)',
                 user_status_platform: str='Active',
                 prm: str='Global (all)',
                 transcript_type: str='Thomson Reuters',
                 lexis_nexis: bool=True,
                 premium_news: bool=True,
                 brm_type: str='Purchase',
                 brm_pruchase_date: date=date.today(),
                 brm_region: str='Global (all)',
                 opp_contact_role_name: str='Paying User',
                 rewnewal_opp_contact_role_name: str='Paying User',
                 dashboard_access: bool=False,
                 dashboard_auto_alerts: bool=False,
                 mt_news_brief_pro: bool=False):

        self.contact_id = contact_id
        self.opportunity_id = opp_id
        self.renewal_opportunity_id = renewal_opp_id
        self.username = username.lower()
        self.password = password
        self.effective_date = effective_date
        self.effective_date_str = utility.convert_date_sfdc_date_str(effective_date)
        self.contract_effective_date = contract_effective_date
        self.contract_effective_date_str = utility.convert_date_sfdc_date_str(contract_effective_date)
        self.user_status_contract = user_status_contract
        self.user_status_platform = user_status_platform
        self.prm = prm
        self.transcript_type = transcript_type
        self.lexis_nexis = 'On' if lexis_nexis else 'Off'
        self.premium_news = premium_news
        self.brm_type = brm_type
        self.brm_pruchase_date = brm_pruchase_date
        self.brm_pruchase_date_str = utility.convert_date_sfdc_date_str(brm_pruchase_date)
        self.brm_region = brm_region
        self.new_ocr_name = opp_contact_role_name
        self.renewal_ocr_name = rewnewal_opp_contact_role_name
        self.dashboard_access = dashboard_access
        self.dashboard_auto_alerts = dashboard_auto_alerts
        self.mt_news_brief_pro = mt_news_brief_pro


        if not self.password:
            self.password = date.today().strftime('%A%d!!')

    def get_activation_payload(self, exclude_contact_id: bool=False):
        if exclude_contact_id:
            p = get_contact_activation_payload(self)
            del p['Id']
            return p

        return get_contact_activation_payload(self)

    def get_new_client_ocr_payload(self):
        return self.get_ocr_payload(self.opportunity_id, self.new_ocr_name)

    def get_renewal_ocr_payload(self):
        return self.get_ocr_payload(self.opportunity_id, self.renewal_ocr_name)

    def get_ocr_payload(self, opportunity_id: str, role_name: str):
        return {
            "ContactId": self.contact_id,
            "OpportunityId": opportunity_id,
            "Role": role_name
        }

    @staticmethod
    def from_csv_row(row):
        return ASContact(
            contact_id=row['ContactId'],
            opp_id=row['OpportunityId'],
            renewal_opp_id=row['RenewalOppId'],
            username=row['Email'],
            password=row['Password'],
            effective_date=datetime.strptime(row['EffectiveDate'], '%m/%d/%Y').date(),
            contract_effective_date=datetime.strptime(row['ContractEffectiveDate'], '%m/%d/%Y').date(),
            user_status_contract=row['UserStatusContract'],
            user_status_platform=row['UserStatusPlatform'],
            prm=row['PRM'],
            transcript_type=row['TranscriptType'],
            lexis_nexis=bool(row['LexisNexis']),
            premium_news=bool(row['PremiumNews']),
            brm_type=row['BRMType'],
            brm_pruchase_date=datetime.strptime(row['BRMPurchaseDate'], '%m/%d/%Y').date(),
            brm_region=row['BRMRegion'],
            opp_contact_role_name=row['ContactRoleName'],
            rewnewal_opp_contact_role_name=row['RenewContactRoleName'],
            dashboard_access=bool(row['DashboardAccess']),
            dashboard_auto_alerts=bool(row['DashboardAutoAlerts']),
            mt_news_brief_pro=bool(row.get('MTNewsBriefPro', False))
        )


class ContactClient:
    def __init__(self, sfdc_client: Salesforce):
        self.client = sfdc_client

    def activate_contact(self, cnt: ASContact):
        try:
            resp = self.client.Contact.update(cnt.contact_id, cnt.get_activation_payload(exclude_contact_id=True))

            if utility.handle_dml_response(resp):
                utility.handle_dml_response(
                    self.client.OpportunityContactRole.create(cnt.get_new_client_ocr_payload()))

                utility.handle_dml_response(
                    self.client.OpportunityContactRole.create(cnt.get_renewal_ocr_payload()))
        except Exception as ex:
            logging.exception(ex)

    def activate_contact_list(self, cnt_list: List[ASContact]):

        contact_for_update = []
        new_client_ocr_for_insert = []
        renewal_ocr_for_insert = []

        for c in cnt_list:
            contact_for_update.append(c.get_activation_payload())
            new_client_ocr_for_insert.append(c.get_new_client_ocr_payload())
            renewal_ocr_for_insert.append(c.get_renewal_ocr_payload())

        utility.handle_dml_response_bulk('Contact',
            self.client.bulk.Contact.update(contact_for_update))

        utility.handle_dml_response_bulk('New_OCR',
            self.client.bulk.OpportunityContactRole.create(new_client_ocr_for_insert))

        utility.handle_dml_response_bulk('Renew_OCR',
            self.client.bulk.OpportunityContactRole.create(renewal_ocr_for_insert))


def get_contact_activation_payload(c: ASContact):
    return {
        "Id": c.contact_id,
        "Username__c": c.username,
        "Password__c": c.password,
        "Confirm_Password__c": c.password,
        "Effective_Date_paying_user__c": c.effective_date_str,
        "Current_Contract_Effective_Date__c": c.contract_effective_date_str,
        "User_Status__c": c.user_status_contract,
        "Status_of_User__c": c.user_status_platform,
        "Region_s_Subscribed__c": c.prm,
        "Transcripts_Type__c": c.transcript_type,
        "LexisNexis__c": c.lexis_nexis,
        "AS_Premium_News_Content__c": c.premium_news,
        "TR_Request_Type__c": c.brm_type,
        "TR_Service_Start_Date__c": c.brm_pruchase_date_str,
        "Broker_Research_Module__c": c.brm_region,
        "Opportunity__c": c.opportunity_id,
        "Renewal_Opportunity__c": c.renewal_opportunity_id,
        "Feature_Flag_2_AS__c": c.dashboard_access,
        "Dashboard_Auto_Alerts_AS__c": c.dashboard_auto_alerts,
        "MTNewswireLiveBriefPro_AS__c": c.mt_news_brief_pro
    }



