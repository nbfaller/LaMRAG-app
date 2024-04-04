# Dash related dependencies
import dash
from dash import dcc, html, dash_table
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
        dcc.Geolocation(id = 'eve_cre_geoloc'),
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
                                                                    "Pahibaro: Kukuhaon san LáMRAG an imo ngaran ug ",
                                                                    html.B(
                                                                        html.A(
                                                                            "puwesto yana sa GPS",
                                                                            id = 'eve_cre_geoloc_loc_war',
                                                                            style = hyperlink_style,
                                                                            target = '_blank'
                                                                        )
                                                                    ),
                                                                    " kaparte sini nga report. Mababaruan mo kun panano ini gingagamit didi.",
                                                                    html.Br(),
                                                                    html.Small(
                                                                        [
                                                                            "(Please note that LáMRAG will record your name and ",
                                                                            html.B(
                                                                                html.A(
                                                                                    "GPS location",
                                                                                    id = 'eve_cre_geoloc_loc_en',
                                                                                    style = hyperlink_style,
                                                                                    target = '_blank'
                                                                                )
                                                                            ),
                                                                            " as part of this report. You can learn how your location is used here.)"
                                                                        ],
                                                                        className = 'text-muted'
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                    id = 'eve_cre_alert_geolocnotice',
                                                    color = 'warning',
                                                    class_name = 'mt-3 mb-0',
                                                    dismissable = True
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
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
                                                    "Klase san nahinabó", tag_required, html.Br(),
                                                    html.Small(" (Event type)", className = 'text-muted')
                                                ],
                                                id = 'eve_cre_label_eventtype_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'eve_cre_input_type_id',
                                                    clearable = True,
                                                    className = 'mb-1'
                                                ),
                                                dbc.FormText(
                                                    """Kinihanglan himuan san maglain nga event an mga panhitabo nga konektado,
                                                    sugad san tsunami dara san linog o storm surge dara san bagyo.
                                                    (Separate events should be created for those caused by others, such as
                                                    tsunamis caused by earthquakes or storm surges caused by typhoons.)""",
                                                    color = 'secondary'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-3',
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
                                                id = 'eve_cre_label_reporttype_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
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
                                                    (Only provide a name if these kinds of events are
                                                    given names, such as typhoons).""",
                                                    color = 'secondary'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-0 col-12 col-md-9'
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
                                                id = 'eve_cre_label_brgy_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'eve_cre_input_brgy_id',
                                                    clearable = True,
                                                    multi = True,
                                                    className = 'mb-1'
                                                ),
                                                dbc.FormText(
                                                    """Alayon pagpili san ngatanan nga mga barangay
                                                    nga naapekto, maaapektuhan, o pwede maapekto.
                                                    (Please select all barangays that were affected,
                                                    have been affected, or may be affected.)""",
                                                    color = 'secondary'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-3',
                                    id = 'eve_cre_row_brgy'
                                ),
                                # Birthdate and sex assigned at birth
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Petsa san panhitabó", tag_required, html.Br(),
                                                    html.Small(" (Date of occurrence)", className = 'text-muted')
                                                ],
                                                id = 'eve_cre_label_date',
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                            #class_name = 'col-md-2 col-sm-11 col-xs-11 mb-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.DatePickerSingle(
                                                    id = 'eve_cre_input_date',
                                                    placeholder = 'MM/DD/YYYY',
                                                    #month_format = 'MMM Do, YYYY',
                                                    clearable = True,
                                                    #style = {'width' : '100%'}
                                                    className = 'w-100'
                                                ),
                                                dbc.FormText(
                                                    """Pwede himuan event an mga panhitabó nga natabó na o matatabó pala.
                                                    (Events that have already occurred or are yet to occur can be created.)""",
                                                    color = 'secondary'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        ),
                                    ], class_name = 'mb-1'
                                )
                            ],
                            id = 'eve_cre_div_details'
                        ),
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)

eve_cre_url_pathname = '/events/create'

# Callback for recording GPS location
@app.callback(
    [
        Output('eve_cre_geoloc', 'update_now'),
    ],
    [
        Input('url', 'pathname'),
    ]
)

def eve_cre_geolocrefresh(pathname):
    if pathname == eve_cre_url_pathname: return [True]
    else: return [False]

# Callback for setting URL links of hyperlinks for GPS location
@app.callback(
    [
        Output('eve_cre_geoloc_loc_war', 'href'),
        Output('eve_cre_geoloc_loc_en', 'href')
    ],
    [
        Input('eve_cre_geoloc', 'position'),
        Input('eve_cre_geoloc', 'local_date')
    ]
)

def eve_cre_geolocrefresh(pos, date):
    href = None
    if pos:
        lat = pos['lat']
        lon = pos ['lon']
        href = 'https://www.google.com/maps/place/%s,%s' % (lat, lon)
    return [href, href]

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