from datetime import datetime, timedelta

def get_date_field_default(default_value: str) -> str:
    if default_value == 'TODAY':
        return datetime.today().strftime('%x')
    elif default_value == 'YESTERDAY':
        return (datetime.today() + timedelta(days=-1)).strftime('%x')
    else: ''

def get_checkbox_field_default_vaule(default_value: str):
    return bool(default_value and default_value.lower() in ['yes', 'true', 'checked'])
