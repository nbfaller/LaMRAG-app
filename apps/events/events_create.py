# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import hashlib
# App definition
from application import app
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H1("Create an event"),
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
                                            id = 'eve_cre_row_header',
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
                                                                            "Kulang an nabutang nga impormasyon. Alayon pag-hatag san",
                                                                            html.Br(),
                                                                            html.Small(
                                                                                "(The information supplied is incomplete. Please enter the following):",
                                                                                className = 'text-muted'
                                                                            ),
                                                                            html.Span(id = 'eve_cre_alert_inputvalidation_span_missing')
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            id = 'eve_cre_alert_inputvalidation',
                                                            is_open = False,
                                                            color = 'warning',
                                                            class_name = label_m,
                                                            dismissable = True
                                                        )
                                                    ]
                                                )
                                            ],
                                            #class_name = row_m
                                        )
                                    ], className = header_m
                                ),
                                html.Hr(),
                                html.Div(
                                    [
                                        # Event type
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Klase san panhitabó", tag_required, html.Br(),
                                                            html.Small(" (Event type)", className = 'text-muted')
                                                        ],
                                                        id = 'eve_cre_label_eventtype_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.Dropdown(
                                                            id = 'eve_cre_input_type_id',
                                                            clearable = True,
                                                        ),
                                                        dbc.FormText(
                                                            """Kinihanglan himuan san maglain nga event an mga panhitabó nga konektado,
                                                            sugad san tsunami dara san linog o storm surge dara san bagyo.
                                                            (Separate events should be created for those caused by others, such as
                                                            tsunamis caused by earthquakes or storm surges caused by typhoons.)""",
                                                            color = 'secondary',
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                )
                                            ], class_name = row_m,
                                            id = 'eve_cre_row_event'
                                        ),
                                        # Event name
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Ngaran san panhitabó, kun posible", html.Br(),
                                                            html.Small(" (Event name, if possible)", className = 'text-muted')
                                                        ],
                                                        id = 'eve_cre_label_reporttype_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            type = 'text',
                                                            id = 'eve_cre_input_name',
                                                            placeholder = 'Ngaran san panhitabó (Event name)'
                                                        ),
                                                        dbc.FormText(
                                                            """Paghatag la ngaran kun gin-ngangaranan ini nga
                                                            mga klase san panhitabó, sugad san mga bagyo.
                                                            Puwede dinhi klaruhon an klase san panhitabó kun "Iba pa"
                                                            an imo ginpili sa una nga patlang.
                                                            (Only provide a name if these kinds of events are
                                                            given names, such as typhoons. You can specify the
                                                            type of event here if you chose "Others" in the menu
                                                            above.)""",
                                                            color = 'secondary',
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                )
                                            ], class_name = row_m,
                                            id = 'eve_cre_row_name'
                                        ),
                                        # Affected barangays
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Mga apektado nga barangay", tag_required, html.Br(),
                                                            html.Small(" (Affected barangays)", className = 'text-muted')
                                                        ],
                                                        id = 'eve_cre_label_brgy_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    dcc.Dropdown(
                                                                        id = 'eve_cre_input_brgy_id',
                                                                        clearable = True,
                                                                        multi = True,
                                                                    ),
                                                                    class_name = 'align-self-center col-12 col-md-6 col-lg-8 mb-2 mb-md-0'
                                                                ),
                                                                dbc.Col(
                                                                    dbc.Switch(
                                                                        id = 'eve_cre_input_selectallbrgys',
                                                                        label = html.Span(
                                                                            [
                                                                                "Pili-a ngatanan. ",
                                                                                html.Small("(Select all.)", className = 'text-muted')
                                                                            ]
                                                                        ),
                                                                        value = False,
                                                                        class_name = 'mb-0'
                                                                    ),
                                                                    class_name = 'align-self-center col-12 col-md-6 col-lg-4 mb-2 mb-md-0'
                                                                )
                                                            ]
                                                        ),
                                                        dbc.FormText(
                                                            """Alayon pagpili san ngatanan nga mga barangay
                                                            nga naapekto, maaapektuhan, o pwede maapekto.
                                                            (Please select all barangays that were affected,
                                                            have been affected, or may be affected.)""",
                                                            color = 'secondary',
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                ),
                                            ], class_name = row_m,
                                            id = 'eve_cre_row_brgy'
                                        ),
                                        # Start date
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Petsa san panhitabó", tag_required, html.Br(),
                                                            html.Small(" (Date of occurrence)", className = 'text-muted')
                                                        ],
                                                        id = 'eve_cre_label_startdate',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.DatePickerSingle(
                                                            id = 'eve_cre_input_startdate',
                                                            placeholder = 'MM/DD/YYYY',
                                                            #month_format = 'MMM Do, YYYY',
                                                            clearable = True,
                                                            #style = {'width' : '100%'}
                                                            className = 'w-100'
                                                        ),
                                                        dbc.FormText(
                                                            """Pwede himuan event an mga panhitabó nga natabó na o matatabó pala.
                                                            (Events that have already occurred or are yet to occur can be created.)""",
                                                            color = 'secondary',
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                ),
                                            ], class_name = row_m
                                        ),
                                        # Date of occurrence
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Petsa san pagtapos", html.Br(),
                                                            html.Small(" (End date)", className = 'text-muted')
                                                        ],
                                                        id = 'eve_cre_label_enddate',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.DatePickerSingle(
                                                            id = 'eve_cre_input_enddate',
                                                            placeholder = 'MM/DD/YYYY',
                                                            #month_format = 'MMM Do, YYYY',
                                                            clearable = True,
                                                            #disabled = True,
                                                            #style = {'width' : '100%'}
                                                            className = 'w-100'
                                                        ),
                                                        dbc.FormText(
                                                            """Alayon pagbilin nga blangko kun usa la ini nga adlaw natabo.
                                                            (Please leave blank if the event only occurs for one day)""",
                                                            color = 'secondary',
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                ),
                                            ],
                                            id = 'eve_cre_row_enddate',
                                            class_name = row_m
                                        ),
                                        # Event escription
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Deskripsiyon", html.Br(),
                                                            html.Small(" (Description)", className = 'text-muted')
                                                        ],
                                                        id = 'eve_cre_label_description',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.Textarea(
                                                            id = 'eve_cre_input_description',
                                                            #clearable = True,
                                                            wrap = True,
                                                            style = {
                                                                'height' : '15em',
                                                                'width' : '100%',
                                                            },
                                                        )
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                )
                                            ], class_name = row_m,
                                            id = 'eve_cre_row_synopsis'
                                        ),
                                    ],
                                    id = 'eve_cre_div_details',
                                    className = div_m
                                ),
                                html.Hr(),
                                # Create button
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.I(className = 'bi bi-exclamation-square-fill me-2'),
                                                    width = 'auto',
                                                    class_name = alert_i_m
                                                ),
                                                dbc.Col(
                                                    html.P(
                                                        [
                                                            html.H5(
                                                                [
                                                                    "Pahibaro ",
                                                                    html.Small(" (Notice)", className = 'text-muted'),
                                                                    ":"
                                                                ]
                                                            ),
                                                            """Sa paghimo sini nga event, maa-alerto an mga barangay nga
                                                            imo ginpili. Puwede sira maghatag report ug puwede sira aruan
                                                            report. Alayon pagseguro nga sakto an mga detalye sini nga event
                                                            ug nakonpórme ini sa mga pahibaro san NDRRMC, OCD, PAGASA,
                                                            PHIVOLCS, ug iba nga mga nasudnon nga ahensiya.
                                                            """, html.Br(),
                                                            html.Small(
                                                                """(By creating this event, the barangays selected will
                                                                be alerted of it. They will be allowed to file reports;
                                                                likewise, you will be allowed to request reports from them.
                                                                Please ensure that all details are correct and conform to the
                                                                advisories published by the NDRRMC, OCD, PAGASA, PHIVOLCS,
                                                                and other relevant national government agencies.)
                                                                """,
                                                                className = 'text-muted'
                                                            )
                                                        ], className = p_m
                                                    )
                                                )
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Button(
                                                        [
                                                            html.I(className = 'bi bi-plus-circle-fill me-2'),
                                                            "Himo (Create)"
                                                        ],
                                                        id = 'eve_cre_btn_submit',
                                                        style = {'width': ' 100%'},
                                                        type = 'submit'
                                                    ),
                                                    class_name = 'align-self-center col-md-3 mb-2'
                                                )
                                            ],
                                            class_name = 'justify-content-end'
                                        )
                                    ],
                                    className = footer_m
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
                                                html.H4("Confirm event creation"),
                                                html.P(
                                                    [
                                                        """Alayon pagbutang san imo password para makumpirma an paghimo sini nga panhitabó.
                                                        Alayon liwat pagseguro nga sakto an ngatanan nga impormasyon nga imo ginhatag.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """(Please enter your password to confirm the creation of this event.
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
                                                                id = 'eve_cre_alert_passwordvalidation_col_text'
                                                            )
                                                        ]
                                                    ),
                                                    id = 'eve_cre_alert_passwordvalidation',
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
                                                    id = 'eve_cre_input_password',
                                                    placeholder = ['Enter password'],
                                                    invalid = False
                                                ),
                                            ]
                                        )
                                    ], class_name = row_m
                                ),
                            ],
                            id = 'eve_cre_modal_confirm_body'
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
                                                id = 'eve_cre_btn_confirm',
                                                style = {'width': ' 100%'},
                                                type = 'submit'
                                            ),
                                            class_name = 'align-self-center col-12 col-md-auto'
                                        )
                                    ],
                                    class_name = 'justify-content-end'
                                )
                            ],
                            id = 'eve_cre_modal_confirm_footer'
                        )
                    ]
                )
            ],
            id = 'eve_cre_modal_confirm',
            is_open = False,
            centered = True,
            scrollable = True,
            backdrop = True,
            #size = 'lg',
        ),
    ]
)

