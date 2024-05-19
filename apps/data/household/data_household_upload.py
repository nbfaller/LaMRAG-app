# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import hashlib
from datetime import datetime, timedelta
# App definition
from app import app
from apps import dbconnect as db

tag_required = html.Sup("*", className = 'text-danger')
hyperlink_style = {
    'text-decoration' : 'none',
    'color' : 'inherit'
}

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
        dcc.Geolocation(id = 'dat_hou_upl_geoloc'),
        dcc.Store(id = 'dat_hou_upl_sto_rescount', data = 0),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Form(
                            [
                                # Common information
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H1(
                                                    [
                                                        "Upload household profile",
                                                        #html.Small(" (User Registration)", className = 'text-muted')
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        "Kinihanglan pun-on an mga patlang nga may pula nga asterisk ", tag_required, ".",
                                                        html.Br(),
                                                        html.Small(
                                                            ["(Fields with red asterisks ", tag_required, " are required.)"],
                                                            className = 'text-muted'
                                                        )
                                                    ], className = p_m
                                                )
                                            ],
                                            id = 'dat_hou_upl_row_header',
                                            class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Alert(
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        html.I(className = 'bi bi-exclamation-circle-fill me-2'),
                                                                        width = 'auto',
                                                                        class_name = alert_i_m
                                                                    ),
                                                                    dbc.Col(
                                                                        [
                                                                            "Kulang an nabutang nga impormasyon. Alayon pag-hatag san:",
                                                                            html.Br(),
                                                                            html.Small(
                                                                                "(The information supplied is incomplete. Please enter the following:)",
                                                                                className = 'text-muted'
                                                                            ),
                                                                            html.Span(id = 'dat_hou_upl_alert_inputvalidation_span_missing')
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            id = 'dat_hou_upl_alert_inputvalidation',
                                                            is_open = False,
                                                            color = 'warning',
                                                            class_name = label_m,
                                                            dismissable = True,
                                                            #fade = True,
                                                        )
                                                    ]
                                                )
                                            ],
                                            id = 'dat_hou_upl_row_inputvalidation',
                                            class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Barangay", tag_required, #html.Br(),
                                                            #html.Small(" (Event)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_hou_upl_label_brgy_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.Dropdown(
                                                            id = 'dat_hou_upl_input_brgy_id',
                                                            clearable = True,
                                                            disabled = True,
                                                        ),
                                                        dbc.FormText(
                                                            "Kun opisyal ka san barangay, awtomatiko nga pipilion dinhi an imo barangay. (If you are a barangay official, your barangay will be automatically selected.)",
                                                            color = 'secondary',
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                )
                                            ],
                                            id = 'dat_hou_upl_row_brgy_id',
                                            class_name = row_m,
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Purok", tag_required, html.Br(),
                                                            #html.Small(" (Purok)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_hou_upl_label_purok',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            id = 'dat_hou_upl_input_purok',
                                                            type = 'number',
                                                            min = 1,
                                                            invalid = False,
                                                            required = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Alayon pagbutang san numero san purok kun diin ini natabó. (Please input the purok number where this incident occurred.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                ),
                                            ], class_name = row_m,
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Lokasiyon san balay", tag_required,
                                                            html.Br(),
                                                            html.Small(" (Location of home)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_hou_upl_label_loc',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        id = 'dat_hou_upl_input_loc',
                                                                        #disabled = True,
                                                                        #placeholder = "Pili (select)...",
                                                                        #value = 8
                                                                    ),
                                                                    class_name = 'align-self-center col-12 col-md-6 col-lg-8 mb-2 mb-md-0'
                                                                ),
                                                                dbc.Col(
                                                                    dbc.Switch(
                                                                        id = 'dat_hou_upl_input_selectgps',
                                                                        label = html.Span(
                                                                            [
                                                                                "Kuha-a sa GPS. ",
                                                                                html.Small("(Use GPS.)", className = 'text-muted')
                                                                            ]
                                                                        ),
                                                                        value = False,
                                                                        class_name = 'mb-0'
                                                                    ),
                                                                    class_name = 'align-self-center col-12 col-md-6 col-lg-4 mb-2 mb-md-0'
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                )
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Kadamo san mga na-istar", tag_required, html.Br(),
                                                            html.Small(" (Number of household residents)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_hou_upl_label_rescount',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            id = 'dat_hou_upl_input_rescount',
                                                            type = 'number',
                                                            #value = 1,
                                                            min = 1,
                                                            invalid = False,
                                                            required = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Alayon pagbutang san numero san purok kun diin ini natabó. (Please input the purok number where this incident occurred.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                ),
                                            ], class_name = row_m,
                                        ),
                                    ]
                                ),
                                # Household residents
                                html.Div(
                                    [
                                        html.Hr(),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H4(
                                                            [
                                                                html.I(className = 'bi bi-person-fill me-2'),
                                                                "Mga na-istar sini nga balay",
                                                                #html.Br(),
                                                                html.Small(" (Household residents)", className = 'text-muted')
                                                            ]
                                                        ),
                                                    ]
                                                )
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            id = 'dat_hou_upl_row_residents'
                                        ),
                                    ],
                                    id = 'dat_hou_upl_div_residents',
                                    className = div_m + ' d-none',
                                    #style = {'display' : 'none'}
                                ),
                                # Submit button
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Button(
                                                        [
                                                            html.I(className = 'bi bi-cloud-upload-fill me-2'),
                                                            "Submit profile"
                                                        ],
                                                        id = 'dat_hou_upl_btn_submit',
                                                        style = {'width': ' 100%'},
                                                        type = 'submit'
                                                    ),
                                                    class_name = 'align-self-center col-md-3 mb-2'
                                                )
                                            ],
                                            class_name = 'justify-content-end'
                                        )
                                    ],
                                    id = 'dat_hou_upl_div_submit',
                                    className = footer_m + 'd-none'
                                )
                            ]
                        )
                    ],
                    class_name = 'col-lg-10'
                )
            ],
            class_name = 'justify-content-center'
        ),
        dbc.Modal(
            [
                dbc.Form(
                    [
                        dbc.ModalBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4("Confirm profile submission"),
                                                html.P(
                                                    [
                                                        """Alayon pagbutang san imo password para makumpirma an pagsumite sini nga profile.
                                                        Alayon liwat pagseguro nga sakto an ngatanan nga impormasyon nga ginbutang.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """(Please enter your password to confirm the submission of this profile.
                                                            Also, please ensure that all information to be submitted is correct.)
                                                            """,
                                                            className = 'text-muted'
                                                        )
                                                    ], className = p_m
                                                ),
                                            ]
                                        )
                                    ], class_name = 'mb-3'
                                ),
                                #html.Hr(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Alert(
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                html.I(className = 'bi bi-exclamation-circle-fill me-2'),
                                                                width = 'auto',
                                                                class_name = alert_i_m
                                                            ),
                                                            dbc.Col(
                                                                id = 'dat_hou_upl_alert_passwordvalidation_col_text'
                                                            )
                                                        ]
                                                    ),
                                                    id = 'dat_hou_upl_alert_passwordvalidation',
                                                    is_open = False,
                                                    color = 'warning',
                                                    class_name = label_m,
                                                    dismissable = True,
                                                    #fade = True,
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'password',
                                                    id = 'dat_hou_upl_input_password',
                                                    placeholder = ['Enter password'],
                                                    invalid = False
                                                ),
                                            ]
                                        )
                                    ], class_name = row_m
                                ),
                            ],
                            id = 'dat_hou_upl_modal_confirm_body'
                        ),
                        dbc.ModalFooter(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(className = 'bi bi-check-circle-fill me-2'),
                                                    "I-kumpirma (Confirm)"
                                                ],
                                                id = 'dat_hou_upl_btn_confirm',
                                                style = {'width': ' 100%'},
                                                type = 'submit'
                                            ),
                                            class_name = 'align-self-center col-12 col-md-auto'
                                        )
                                    ],
                                    class_name = 'justify-content-end'
                                )
                            ],
                            id = 'dat_hou_upl_modal_confirm_footer'
                        )
                    ]
                )
            ],
            id = 'dat_hou_upl_modal_confirm',
            is_open = False,
            centered = True,
            scrollable = True,
            backdrop = True,
            #size = 'lg',
        ),
    ]
)

dat_hou_upl_pathname = '/data/household/upload'

# Callback for changing number of household residents
@app.callback(
    [
        Output('dat_hou_upl_sto_rescount', 'data')
    ],
    [
        Input('dat_hou_upl_input_rescount', 'value')
    ]
)

def dat_hou_upl_setrescount(count):
    return [count]

# Callback for recording GPS location
@app.callback(
    [
        Output('dat_hou_upl_geoloc', 'update_now'),
    ],
    [
        Input('dat_hou_upl_input_selectgps', 'value'),
    ]
)

def dat_hou_upl_geolocrefresh(selectgps):
    if selectgps: return [True]
    else: return [False]

# Callback for setting the current GPS location
@app.callback(
    [
        Output('dat_hou_upl_input_loc', 'value'),
        Output('dat_hou_upl_input_loc', 'disabled'),
    ],
    [
        Input('dat_hou_upl_input_selectgps', 'value'),
    ],
    [
        State('dat_hou_upl_geoloc', 'position'),
        State('dat_hou_upl_geoloc', 'local_date')
    ],
    prevent_initial_call = True
)

def dat_hou_upl_geolocset(selectgps, pos, date):
    geoloc = None
    disabled = False
    if selectgps and pos:
        lat = pos['lat']
        lon = pos ['lon']
        geoloc = '%s, %s' % (lat, lon)
        disabled = True
    return [geoloc, disabled]

# Callback for populating basic dropdown menus
@app.callback(
    [
        # Dropdowns
        Output('dat_hou_upl_input_brgy_id', 'options'),
        Output('dat_hou_upl_input_brgy_id', 'value'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data'),
    ]
)

def dat_hou_upl_populatedropdowns(pathname, region, province, citymun, brgy):
    if pathname == dat_hou_upl_pathname:
        dropdowns = []

        # Barangays
        sql = """SELECT name as label, id as value
        FROM utilities.addressbrgy
        WHERE region_id = %s AND province_id = %s AND citymun_id = %s;
        """
        values = [region, province, citymun]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        brgys = df.to_dict('records')
        dropdowns.append(brgys)
        dropdowns.append(brgy)

        # Assgined sex
        #sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        #FROM utilities.assignedsex;
        #"""
        #values = []
        #df = db.querydatafromdatabase(sql, values, cols)
        #df = df.sort_values('value')
        #sexes = df.to_dict('records')
        #dropdowns.append(sexes)
        
        return dropdowns
    else: raise PreventUpdate

# Callback for populating form based on number of residents
@app.callback(
    [
        # Residents div
        Output('dat_hou_upl_row_residents', 'children'),
        Output('dat_hou_upl_div_residents', 'className'),
        Output('dat_hou_upl_div_submit', 'className')
    ],
    [
        Input('dat_hou_upl_sto_rescount', 'data'),
    ],
    [
        State('dat_hou_upl_input_brgy_id', 'value'),
        State('dat_hou_upl_input_purok', 'value'),
        State('dat_hou_upl_input_loc', 'value'),
    ],
    prevent_initial_call = True
)

def dat_hou_upl_populatedropdowns(count, brgy, purok, loc):
    to_return = []
    residents_className = 'mt-3 mb-3 d-none'
    submit_className = 'mt-3 d-none'

    # Populating dropdowns
    # Assgined sex
    sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
    FROM utilities.assignedsex;
    """
    values = []
    cols = ['label', 'value']
    df = db.querydatafromdatabase(sql, values, cols)
    df = df.sort_values('value')
    sexes = df.to_dict('records')

    # Populating checklists
    # Sectors
    sql = """SELECT CONCAT(symbol, ';', desc_war, ';', desc_en) AS label, id AS value
    FROM utilities.demographicsector;
    """
    df = db.querydatafromdatabase(sql, values, cols)
    df = df.sort_values('value')
    for i in range (len(df.index)):
        df.at[i, 'label'] = [
            str(df['label'][i]).split(";")[0] + " " + str(df['label'][i]).split(";")[1],
            html.Br(),
            html.Small(
                str(df['label'][i]).split(";")[2],
                className = 'text-muted'
            )
        ]
    sectors = df.to_dict('records')
    # Needs
    sql = """SELECT CONCAT(symbol, ';', desc_war, ';', desc_en) AS label, id AS value
    FROM utilities.demographicneed;
    """
    df = db.querydatafromdatabase(sql, values, cols)
    df = df.sort_values('value')
    for i in range (len(df.index)):
        df.at[i, 'label'] = [
            str(df['label'][i]).split(";")[0] + " " + str(df['label'][i]).split(";")[1],
            html.Br(),
            html.Small(
                str(df['label'][i]).split(";")[2],
                className = 'text-muted'
            )
        ]
    needs = df.to_dict('records')

    # Current date (for maximum date of birth)# Minimum date
    today = datetime.today()

    if count and count >= 1 and (brgy and purok and loc):
        residents_className = 'mt-3 mb-3 d-block',
        submit_className = 'mt-3 d-block',
        for i in range(1, 1 + count):
            resident = [
                dbc.Col(
                    [
                        html.H4(
                            [
                                html.Span("Residente numero ", className = 'd-inline d-lg-none'),
                                #html.Span("No. ", className = 'd-none d-lg-inline'),
                                i
                            ]
                        )
                    ],
                    class_name = 'text-muted text-lg-start col-12 col-lg-1'
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Label(
                                        [
                                            "Ngaran", tag_required, html.Br(),
                                            html.Small(" (Name)", className = 'text-muted')
                                        ],
                                        id = {
                                            'type' : 'dat_hou_upl_label_name',
                                            'index' : i
                                        },
                                        class_name = label_m
                                    ),
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type = 'text',
                                            id = {
                                                'type' : 'dat_hou_upl_input_fname',
                                                'index' : i
                                                },
                                            placeholder = 'Primero (First name)',
                                            invalid = False
                                        )
                                    ],
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type = 'text',
                                            id = {
                                                'type' : 'dat_hou_upl_input_mname',
                                                'index' : i
                                            },
                                            placeholder = 'Butnga (Middle name)',
                                            invalid = False
                                        )
                                    ],
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type = 'text',
                                            id = {
                                                'type' : 'dat_hou_upl_input_lname',
                                                'index' : i
                                            },
                                            placeholder = 'Apelyido (Last name)',
                                            invalid = False
                                        )
                                    ],
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                ),
                            ], class_name = row_m,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Label(
                                        [
                                            "Petsa san pagkatawo", tag_required, html.Br(),
                                            html.Small(" (Date of birth)", className = 'text-muted')
                                        ],
                                        id = {
                                            'type' : 'dat_hou_upl_label_birthdate',
                                            'index' : i
                                        },
                                        class_name = label_m
                                    ),
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                ),
                                dbc.Col(
                                    dcc.DatePickerSingle(
                                        id = {
                                            'type' : 'dat_hou_upl_input_birthdate',
                                            'index' : i
                                        },
                                        placeholder = 'MM/DD/YYYY',
                                        #month_format = 'MMM Do, YYYY',
                                        clearable = True,
                                        #style = {'width' : '100%'}
                                        className = 'w-100',
                                        max_date_allowed = today
                                    ),
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                ),
                                dbc.Col(
                                    dbc.Label(
                                        [
                                            "Natawo nga babayi/lalaki", tag_required, html.Br(),
                                            html.Small(" (Sex assigned at birth)", className = 'text-muted')
                                        ],
                                        id = {
                                            'type' : 'dat_hou_upl_label_assignedsex_id',
                                            'index' : i
                                        },
                                        class_name = label_m
                                    ),
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                ),
                                dbc.Col(
                                    [
                                        #dcc.Dropdown(
                                        dbc.Select(
                                            id = {
                                                'type': 'dat_hou_upl_input_assignedsex_id',
                                                'index' : i
                                            },
                                            options = sexes
                                            #clearable = True
                                        ),
                                        #dbc.FormText(
                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                        #    color = 'secondary',
                                        #    class_name = ftext_m
                                        #),
                                    ],
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                ),
                            ], className = div_m,
                        ),
                        # Affirmative identity
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H5(
                                            [
                                                html.I(className = 'bi bi-rainbow me-2'),
                                                "Apirmatibo nga identidad",
                                                #html.Br(),
                                                html.Small(" (Affirmative identity)", className = 'text-muted')
                                            ]
                                        ),
                                        html.P(
                                            [
                                                """Guin-aaghat ug guinpapanalipdan san Siyudadnon nga Gobyerno an katungod san iya mga
                                                sinasakupan nga magpahayag san ira sexual orientation, gender identity, ug expression (SOGIE).
                                                Guin-aaghat an ngatanan nga maghatag sini nga impormasyon kun sano man ini naangay.""",
                                                html.Br(),
                                                html.Small(
                                                    """(The City Government seeks to promote and protect the ability of its constituents to
                                                    freely express their sexual orientation, gender identity, and expression (SOGIE).
                                                    Everyone is enjoined to fill out these details whenever applicable.)""",
                                                    className = 'text-muted'
                                                )
                                            ], className = p_m
                                        ),
                                    ], class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                "Lived name",
                                                id = {
                                                    'type' : 'dat_hou_upl_label_livedname',
                                                    'index' : i
                                                },
                                                class_name = label_m
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = {
                                                    'type' : 'dat_hou_upl_input_livedname',
                                                    'index' : i
                                                },
                                                placeholder = 'Lived name'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                        )
                                    ], class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Honoripiko",
                                                    html.Br(), html.Small(" (Honorific)", className = 'text-muted')
                                                ],
                                                id = {
                                                    'type' : 'dat_hou_upl_label_honorific',
                                                    'index' : i
                                                },
                                                class_name = label_m
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = {
                                                    'type' : 'dat_hou_upl_input_honorific',
                                                    'index' : i
                                                },
                                                placeholder = 'Example: Mr., Mrs., Ms., Dr.'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Mga pronoun",
                                                    html.Br(), html.Small(" (Pronouns)", className = 'text-muted')
                                                ],
                                                id = {
                                                    'type' : 'dat_hou_upl_label_pronouns',
                                                    'index' : i
                                                },
                                                class_name = label_m
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = {
                                                    'type' : 'dat_hou_upl_input_pronouns',
                                                    'index' : i
                                                },
                                                placeholder = 'Example: she/her, he/him, they/them'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        )
                                    ], class_name = row_m
                                )
                            ], className = div_m
                        ),
                        # Additional information
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H5(
                                                    [
                                                        html.I(className = 'bi bi-person-plus me-2'),
                                                        "Dugang nga impormasiyon",
                                                        #html.Br(),
                                                        html.Small(" (Additional information)", className = 'text-muted')
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        """Guintatalingúha san Siyudadnon nga Gobyerno an paghatag san tangkód
                                                        nga serbisyo sa iya mga sinasakupan. Upod sini an paghatag san espésiyal
                                                        nga atensiyon o pag-atáman sa mga minorya o bulnerable nga sektor san aton
                                                        katilíngban. Tungód sini, guin-aaghat an ngatanan nga mga residente nga magpahibaro kun
                                                        api sira sini nga mga sektor.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """(The city government seeks to deliver equitable services to its constituents.
                                                            This necessitates the provision of specific attention or care to minorities or
                                                            vulnerable sectors of our society. Residents are thus encouraged to identify themselves
                                                            as the following whenever applicable.)""",
                                                            className = 'text-muted'
                                                        )
                                                    ], className = p_m
                                                ),
                                            ]
                                        )
                                    ], class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Checklist(
                                                    options = sectors,
                                                    id = {
                                                        'type' : 'dat_hou_upl_input_demographicsector',
                                                        'index' : i
                                                    },
                                                )
                                            ],
                                            class_name = 'mb-0 col-12 col-md-6'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Checklist(
                                                    options = needs,
                                                    id = {
                                                        'type' : 'dat_hou_upl_input_demographicneed',
                                                        'index' : i
                                                    },
                                                )
                                            ],
                                            class_name = 'mb-0 col-12 col-md-6'
                                        ),
                                    ], class_name = row_m
                                )
                            ]
                        ),
                        html.Hr()
                    ],
                    class_name = 'col-12 col-lg-11'
                )
            ]
            to_return += resident
    return [to_return, residents_className, submit_className]

