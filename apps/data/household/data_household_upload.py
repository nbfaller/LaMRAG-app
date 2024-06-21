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
from utilities.utils import MarginSettings, CardStyle, RequiredTag, DropdownDataLoader

layout = html.Div(
    [
        dcc.Geolocation(id = 'dat_hou_upl_geoloc'),
        dcc.Store(id = 'dat_hou_upl_sto_rescount', data = 0),
        dcc.Store(id = 'dat_hou_upl_sto_newhousehold_id', storage_type = 'session'),
        dcc.Store(id = 'dat_hou_upl_sto_newresident_id', storage_type = 'session'),
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
                                                        "Kinihanglan pun-on an mga patlang nga may pula nga asterisk ", RequiredTag.tag, ".",
                                                        html.Br(),
                                                        html.Small(
                                                            ["(Fields with red asterisks ", RequiredTag.tag, " are required.)"],
                                                            className = 'text-muted'
                                                        )
                                                    ], MarginSettings().paragraph
                                                )
                                            ],
                                            id = 'dat_hou_upl_row_header',
                                            class_name = MarginSettings().row
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
                                                                        class_name = MarginSettings().alert_icon 
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
                                                            class_name = MarginSettings().label,
                                                            dismissable = True,
                                                            #fade = True,
                                                        )
                                                    ]
                                                )
                                            ],
                                            id = 'dat_hou_upl_row_inputvalidation',
                                            class_name = MarginSettings().row
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Barangay", RequiredTag.tag, #html.Br(),
                                                            #html.Small(" (Event)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_hou_upl_label_brgy_id',
                                                        class_name = MarginSettings().label
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
                                                            class_name = MarginSettings().form_text
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                )
                                            ],
                                            id = 'dat_hou_upl_row_brgy_id',
                                            class_name = MarginSettings().row,
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Purok", RequiredTag.tag, html.Br(),
                                                            #html.Small(" (Purok)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_hou_upl_label_purok',
                                                        class_name = MarginSettings().label
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
                                                        #    class_name = MarginSettings().form_text
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                ),
                                            ], class_name = MarginSettings().row,
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Lokasiyon san balay", RequiredTag.tag,
                                                            html.Br(),
                                                            html.Small(" (Location of home)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_hou_upl_label_loc',
                                                        class_name = MarginSettings().label
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
                                            ], class_name = MarginSettings().row
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Kadamo san mga na-istar", RequiredTag.tag, html.Br(),
                                                            html.Small(" (Number of household residents)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_hou_upl_label_rescount',
                                                        class_name = MarginSettings().label
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
                                                        #    class_name = MarginSettings().form_text
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                ),
                                            ], class_name = MarginSettings().row,
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
                                            ], class_name = MarginSettings().row
                                        ),
                                        dbc.Row(
                                            id = 'dat_hou_upl_row_residents'
                                        ),
                                    ],
                                    id = 'dat_hou_upl_div_residents',
                                    className = MarginSettings().div + ' d-none',
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
                                    className = MarginSettings().footer + 'd-none'
                                )
                            ]
                        )
                    ],
                    class_name = 'col-md-10'
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
                                                    ], MarginSettings().paragraph
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
                                                                class_name = MarginSettings().alert_icon 
                                                            ),
                                                            dbc.Col(
                                                                id = 'dat_hou_upl_alert_passwordvalidation_col_text'
                                                            )
                                                        ]
                                                    ),
                                                    id = 'dat_hou_upl_alert_passwordvalidation',
                                                    is_open = False,
                                                    color = 'warning',
                                                    class_name = MarginSettings().label,
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
                                    ],
                                    id = 'dat_hou_upl_row_password',
                                    class_name = MarginSettings().row
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
                                                    html.I(className = 'bi bi-arrow-clockwise me-2'),
                                                    "Mag-upload pa (Upload another household)"
                                                ],
                                                id = 'dat_hou_upl_btn_repeat',
                                                style = {'width': ' 100%'},
                                                href = '/data/household/upload',
                                                external_link = True
                                            ),
                                            id = 'dat_hou_upl_col_repeat',
                                            class_name = 'd-none align-self-center col-12 p-0'
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(className = 'bi bi-arrow-return-left me-2'),
                                                    "Balik sa dashboard (Return to dashboard)"
                                                ],
                                                id = 'dat_hou_upl_btn_return',
                                                style = {'width': ' 100%'},
                                                href = '/dashboard',
                                                external_link = True
                                            ),
                                            id = 'dat_hou_upl_col_return',
                                            class_name = 'd-none align-self-center col-12 p-0'
                                        ),
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
                                            id = 'dat_hou_upl_col_confirm',
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
        # New household id
        Output('dat_hou_upl_sto_newhousehold_id', 'data'),
        Output('dat_hou_upl_sto_newresident_id', 'data'),
        # New resident id
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
        ddl = DropdownDataLoader(db)

        # New household id
        newhousehold_id = 1
        sql = """SELECT id FROM data.household ORDER BY id DESC LIMIT 1;"""
        values = []
        cols = ['id']
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0]:
            newhousehold_id = int(df['id'][0]) + 1
        dropdowns.append(newhousehold_id)

        # New resident id
        newresident_id = 1
        sql = """SELECT id FROM data.resident ORDER BY id DESC LIMIT 1;"""
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0]:
            newresident_id = int(df['id'][0]) + 1
        dropdowns.append(newresident_id)

        # Barangays
        brgys = ddl.load_barangays(region, province, citymun)
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
    ddl = DropdownDataLoader(db)

    # Populating dropdowns
    # Assgined sex
    sexes = ddl.load_assignedsexes()

    # Populating checklists
    # Sectors
    sectors = ddl.load_sectors()

    # Needs
    needs = ddl.load_needs()

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
                                            "Ngaran", RequiredTag.tag, html.Br(),
                                            html.Small(" (Name)", className = 'text-muted')
                                        ],
                                        id = {
                                            'type' : 'dat_hou_upl_label_name',
                                            'index' : i
                                        },
                                        class_name = MarginSettings().label
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
                            ], class_name = MarginSettings().row,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Label(
                                        [
                                            "Petsa san pagkatawo", RequiredTag.tag, html.Br(),
                                            html.Small(" (Date of birth)", className = 'text-muted')
                                        ],
                                        id = {
                                            'type' : 'dat_hou_upl_label_birthdate',
                                            'index' : i
                                        },
                                        class_name = MarginSettings().label
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
                                            "Natawo nga babayi/lalaki", RequiredTag.tag, html.Br(),
                                            html.Small(" (Sex assigned at birth)", className = 'text-muted')
                                        ],
                                        id = {
                                            'type' : 'dat_hou_upl_label_assignedsex_id',
                                            'index' : i
                                        },
                                        class_name = MarginSettings().label
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
                                        #    class_name = MarginSettings().form_text
                                        #),
                                    ],
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                ),
                            ], className = MarginSettings().div,
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
                                            ], MarginSettings().paragraph
                                        ),
                                    ], class_name = MarginSettings().row
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
                                                class_name = MarginSettings().label
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
                                    ], class_name = MarginSettings().row
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
                                                class_name = MarginSettings().label
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
                                                class_name = MarginSettings().label
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
                                    ], class_name = MarginSettings().row
                                )
                            ], className = MarginSettings().div
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
                                                    ], MarginSettings().paragraph
                                                ),
                                            ]
                                        )
                                    ], class_name = MarginSettings().row
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
                                    ], class_name = MarginSettings().row
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
        Output('dat_hou_upl_input_password', 'invalid'),
        Output('dat_hou_upl_input_password', 'valid'),
        # Button visibility
        Output('dat_hou_upl_col_repeat', 'class_name'),
        Output('dat_hou_upl_col_return', 'class_name'),
        Output('dat_hou_upl_col_confirm', 'class_name'),
        # Modal dissmisability
        Output('dat_hou_upl_modal_confirm', 'backdrop'),
        # Password field visibility
        Output('dat_hou_upl_row_password', 'class_name')
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
        # Household location
        State('dat_hou_upl_input_brgy_id', 'value'),
        State('dat_hou_upl_input_purok', 'value'),
        State('dat_hou_upl_input_loc', 'value'),
        State('dat_hou_upl_input_selectgps', 'value'),
        State('dat_hou_upl_geoloc', 'position'),
        # Number of residents
        State('dat_hou_upl_sto_rescount', 'data'),
        # Basic information
        State({'type' : 'dat_hou_upl_input_fname', 'index' : ALL}, 'value'),
        State({'type' : 'dat_hou_upl_input_mname', 'index' : ALL}, 'value'),
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
        # New household id
        State('dat_hou_upl_sto_newhousehold_id', 'data'),
        State('dat_hou_upl_sto_newresident_id', 'data'),
    ],
    prevent_initial_call = True
)

