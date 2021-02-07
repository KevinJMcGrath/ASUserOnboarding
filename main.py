import csv

from pathlib import Path

import sfdc
import excel

import wx_gui

# from gui import win_main
from sfdc.sobjects.contact import ASContact


def run_main_csv():
    csv_path = Path('./input/JPM-RE-2020-12-29.csv')

    as_contacts = []
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            as_contacts.append(ASContact.from_csv_row(row))

    sfdc.SFDC.Contact.activate_contact_list(as_contacts)


def run_main_xlsx():
    wb_path = Path('./input/FT Partners  - User Upload Template (02-02-2021).xlsx')
    template_values, user_dict, opp_id, opp_role = excel.load_workbook_data(wb_path)

    user_emails = [f"'{u.lower()}'" for u in user_dict.keys()]
    email_str = ','.join(user_emails)

    soql_contact = f'SELECT Id, Email FROM Contact WHERE Email IN ({email_str})'
    sfdc_contacts = sfdc.SFDC.execute_soql_all(soql_contact)

    existing_contact = []
    for c in sfdc_contacts:
        email = c['Email']
        if email in user_emails:
            existing_contact.append(email)
            del user_emails[email]

    soql_lead = f'SELECT Id, Email FROM Lead WHERE IsConverted = false AND Email IN ({email_str})'
    sfdc_leads = sfdc.SFDC.execute_soql_all(soql_lead)

    existing_lead = []
    for l in sfdc_leads:
        email = l['Email']
        if email in user_emails:
            existing_lead.append(email)
            del user_emails[email]

    # Insert remaining Contacts

    # Convert Leads

    # Activate Converted Leads

    # Activate Existing Contacts

if __name__ == '__main__':
    # run_main_xlsx()
    # win_main.create_window()
    wx_gui.AppGui.start_gui()
