import PySimpleGUI as sg

import sfdc
import cache

def handle_add_opp_new_business(window: sg.Window, values):
    ele = window['txt_new_client_opp']
    opp_id = values['txt_new_client_opp']
    if not opp_id:
        text_box_error(element=ele, err_msg='Please specify an Opportunity Id')
    else:
        success, error = cache.imported_data_cache.add_new_biz_opp_id(opp_id=opp_id)

        if not success:
            sg.PopupError(error, keep_on_top=True)
        else:
            add_opp_items_to_new_biz_frame(window=window, opp_id=opp_id)


def handle_add_opp_renewal(window: sg.Window, values):
    ele = window['txt_renewal_opp']
    opp_id = values['txt_renewal_opp']
    if not opp_id:
        text_box_error(element=ele, err_msg='Please specify an Opportunity Id')
    else:
        success, error = cache.imported_data_cache.add_renewal_opp_id(opp_id=opp_id)

        if not success:
            sg.PopupError(error, keep_on_top=True)


def text_box_error(element: sg.Element, err_msg: str):
    sg.PopupError(err_msg, keep_on_top=True)
    element.set_focus()
    element.Widget.configure(highlightcolor='red', highlightthickness=2)

def add_opp_items_to_new_biz_frame(window: sg.Window, opp_id: str):
    frame = window['frm_new_business']
    window['txt_new_business_placeholder'].hide_row()

    o = cache.imported_data_cache.new_biz_opportunities.get(opp_id)
    o_name = o['Name']

    id_ele = sg.Text(text=opp_id, size=(20, 1), key=f'txt_nb_id_{opp_id}')
    name_ele = sg.Text(text=o_name, size=(30, 1), key=f'txt_nb_name_{opp_id}', tooltip=o_name)
    rm_btn_ele = sg.Button(button_text='-', key=f'btn_nb_rm_{opp_id}')

    row = (id_ele, name_ele, rm_btn_ele)



    frame.add_row(row)

