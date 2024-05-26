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

tag_required = html.Sup("*", className = 'text-danger')


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
        dcc.Store(id = 'dat_ena_sto_newwindow_id'),
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
                                                html.H1("Activate community profiling"),
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
                                            id = 'dat_ena_row_header',
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
                                                                            html.Span(id = 'dat_ena_alert_inputvalidation_span_missing')
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            id = 'dat_ena_alert_inputvalidation',
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
                                        # Start date
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Petsa san pagtikang", tag_required, html.Br(),
                                                            html.Small(" (Start date)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_ena_label_startdate',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.DatePickerSingle(
                                                            id = 'dat_ena_input_startdate',
                                                            placeholder = 'MM/DD/YYYY',
                                                            #month_format = 'MMM Do, YYYY',
                                                            clearable = True,
                                                            #style = {'width' : '100%'}
                                                            className = 'w-100'
                                                        ),
                                                        #dbc.FormText(
                                                        #    """Kinihanglan himuan san maglain nga event an mga panhitabó nga konektado,
                                                        #    sugad san tsunami dara san linog o storm surge dara san bagyo.
                                                        #    (Separate events should be created for those caused by others, such as
                                                        #    tsunamis caused by earthquakes or storm surges caused by typhoons.)""",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Petsa san pagtapos", tag_required, html.Br(),
                                                            html.Small(" (Deadline/end date)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_ena_label_enddate',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.DatePickerSingle(
                                                            id = 'dat_ena_input_enddate',
                                                            placeholder = 'MM/DD/YYYY',
                                                            #month_format = 'MMM Do, YYYY',
                                                            clearable = True,
                                                            #style = {'width' : '100%'}
                                                            className = 'w-100',
                                                            disabled = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    """Kinihanglan himuan san maglain nga event an mga panhitabó nga konektado,
                                                        #    sugad san tsunami dara san linog o storm surge dara san bagyo.
                                                        #    (Separate events should be created for those caused by others, such as
                                                        #    tsunamis caused by earthquakes or storm surges caused by typhoons.)""",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                )
                                            ], class_name = row_m,
                                            id = 'dat_ena_row_date'
                                        ),
                                        # Participating barangays
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Mga api nga barangay", tag_required, html.Br(),
                                                            html.Small(" (Participating barangays)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_ena_label_brgy_id',
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
                                                                        id = 'dat_ena_input_brgy_id',
                                                                        clearable = True,
                                                                        multi = True,
                                                                    ),
                                                                    class_name = 'align-self-center col-12 col-md-6 col-lg-8 mb-2 mb-md-0'
                                                                ),
                                                                dbc.Col(
                                                                    dbc.Switch(
                                                                        id = 'dat_ena_input_selectallbrgys',
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
                                                            nga aaruan datos sini nga salang san community profiling.
                                                            (Please select all barangays that will participate in
                                                            this community profiling run.)""",
                                                            color = 'secondary',
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                ),
                                            ], class_name = row_m,
                                            id = 'dat_ena_row_brgy'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Mga komento/mensahe sa mga barangay", html.Br(),
                                                            html.Small(" (Remarks/message to barangays)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_ena_label_remarks',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.Textarea(
                                                            id = 'dat_ena_input_remarks',
                                                            #clearable = True,
                                                            wrap = True,
                                                            style = {
                                                                'height' : '15em',
                                                                'width' : '100%',
                                                            },
                                                        ),
                                                        dbc.FormText(
                                                            """Isurat dinhi an mensahe o mga instruksiyon nga angay
                                                            ighatag sa mga barangay sini nga salang san community profiling.
                                                            (Please input the message or instructions that you would
                                                            like to give to the barangays that are participating in this
                                                            community profiling run.)""",
                                                            color = 'secondary',
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                )
                                            ], class_name = row_m,
                                            id = 'dat_ena_row_remarks'
                                        ),
                                    ],
                                    id = 'dat_ena_div_details',
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
                                                            """Sa pag-abri sini nga salang san community profiling, maa-alerto
                                                            an mga barangay nga imo ginpili. Puwede sira maghatag mga profile san
                                                            ira mga sinasakupan nga barangay. Alayon pagseguro nga sakto an mga
                                                            detalye nga ginbutang sa igbaw.
                                                            """, html.Br(),
                                                            html.Small(
                                                                """By enabling this community profiling run, the barangays
                                                                selected will be notified of it. They will be allowed to file
                                                                household profiles under their jurisdiction. Please ensure that
                                                                all details written above are correct.
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
                                                        id = 'dat_ena_btn_submit',
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
                                                html.H4("Confirm community profiling activation"),
                                                html.P(
                                                    [
                                                        """Alayon pagbutang san imo password para makumpirma an pag-aktibar san community profiling.
                                                        Alayon liwat pagseguro nga sakto an ngatanan nga ginbutang nga impormasyon.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """(Please enter your password to confirm community profiling activation.
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
                                                                id = 'dat_ena_alert_passwordvalidation_col_text'
                                                            )
                                                        ]
                                                    ),
                                                    id = 'dat_ena_alert_passwordvalidation',
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
                                                    id = 'dat_ena_input_password',
                                                    placeholder = ['Enter password'],
                                                    invalid = False
                                                ),
                                            ]
                                        )
                                    ],
                                    id = 'dat_ena_row_password',
                                    class_name = row_m
                                ),
                            ],
                            id = 'dat_ena_modal_confirm_body'
                        ),
                        dbc.ModalFooter(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(className = 'bi bi-calendar-range me-2'),
                                                    "Basaha utro an mga detalye (Review details)"
                                                ],
                                                id = 'dat_ena_btn_review',
                                                style = {'width': ' 100%'},
                                                external_link = True
                                            ),
                                            id = 'dat_ena_col_review',
                                            class_name = 'd-none align-self-center col-12 p-0'
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(className = 'bi bi-arrow-return-left me-2'),
                                                    "Balik sa dashboard (Return to dashboard)"
                                                ],
                                                id = 'dat_ena_btn_return',
                                                style = {'width': ' 100%'},
                                                href = '/dashboard',
                                                external_link = True
                                            ),
                                            id = 'dat_ena_col_return',
                                            class_name = 'd-none align-self-center col-12 p-0'
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(className = 'bi bi-check-circle-fill me-2'),
                                                    "I-kumpirma (Confirm)"
                                                ],
                                                id = 'dat_ena_btn_confirm',
                                                style = {'width': ' 100%'},
                                                type = 'submit'
                                            ),
                                            id = 'dat_ena_col_confirm',
                                            class_name = 'align-self-center col-12 col-md-auto'
                                        )
                                    ],
                                    class_name = 'justify-content-end'
                                )
                            ],
                            id = 'dat_ena_modal_confirm_footer'
                        )
                    ]
                )
            ],
            id = 'dat_ena_modal_confirm',
            is_open = False,
            centered = True,
            scrollable = True,
            backdrop = True,
            #size = 'lg',
        ),
    ]
)