# Callback for confirming profile creation
@app.callback(
    [
        # Modal
        Output('dat_hou_upl_modal_confirm', 'is_open'),
        # Overall validation alert
        Output('dat_hou_upl_alert_inputvalidation', 'is_open'),
        Output('dat_hou_upl_alert_inputvalidation', 'class_name'),
        Output('dat_hou_upl_alert_inputvalidation_span_missing', 'children'),
    ],
    [
        Input('dat_hou_upl_btn_submit', 'n_clicks')
    ],
    [
        State('dat_hou_upl_sto_rescount', 'data'),
        State({'type' : 'dat_hou_upl_input_fname', 'index' : ALL}, 'value'),
        State({'type' : 'dat_hou_upl_input_lname', 'index' : ALL}, 'value'),
        State({'type' : 'dat_hou_upl_input_birthdate', 'index' : ALL}, 'date'),
        State({'type' : 'dat_hou_upl_input_assignedsex_id', 'index' : ALL}, 'value'),
    ],
    prevent_initial_call = True
)

def dat_hou_upl_confirmcreation(btn, rescount, fnames, lnames, birthdates, assignedsexes):
    #print(fnames, lnames, birthdates, assignedsexes)
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'dat_hou_upl_btn_submit' and btn:
            # Modal
            modal_open = False
            # Overall validation alert
            alert_open = False
            alert_class_name = None
            alert_span = []

            conditions = [
                None in fnames,
                None in lnames,
                None in birthdates,
                len(assignedsexes) < rescount
            ]

            if any(conditions):
                alert_open = True
                alert_class_name = 'mb-3'
                if None in fnames:
                    # Add input validation here
                    alert_span.append(
                        html.Li(
                            [
                                "Mga primero nga ngaran", html.Br(),
                                html.Small(" (First names)", className = 'ms-3 text-muted'),
                            ]
                        )
                    )
                if None in lnames:
                    # Add input validation here
                    alert_span.append(
                        html.Li(
                            [
                                "Mga apelyido", html.Br(),
                                html.Small(" (Last names)", className = 'ms-3 text-muted'),
                            ]
                        )
                    )
                if None in birthdates:
                    # Add input validation here
                    alert_span.append(
                        html.Li(
                            [
                                "Mga petsa san pagkatawo", html.Br(),
                                html.Small(" (Birthdates)", className = 'ms-3 text-muted'),
                            ]
                        )
                    )
                if len(assignedsexes) < rescount:
                    # Add input validation here
                    alert_span.append(
                        html.Li(
                            [
                                "Kun natawo nga babayi/lalaki", html.Br(),
                                html.Small(" (Sexes assigned at birth)", className = 'ms-3 text-muted'),
                            ]
                        )
                    )
            else: modal_open = True
            return [modal_open, alert_open, alert_class_name, alert_span]
        else: raise PreventUpdate
    else: raise PreventUpdate

