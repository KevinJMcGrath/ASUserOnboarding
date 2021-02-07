import PySimpleGUI as sg

import gui.utility as util

def create_template_fields(field_def_list):
    fields = []

    for field_def in field_def_list:
        f = create_template_field(field_def)

        if f:
            fields.append(f)

    return fields

def create_template_field(field_def):
    field = build_field_def(field_def)

    # I use the * below to break the tuple up in case the field
    # is composed of multiple elements.
    if field:
        field_item = [sg.Text(field_def['label'], size=(25,1)),
            sg.Text(field_def['api_name'], size=(25,1))]

        if isinstance(field, tuple):
            field_item += list(field)
        else:
            field_item.append(field)

        return field_item



def build_field_def(field_def):
    if field_def['type'] == 'text':
        field_key = f"txt_{field_def['api_name']}"
        return sg.In(default_text=field_def['default_value'], size=(30,1), key=field_key)
    elif field_def['type'] == 'date':
        return create_field_date(field_def)
    elif field_def['type'] == 'checkbox':
        return create_field_checkbox(field_def)
    elif field_def['type'] == 'dropdown':
        return create_field_dropdown(field_def)


def create_field_date(field_def):
    date_default = util.get_date_field_default(field_def['default_value'])
    field_key = 'input_' + field_def['api_name']
    return (sg.In(default_text=date_default, size=(20,1), key=field_key),
           sg.CalendarButton(button_text='Choose Date',target=field_key, key='date'))

def create_field_checkbox(field_def):
    field_key = f"chk_{field_def['api_name']}"
    check_default = util.get_checkbox_field_default_vaule(field_def['default_value'])
    return sg.Checkbox(text='', key=field_key, default=check_default)


def create_field_dropdown(field_def):
    field_key = f"ddl_{field_def['api_name']}"
    return sg.Combo(values=field_def['picklist_options'], default_value=field_def['default_value'], key=field_key,
                    size=(35,1))


