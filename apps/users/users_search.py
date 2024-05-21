# FIX THIS ERROR
# When you input permanent address first and add present address later
# details in permanent address fields disappear.

# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import hashlib
from datetime import datetime, timedelta
# App definition
from app import app
from apps import dbconnect as db

usr_reg_tag_required = html.Sup("*", className = 'text-danger')

# Default margins and spacing settings
header_m = 'mb-3'
div_m = 'mt-3 mb-3'
row_m = 'mb-2'
subhead_m = 'mt-3'
p_m = 'mb-0'
label_m = 'mb-0'
ftext_m = 'mt-1'
alert_i_m = 'pe-0 me-0 col-12 col-md-auto mb-2 mb-md-0'
footer_m = 'mt-3'

layout = html.Div(
    [
        dcc.Store(id = 'usr_reg_store_regsuccess', data = False, storage_type = 'session'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Header
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H1(
                                            "Search users",
                                            id = 'usr_src_h1_header'
                                        ),
                                    ],
                                    class_name = row_m,
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Input(
                                                id = 'usr_src_input_user',
                                                type = 'text',
                                                placeholder = "Search by last name, first name, lived name, or middle name"
                                                #value = 1
                                               ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ], className = 'mb-1 mb-md-0',
                                    id = 'usr_src_row_searchuser',
                                    class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Filter by:", #html.Br(),
                                                    #html.Small(" (Year)", className = 'text-muted')
                                                ],
                                                id = 'usr_src_label_filter',
                                                class_name = label_m
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-auto'
                                        ),
                                        dbc.Col(
                                            dbc.DropdownMenu(
                                                dbc.Checklist(
                                                    id = 'usr_src_input_usertype_id',
                                                    #type = 'text',
                                                    #placeholder = "Search by last name, first name, lived name, or middle name"
                                                    #value = 1
                                                ),
                                                id = 'usr_src_dropdown_usertype_id',
                                                color = 'white',
                                                label = 'User type',
                                                #size = 'sm'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-auto'
                                        ),
                                        dbc.Col(
                                            dbc.DropdownMenu(
                                                dbc.Checklist(
                                                    id = 'usr_src_input_office_id',
                                                    #type = 'text',
                                                    #placeholder = "Search by last name, first name, lived name, or middle name"
                                                    #value = 1
                                                ),
                                                id = 'usr_src_dropdown_office_id',
                                                color = 'white',
                                                label = 'Office',
                                                #size = 'sm'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-auto'
                                        ),
                                    ], className = 'mb-1 mb-md-0',
                                    id = 'usr_src_row_filter',
                                    class_name = row_m
                                ),
                            ],
                            id = 'usr_src_div_header',
                            className = header_m
                        ),
                        html.Div(
                            id = 'usr_src_div_results',
                            className = div_m
                        )
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        ),
    ]
)

usr_src_url_pathname = '/users/search'

# Callback for searching users
@app.callback(
    [
        Output('usr_src_div_results', 'children')
    ],
    [
        Input('url', 'pathname'),
        #Input('usr_src_input_user', 'value')
    ]
)

def usr_src_loadsearchresults(pathname):
    if pathname == usr_src_url_pathname:
        sql = """SELECT CONCAT(u.lname, ', ', COALESCE(u.livedname, u.fname), ' ', LEFT(u.mname, 1)) AS Name,
        o.name AS Office,
        u.designation AS Designation,
        ut.label AS usertype
        FROM users.user AS u
        LEFT JOIN utilities.office AS o ON u.office_id = o.id
        LEFT JOIN utilities.usertype AS ut ON u.usertype_id = ut.id
        WHERE u.is_active;
        """
        values = []
        cols = ['Name', 'Office', 'Designation', 'User type']
        df = db.querydatafromdatabase(sql, values, cols)
        table = dbc.Table.from_dataframe(
            df,
            striped = False,
            bordered = False,
            hover = True,
            size = 'sm'
        )

        return [table]
    else: raise PreventUpdate