# Callback for creating new household
@app.callback(
    [
        # In-modal alert
        Output('dat_hou_upl_alert_passwordvalidation', 'is_open'),
        Output('dat_hou_upl_alert_passwordvalidation', 'class_name'),
        Output('dat_hou_upl_alert_passwordvalidation', 'color'),
        Output('dat_hou_upl_alert_passwordvalidation_col_text', 'children'),
        # Input validation
        Output('dat_hou_upl_input_password', 'invalid')
    ],
    [
        Input('dat_hou_upl_btn_confirm', 'n_clicks')
    ],
    [
        # User details
        State('app_currentuser_id', 'data'),
        # Password
        State('dat_hou_upl_input_password', 'value'),
        # App geolock details
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        # Number of residents
        State('dat_hou_upl_sto_rescount', 'data'),
        # Basic information
        State({'type' : 'dat_hou_upl_input_fname', 'index' : ALL}, 'value'),
        State({'type' : 'dat_hou_upl_input_lname', 'index' : ALL}, 'value'),
        State({'type' : 'dat_hou_upl_input_birthdate', 'index' : ALL}, 'date'),
        State({'type' : 'dat_hou_upl_input_assignedsex_id', 'index' : ALL}, 'value'),
        # Affirmative identity
        State({'type' : 'dat_hou_upl_input_livedname', 'index' : ALL}, 'value'),
        State({'type' : 'dat_hou_upl_input_honorific', 'index' : ALL}, 'value'),
        State({'type' : 'dat_hou_upl_input_pronouns', 'index' : ALL}, 'value'),
        # Sectors and needs
        State({'type' : 'dat_hou_upl_input_demographicsector', 'index' : ALL}, 'value'),
        State({'type' : 'dat_hou_upl_input_demographicneed', 'index' : ALL}, 'value'),
    ],
    prevent_initial_call = True
)