def dat_hou_upl_submitcreation(
    btn, user_id, password, region, province, citymun,
    brgy, purok, loc, selectgps, geoloc,
    rescount,
    fnames, mnames, lnames, birthdates, assignedsexes,
    livednames, honorifics, pronouns,
    sectors, needs,
    newhousehold_id, newresident_id
):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'dat_hou_upl_btn_confirm' and btn:
            # Alert
            alert_open = False
            alert_class_name = None
            alert_color = None
            alert_col_text = None
            # Password validation
            password_invalid = False
            password_valid = False
            # Button visibility
            vis_none = 'd-none'
            #vis_inline = 'd-inline'
            vis_block = 'd-block'
            common_class = ' align-self-center col-12 p-0'
            class_repeat = vis_none + common_class
            class_return = vis_none + common_class
            class_confirm = vis_block + common_class + ' col-md-auto'
            # Modal dissmisability
            modal_backdrop = True
            # Password visibility
            class_password = MarginSettings().row + ' ' + vis_block

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
                    loc_gps = None
                    if selectgps and geoloc:
                        loc_gps = "(%s,%s)" % (geoloc['lat'], geoloc['lon'])

                    # Household creation
                    sql = """INSERT INTO data.household(id, region_id, province_id, citymun_id,
                    brgy_id, purok, loc_text, loc_gps, creator_id)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = [newhousehold_id, region, province, citymun, brgy, purok, loc, loc_gps, user_id]
                    db.modifydatabase(sql, values)
                    
                    for i in range(0, rescount):
                        if mnames[i] == None or mnames[i] == '': mnames[i] = ''
                        # Resident creation
                        sql = """INSERT INTO data.resident(id, household_id,
                        fname, mname, lname, birthdate, assignedsex_id,
                        livedname, honorific, pronouns)
                        VALUES(%s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s);"""
                        values = [
                            newresident_id, newhousehold_id,
                            fnames[i], mnames[i], lnames[i], birthdates[i], assignedsexes[i],
                            livednames[i], honorifics[i], pronouns[i]
                        ]
                        db.modifydatabase(sql, values)
                        
                        if sectors[i]:
                            for j in sectors[i]:
                                # Attaching sectors per resident, if any
                                sql = """INSERT INTO data.residentsector(resident_id, sector_id)
                                VALUES(%s, %s);"""
                                values = [newresident_id, j]
                                db.modifydatabase(sql, values)
                        if needs[i]:
                            for j in needs[i]:
                                # Attaching needs per resident, if any
                                sql = """INSERT INTO data.residentneed(resident_id, need_id)
                                VALUES(%s, %s);"""
                                values = [newresident_id, j]
                                db.modifydatabase(sql, values)
                        
                        newresident_id += 1
                    
                    # Open alert
                    alert_open = True
                    alert_class_name = 'mb-3'
                    alert_color = 'success'
                    alert_col_text = [
                        "Nasumite na an profile sini nga panimalay.",
                        html.Br(),
                        html.Small(
                            "(Household profile submitted.)",
                            className = 'text-muted'
                        ),
                    ]
                    password_invalid = False
                    password_valid = True
                    # Button visibility
                    class_repeat = vis_block + common_class + ' mb-2'
                    class_return = vis_block + common_class + ' mt-2'
                    class_confirm = vis_none + common_class
                    # Modal dissmisability
                    modal_backdrop = 'static'
                    # Password visibility
                    class_password = MarginSettings().row + ' ' + vis_none
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
            return [
                alert_open, alert_class_name, alert_color, alert_col_text,
                password_invalid, password_valid,
                class_repeat, class_return, class_confirm,
                modal_backdrop, class_password
            ]
        else: raise PreventUpdate
    else: raise PreventUpdate