eve_cre_url_pathname = '/events/create'

# Callback for populating basic dropdown menus
@app.callback(
    [
        Output('eve_cre_input_type_id', 'options'),
        Output('eve_cre_input_brgy_id', 'options'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data')
    ]
)

def eve_cre_populatedropdowns(pathname, region, province, citymun):
    if pathname == eve_cre_url_pathname:
        dropdowns = []

        # Event types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.eventtype
        ORDER BY id ASC;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        types = df.to_dict('records')
        dropdowns.append(types)

        # Barangays
        sql = """SELECT name AS label, id AS value
        FROM utilities.addressbrgy WHERE region_id = %s AND province_id = %s AND citymun_id = %s;
        """
        values = [region, province, citymun]
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        brgys = df.to_dict('records')
        dropdowns.append(brgys)

        return dropdowns
    else: raise PreventUpdate

# Callback for setting min_date_allowed end date field
@app.callback(
    [
        Output('eve_cre_row_enddate', 'class_name'),
        Output('eve_cre_input_enddate', 'min_date_allowed')
    ],
    [
        Input('eve_cre_input_startdate', 'date')
    ]
)

def eve_cre_setminenddate(startdate):
    retclass = 'mb-2 d-none'
    min_date = None
    if startdate:
        retclass = 'mb-2'
        min_date = startdate
    return [retclass, min_date]

# Callback for disabling barangay selection when "select all" is selected
@app.callback(
    [
        Output('eve_cre_input_brgy_id', 'value'),
        Output('eve_cre_input_brgy_id', 'disabled')
    ],
    [
        Input('eve_cre_input_selectallbrgys', 'value')
    ]
)

def eve_cre_selectallbrgys(switch):
    disabled = False
    if switch: disabled = True
    return [None, disabled]

# Callback for confirming event creation
@app.callback(
    [
        # Modal
        Output('eve_cre_modal_confirm', 'is_open'),
        # Overall validation alert
        Output('eve_cre_alert_inputvalidation', 'is_open'),
        Output('eve_cre_alert_inputvalidation', 'class_name'),
        Output('eve_cre_alert_inputvalidation_span_missing', 'children'),
    ],
    [
        Input('eve_cre_btn_submit', 'n_clicks')
    ],
    [
        State('eve_cre_input_type_id', 'value'),
        State('eve_cre_input_brgy_id', 'value'),
        State('eve_cre_input_selectallbrgys', 'value'),
        State('eve_cre_input_startdate', 'date'),
    ]
)

def eve_cre_confirmcreation(btn, type_id, brgy, selectallbrgys, startdate):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'eve_cre_btn_submit' and btn:
            # Modal
            modal_open = False
            # Overall validation alert
            alert_open = False
            alert_class_name = None
            alert_span = []

            if (not(type_id) or not(brgy or selectallbrgys) or not(startdate)):
                alert_open = True
                alert_class_name = 'mb-3'
                if not(type_id):
                    # Add input validation here
                    alert_span.append(html.Li(
                        [
                            "Klase san panhitabó", html.Br(),
                            html.Small(" (Event type)", className = 'ms-3 text-muted'),
                        ]
                    ))
                if not(brgy or selectallbrgys):
                    # Add input validation here
                    alert_span.append(html.Li(
                        [
                            "Mga apektado nga barangay", html.Br(),
                            html.Small(" (Affected barangays)", className = 'ms-3 text-muted'),
                        ]
                    ))
                if not(startdate):
                    # Add input validation here
                    alert_span.append(html.Li(
                        [
                            "Petsa san panhitabó", html.Br(),
                            html.Small(" (Date of occurrence)", className = 'ms-3 text-muted'),
                        ]
                    ))
            else: modal_open = True
            return [modal_open, alert_open, alert_class_name, alert_span]
        else: raise PreventUpdate
    else: raise PreventUpdate

# Callback for creating new event
@app.callback(
    [
        # In-modal alert
        Output('eve_cre_alert_passwordvalidation', 'is_open'),
        Output('eve_cre_alert_passwordvalidation', 'class_name'),
        Output('eve_cre_alert_passwordvalidation', 'color'),
        Output('eve_cre_alert_passwordvalidation_col_text', 'children'),
        # Input validation
        Output('eve_cre_input_password', 'invalid')
    ],
    [
        Input('eve_cre_btn_confirm', 'n_clicks')
    ],
    [
        # Password
        State('eve_cre_input_password', 'value'),
        # Event details
        State('eve_cre_input_type_id', 'value'),
        State('eve_cre_input_name', 'value'),
        State('eve_cre_input_brgy_id', 'value'),
        State('eve_cre_input_selectallbrgys', 'value'),
        State('eve_cre_input_startdate', 'date'),
        State('eve_cre_input_enddate', 'date'),
        State('eve_cre_input_description', 'value'),
        # User details
        State('app_currentuser_id', 'data'),
        # App geolock details
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
    ],
    prevent_initial_call = True
)

def eve_cre_submitcreation(
    btn, password,
    type_id, name, brgy_id, selectallbrgys,
    startdate, enddate, description,
    user_id, region_id, province_id, citymun_id
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
                    # Retrieves all barangays if "select all barangays" is selected
                    if selectallbrgys:
                        sql = """SELECT id FROM utilities.addressbrgy
                        WHERE region_id = %s AND province_id = %s AND citymun_id = %s;"""
                        values = [region_id, province_id, citymun_id]
                        cols = ['id']
                        brgy_id = db.querydatafromdatabase(sql, values, cols)['id'].to_list()

                    # Actual event creation
                    sql = """INSERT INTO events.event(type_id, name, startdate,
                    enddate, description, creator_id) VALUES(%s, %s,
                    %s, %s, %s, %s)"""
                    values = [type_id, name, startdate, enddate, description, user_id]
                    db.modifydatabase(sql, values)

                    # Get index of latest event
                    sql = """SELECT id FROM events.event ORDER BY id DESC LIMIT 1;"""
                    values = []
                    cols = ['id']
                    event_id = int(db.querydatafromdatabase(sql, values, cols)['id'][0])

                    # Add entries to eventbrgy table
                    # AS MUCH AS POSSIBLE avoid loops
                    for brgy in brgy_id:
                        sql = """INSERT INTO events.eventbrgy(event_id, region_id,
                        province_id, citymun_id, brgy_id) VALUES(%s, %s, %s, %s, %s)"""
                        values = [event_id, region_id, province_id, citymun_id, brgy]
                        db.modifydatabase(sql, values)
                    
                    # Open alert
                    alert_open = True
                    alert_class_name = 'mb-3'
                    alert_color = 'success'
                    password_invalid = False
                    alert_col_text = [
                        "Nahimo na an event.",
                        html.Br(),
                        html.Small(
                            "(Event created.)",
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