def dat_hou_upl_submitcreation(
    btn, user_id, password, region, province, citymun, rescount,
    fnames, lnames, birthdates, assignedsexes,
    livednames, honorifics, pronouns,
    sectors, needs
):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'eve_cre_btn_confirm' and btn:
            # Alert
            alert_open = False
            alert_class_name = None
            alert_color = None
            alert_col_text = None
            # Password validation
            password_invalid = False
            if not(password):
                alert_open = True
                alert_class_name = 'mb-3'
                alert_color = 'warning'
                password_invalid = True
                alert_col_text = [
                    "Alayon pagbutang san imo password.",
                    html.Br(),
                    html.Small(
                        "(Please enter your password.)",
                        className = 'text-muted'
                    ),
                ]
            else:
                sql = """SELECT username FROM users.user
                WHERE id = %s AND password = %s;"""
                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
                values = [user_id, encrypt_string(password)]
                cols = ['username']
                df = db.querydatafromdatabase(sql, values, cols)
                if df.shape[0]:

                    print(fnames, lnames, birthdates, assignedsexes, livednames, honorifics, pronouns, sectors, needs)
                    
                    # Open alert
                    alert_open = True
                    alert_class_name = 'mb-3'
                    alert_color = 'success'
                    password_invalid = False
                    alert_col_text = [
                        "Nasumite na an profile sini nga panimalay.",
                        html.Br(),
                        html.Small(
                            "(Household profile submitted.)",
                            className = 'text-muted'
                        ),
                    ]
                else:
                    alert_open = True
                    alert_class_name = 'mb-3'
                    alert_color = 'warning'
                    password_invalid = True
                    alert_col_text = [
                        "Diri sakto an nabutang nga password.",
                        html.Br(),
                        html.Small(
                            "(Incorrect password.)",
                            className = 'text-muted'
                        ),
                    ]
            return [alert_open, alert_class_name, alert_color, alert_col_text, password_invalid]
        else: raise PreventUpdate
    else: raise PreventUpdate