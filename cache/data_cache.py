from sfdc import SFDC

class ImportData:
    def __init__(self):
        self.imported_users_raw = []
        self.leads_for_conversion = []
        self.contacts_for_insert = []
        self.contacts_for_update = []
        self.new_biz_opp_ids = set()
        self.renewal_opp_ids = set()
        self.new_biz_opportunities = {}
        self.renewal_opportunities = {}

    def add_new_biz_opp_id(self, opp_id: str):
        o = load_opp_from_sfdc(opp_id)

        if o:
            self.new_biz_opp_ids.add(opp_id)
            self.new_biz_opportunities[opp_id] = o
            return True, None

        return False, f'Opportunity with Id {opp_id} was not found in Salesforce.'

    def add_renewal_opp_id(self, opp_id: str):
        o = load_opp_from_sfdc(opp_id)

        if o:
            self.renewal_opp_ids.add(opp_id)
            self.renewal_opportunities[opp_id] = o
            return True, None

        return False, f'Opportunity with Id {opp_id} was not found in Salesforce.'



def load_opp_from_sfdc(opp_id: str):
    soql = f"SELECT Id, Name FROM Opportunity WHERE Id = '{opp_id}'"

    opps = SFDC.execute_soql_all(soql_query=soql)

    if opps:
        return opps[0]