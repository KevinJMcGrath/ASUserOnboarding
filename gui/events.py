import PySimpleGUI as sg

import sfdc
import gui.eh_opp
import gui.eh_template

def event_handler(window: sg.Window, event, values):
    reset_error_borders(window)

    if event == 'btn_add_nb':
        gui.eh_opp.handle_add_opp_new_business(window=window, values=values)
    elif event == 'btn_add_re':
        gui.eh_opp.handle_add_opp_renewal(window=window, values=values)
    elif event == 'btn_reset_all':
        gui.eh_template.handle_reset_all_fields(window=window, values=values)
    elif event == 'btn_import':
        gui.eh_template.handle_submit_contacts(window=window, values=values)
    else:
        print(f'Unhandled event: {event}')


def reset_error_borders(window: sg.Window):
    for ele in window.element_list():
        if ele.Type == 'input':
            ele.Widget.configure(highlightthickness=0)