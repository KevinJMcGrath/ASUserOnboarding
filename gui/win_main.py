import jsonpickle
import PySimpleGUI as sg

from pathlib import Path

import gui.events as events
import gui.field_factory as ff

def load_field_definitions():
    field_def_path = Path('gui/field_definitions.json')

    with open(field_def_path, 'r') as field_def_file:
        field_def_obj_str = field_def_file.read()
        field_def_obj = jsonpickle.decode(field_def_obj_str)

    contact_user_fields = field_def_obj['contact_user_fields']
    contact_setup_fields = field_def_obj['contact_setup_fields']
    activation_template_fields = field_def_obj['activation_template_fields']

    return contact_user_fields, contact_setup_fields, activation_template_fields


def create_output_frame():
    output_layout = [
        [
            sg.Multiline(default_text='', enter_submits=False, autoscroll=True, disabled=True, size=(150, 10),
                         key='txt_output')
        ]
    ]

    return sg.Frame(title='Output', layout=output_layout)

def create_activation_template_tab(activation_template_fields):
    activation_tab_layout = [
        [sg.InputText(default_text='Template Path', size=(20, 1), key='act-template-import'), sg.Button('Import')],
        [sg.Combo(['Trial Template', 'Active User Template'])]
    ]

    field_list = ff.create_template_fields(activation_template_fields)

    activation_tab_layout += field_list

    return sg.Tab(title='1. Activation Template', layout=activation_tab_layout, key='tab_template')

def create_user_list_tab():
    user_tab_layout = [
        [sg.T(text='This is where we add the users', key='tab_user')]
    ]

    return sg.Tab(title='3. Add Users', layout=user_tab_layout)

def create_opp_selection_tab():
    # nb_layout = [[sg.Text('Add a New Business Opp', key='txt_new_business_placeholder')]]
    # re_layout = [[sg.Text('Add a Renewal Opp', key='txt_renewal_placeholder')]]

    nb_layout = [
        [
            sg.Text('', key='lbl_nb_id_0', size=(20, 1)),
            sg.In('', key='txt_nb_name_0', size=(30, 1)),
            sg.Button('-', key='btn_nb_rm_0', disabled=True)
        ],
        [
            sg.Text('', key='lbl_nb_id_1', size=(20, 1)),
            sg.In('', key='txt_nb_name_1', size=(30, 1)),
            sg.Button('-', key='btn_nb_rm_1', disabled=True)
        ],
        [
            sg.Text('', key='lbl_nb_id_2', size=(20, 1)),
            sg.In('', key='txt_nb_name_2', size=(30, 1)),
            sg.Button('-', key='btn_nb_rm_2', disabled=True)
        ]
    ]

    re_layout = [
        [
            sg.Text('', key='lbl_re_id_0', size=(20, 1)),
            sg.In('', key='txt_re_name_0', size=(30, 1)),
            sg.Button('-', key='btn_re_rm_0', disabled=True)
        ],
        [
            sg.Text('', key='lbl_re_id_1', size=(20, 1)),
            sg.In('', key='txt_re_name_1', size=(30, 1)),
            sg.Button('-', key='btn_re_rm_1', disabled=True)
        ],
        [
            sg.Text('', key='lbl_re_id_2', size=(20, 1)),
            sg.In('', key='txt_re_name_2', size=(30, 1)),
            sg.Button('-', key='btn_re_rm_2', disabled=True)
        ]
    ]

    opp_tab_layout = [
        [sg.Text(text='Add New Business and Renewal Opps by Id')],
        [
            sg.In(size=(50,1), key='txt_new_client_opp', do_not_clear=False),
            sg.Button(button_text='Add New Business Opp', key='btn_add_nb')
        ],
        [
            sg.In(size=(50, 1), key='txt_renewal_opp', do_not_clear=False),
            sg.Button(button_text='Add Renewal Opp', key='btn_add_re')
        ],
        [sg.Frame(title='New Business Opportunities', key='frm_new_business', layout=nb_layout)],
        [sg.Frame(title='Renewal Opportunities', key='frm_renewal', layout=re_layout)]
    ]

    return sg.Tab(title='2. Add Opportunities', layout=opp_tab_layout)

def create_window():
    contact_user_fields, contact_setup_fields, activation_template_fields = load_field_definitions()

    tg = sg.TabGroup(
        [
            [
                create_activation_template_tab(activation_template_fields),
                create_opp_selection_tab(),
                create_user_list_tab()
             ]
        ])

    layout_tab = [
        [tg],
        [sg.Button(button_text='Reset All', key='btn_reset_all'),
         sg.Button(button_text='Execute Import', key='btn_import')],
        [create_output_frame()]
    ]

    win_main = sg.Window(title='AS Mass User Onboarding', layout=layout_tab, finalize=True)

    while True:
        try:
            ev, val = win_main.read()

            # window['txt_output'].print(f"Event: {event} | Values: {values}")
            print(f"Event: {ev} | Values: {val}")

            if not ev or ev == 'Exit':
                break
            else:
                events.event_handler(window=win_main, event=ev, values=val)

        except Exception as ex:
            print(ex)

    win_main.close()