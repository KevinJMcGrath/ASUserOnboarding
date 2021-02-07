import logging

from datetime import date, datetime
from pathlib import Path


def convert_datetime_sfdc_datetime_str(dt: datetime):
    return dt.isoformat().split('.')[0] + 'Z'


def convert_date_sfdc_date_str(d: date):
    return d.isoformat()


def convert_sfdc_datetime_str_datetime(sfdc_dt_str: str):
    return datetime.fromisoformat(sfdc_dt_str.split('.')[0])


def convert_sfdc_date_str_date(sfdc_d_str: str):
    return date.fromisoformat(sfdc_d_str)

def handle_dml_response(resp):
    if not resp['success']:
        logging.error(f'Database update failed.')

        for err in resp['errors']:
            logging.error(err)

    return bool(resp['success'])


def handle_dml_response_bulk(operation_file_name: str, resp_list):
    is_success = True
    success_list = []
    error_dict = {}

    for r in resp_list:
        record_id = r['id']
        success = r['success']
        errors = r['errors']

        if success:
            success_list.append(record_id)
        else:
            error_dict[record_id] = errors
            is_success = False

    file_date = datetime.now().isoformat().replace(':', '_').replace('.', '_')
    filename_err = f'{operation_file_name}_errors_{file_date}.csv'
    filename_succ = f'{operation_file_name}_success_{file_date}.csv'

    output_path_err = Path.cwd() / f'output/{filename_err}'
    output_path_succ = Path.cwd() / f'output/{filename_succ}'

    logging.info('Saving success list')
    with open(output_path_succ, 'w', encoding='utf-8') as output_file:
        header = 'contact_id\n'

        output_file.write(header)

        output_file.writelines(success_list)

    logging.info('Saving error list')
    with open(output_path_err, 'w', encoding='utf-8') as output_file:
        header = 'contact_id, error\n'
        output_file.write(header)

        err_output = []
        for cid, err_list in error_dict:
            for err in err_list:
                s = f'{cid},{err}'
                err_output.append(s)

        if err_output:
            output_file.writelines(err_output)





    return is_success