dat_ena_url_pathname = '/data/activate'

# Callback for populating basic dropdown menus and other restrictions
@app.callback(
    [
        # New window id
        Output('dat_ena_sto_newwindow_id', 'data'),
        Output('dat_ena_input_brgy_id', 'options'),
        Output('dat_ena_input_startdate', 'min_date_allowed'),
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

def dat_ena_populatedropdowns(pathname, region, province, citymun):
    if pathname == dat_ena_url_pathname:
        dropdowns = []

        # New window id
        window_id = 1
        sql = """SELECT id FROM data.profilingwindow ORDER BY id DESC LIMIT 1;"""
        values = []
        cols = ['id']
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0]:
            window_id = int(df['id'][0]) + 1
        dropdowns.append(window_id)

        # Barangays
        sql = """SELECT name AS label, id AS value
        FROM utilities.addressbrgy WHERE region_id = %s AND province_id = %s AND citymun_id = %s;
        """
        values = [region, province, citymun]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        brgys = df.to_dict('records')
        dropdowns.append(brgys)

        # Minimum date
        dropdowns.append(datetime.today())

        return dropdowns
    else: raise PreventUpdate

# Callback for setting min_date_allowed of end date field
@app.callback(
    [
        Output('dat_ena_input_enddate', 'min_date_allowed'),
        Output('dat_ena_input_enddate', 'disabled')
    ],
    [
        Input('dat_ena_input_startdate', 'date')
    ]
)

def dat_ena_setminenddate(startdate):
    min_date = datetime.today() + timedelta(1) # Date tomorrow
    disabled = True
    if startdate:
        min_date = startdate
        disabled = False
    return [min_date, disabled]

# Callback for disabling barangay selection when "select all" is selected
@app.callback(
    [
        Output('dat_ena_input_brgy_id', 'value'),
        Output('dat_ena_input_brgy_id', 'disabled'),
        Output('dat_ena_input_brgy_id', 'placeholder')
    ],
    [
        Input('dat_ena_input_selectallbrgys', 'value')
    ]
)

def dat_ena_selectallbrgys(switch):
    disabled = False
    placeholder = "Pili (select)..."
    if switch:
        disabled = True
        placeholder = "All barangays selected."
    return [None, disabled, placeholder]

# Callback for confirming community profiling window
@app.callback(
    [
        # Modal
        Output('dat_ena_modal_confirm', 'is_open'),
        # Overall validation alert
        Output('dat_ena_alert_inputvalidation', 'is_open'),
        Output('dat_ena_alert_inputvalidation', 'class_name'),
        Output('dat_ena_alert_inputvalidation_span_missing', 'children'),
        # Button href
        Output('dat_ena_btn_review', 'href')
    ],
    [
        Input('dat_ena_btn_submit', 'n_clicks')
    ],
    [
        State('dat_ena_input_startdate', 'date'),
        State('dat_ena_input_enddate', 'date'),
        State('dat_ena_input_brgy_id', 'value'),
        State('dat_ena_input_selectallbrgys', 'value'),
        State('dat_ena_sto_newwindow_id', 'data')
    ]
)

def dat_ena_confirmcreation(btn, startdate, enddate, brgys, selectallbrgys, newwindow_id):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'dat_ena_btn_submit' and btn:
            # Modal
            modal_open = False
            # Overall validation alert
            alert_open = False
            alert_class_name = None
            alert_span = []
            # Button href
            review_href = '/data/window?id=%s' % newwindow_id

            conditions = [
                not(startdate),
                not(enddate),
                not(brgys or selectallbrgys)
            ]

            if any(conditions):
                alert_open = True
                alert_class_name = 'mb-3'
                if conditions[0]:
                    # Add input validation here
                    alert_span.append(
                        html.Li(
                            [
                                "Petsa san pagtikang", html.Br(),
                                html.Small(" (Start date)", className = 'ms-3 text-muted'),
                            ]
                        )
                    )
                if conditions[1]:
                    # Add input validation here
                    alert_span.append(
                        html.Li(
                            [
                                "Petsa san pagtapos", html.Br(),
                                html.Small(" (End date)", className = 'ms-3 text-muted'),
                            ]
                        )
                    )
                if conditions[2]:
                    # Add input validation here
                    alert_span.append(html.Li(
                        [
                            "Mga api nga barangay", html.Br(),
                            html.Small(" (Participating barangays)", className = 'ms-3 text-muted'),
                        ]
                    ))
            else: modal_open = True
            return [modal_open, alert_open, alert_class_name, alert_span, review_href]
        else: raise PreventUpdate
    else: raise PreventUpdate

# Callback for activating community profiling
@app.callback(
    [
        # In-modal alert
        Output('dat_ena_alert_passwordvalidation', 'is_open'),
        Output('dat_ena_alert_passwordvalidation', 'class_name'),
        Output('dat_ena_alert_passwordvalidation', 'color'),
        Output('dat_ena_alert_passwordvalidation_col_text', 'children'),
        # Input validation
        Output('dat_ena_input_password', 'invalid'),
        Output('dat_ena_input_password', 'valid'),
        # Button visibility
        Output('dat_ena_col_review', 'class_name'),
        Output('dat_ena_col_return', 'class_name'),
        Output('dat_ena_col_confirm', 'class_name'),
        # Modal dissmisability
        Output('dat_ena_modal_confirm', 'backdrop'),
        # Password field visibility
        Output('dat_ena_row_password', 'class_name')
    ],
    [
        Input('dat_ena_btn_confirm', 'n_clicks')
    ],
    [
        # User details
        State('app_currentuser_id', 'data'),
        # Password
        State('dat_ena_input_password', 'value'),
        # App geolock details
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        # Window details
        State('dat_ena_input_startdate', 'date'),
        State('dat_ena_input_enddate', 'date'),
        State('dat_ena_input_brgy_id', 'value'),
        State('dat_ena_input_selectallbrgys', 'value'),
        State('dat_ena_input_remarks', 'value'),
        # New window id
        State('dat_ena_sto_newwindow_id', 'data')
    ],
    prevent_initial_call = True
)

def dat_ena_submitcreation(
    btn, user_id, password,
    region_id, province_id, citymun_id,
    startdate, enddate, brgy_id, selectallbrgys, remarks,
    newwindow_id
):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'dat_ena_btn_confirm' and btn:
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
            class_review = vis_none + common_class
            class_return = vis_none + common_class
            class_confirm = vis_block + common_class + ' col-md-auto'
            # Modal dissmisability
            modal_backdrop = True
            # Password visibility
            class_password = row_m + ' ' + vis_block

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

                    # Actual window creation
                    sql = """INSERT INTO data.profilingwindow(id, startdate, enddate, remarks, creator_id)
                    VALUES(%s, %s, %s, %s, %s);"""
                    values = [newwindow_id, startdate, enddate, remarks, user_id]
                    db.modifydatabase(sql, values)

                    # Add entries to eventbrgy table
                    # AS MUCH AS POSSIBLE avoid loops
                    for brgy in brgy_id:
                        sql = """INSERT INTO data.windowbrgy(window_id, region_id,
                        province_id, citymun_id, brgy_id) VALUES(%s, %s, %s, %s, %s)"""
                        values = [newwindow_id, region_id, province_id, citymun_id, brgy]
                        db.modifydatabase(sql, values)
                    
                    # Open alert
                    alert_open = True
                    alert_class_name = 'mb-3'
                    alert_color = 'success'
                    alert_col_text = [
                        "Na-aktibar na an community profiling.",
                        html.Br(),
                        html.Small(
                            "(Community profiling activated.)",
                            className = 'text-muted'
                        ),
                    ]
                    # Password validity
                    password_invalid = False
                    password_valid = True
                    # Button visibility
                    class_review = vis_block + common_class + ' mb-2'
                    class_return = vis_block + common_class + ' mt-2'
                    class_confirm = vis_none + common_class
                    # Modal dissmisability
                    modal_backdrop = 'static'
                    # Password visibility
                    class_password = row_m + ' ' + vis_none
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
                class_review, class_return, class_confirm,
                modal_backdrop, class_password
            ]
        else: raise PreventUpdate
    else: raise PreventUpdate