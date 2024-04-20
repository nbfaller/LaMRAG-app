# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# App definition
from app import app
from apps import dbconnect as db

tag_required = html.Sup("*", className = 'text-danger')
hyperlink_style = {
    'text-decoration' : 'none',
    'color' : 'inherit'
}

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
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
                                            ], className = 'mb-0'
                                        )
                                    ],
                                    id = 'eve_cre_row_header'
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
                                                                class_name = 'pe-0 me-0'
                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    """Pahibaro: Kun diri ka empleyado/opisyal san City Disaster Risk Reduction
                                                                    and Management Office (CDRRMO) o san City Mayor's Office (CMO), kinihanglan
                                                                    nira kumpirmahon an paghimo sini nga panhitabó.""",
                                                                    html.Br(),
                                                                    html.Small(
                                                                        """(Please note that events created by users registered under offices apart from
                                                                        the City Disaster Risk Reduction and Management Office (CDRRMO) and City Mayor's
                                                                        Office (CMO) will require their confirmation.)
                                                                        """,
                                                                        className = 'text-muted'
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                    id = 'eve_cre_alert_geolocnotice',
                                                    color = 'info',
                                                    class_name = 'mb-0',
                                                    dismissable = True
                                                )
                                            ]
                                        )
                                    ],
                                    class_name = 'mb-2'
                                )
                            ], className = 'mb-3'
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
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
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
                                                    class_name = 'mt-1'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-2',
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
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
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
                                                    class_name = 'mt-1'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-3',
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
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'eve_cre_input_brgy_id',
                                                    clearable = True,
                                                    multi = True,
                                                ),
                                                dbc.FormText(
                                                    """Alayon pagpili san ngatanan nga mga barangay
                                                    nga naapekto, maaapektuhan, o pwede maapekto.
                                                    (Please select all barangays that were affected,
                                                    have been affected, or may be affected.)""",
                                                    color = 'secondary',
                                                    class_name = 'mt-1'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-2',
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
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
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
                                                    class_name = 'mt-1'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
                                        ),
                                    ], class_name = 'mb-2'
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
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.DatePickerSingle(
                                                    id = 'eve_cre_input_enddate',
                                                    placeholder = 'MM/DD/YYYY',
                                                    #month_format = 'MMM Do, YYYY',
                                                    clearable = True,
                                                    disabled = True,
                                                    #style = {'width' : '100%'}
                                                    className = 'w-100'
                                                ),
                                                dbc.FormText(
                                                    """Alayon pagbilin nga blangko kun usa la ini nga adlaw natabo.
                                                    (Please leave blank if the event only occurs for one day)""",
                                                    color = 'secondary',
                                                    class_name = 'mt-1'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
                                        ),
                                    ], class_name = 'mb-2'
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
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-2',
                                    id = 'rep_cre_row_synopsis'
                                ),
                            ],
                            id = 'eve_cre_div_details',
                            className = 'mt-3 mb-3'
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
                                            class_name = 'pe-0 me-0'
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
                                                ]
                                            )
                                        )
                                    ], class_name = 'mb-2'
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
                                                href = '#'
                                            ),
                                            class_name = 'align-self-center col-md-3 mb-2'
                                        )
                                    ],
                                    class_name = 'justify-content-end'
                                )
                            ],
                            className = 'mt-3'
                        )
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        )
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

def rep_cre_populatedropdowns(pathname, region, province, citymun):
    if pathname == eve_cre_url_pathname:
        dropdowns = []

        # Event types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.eventtype;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        types = df.to_dict('records')
        dropdowns.append(types)

        # Barangays
        region = 8
        province = 60
        citymun = 3
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
        Output('eve_cre_input_enddate', 'disabled'),
        Output('eve_cre_input_enddate', 'min_date_allowed')
    ],
    [
        Input('eve_cre_input_startdate', 'date')
    ]
)

def eve_cre_setminenddate(startdate):
    disabled = True
    min_date = None
    if startdate:
        disabled = False
        min_date = startdate
    return [disabled, min_date]