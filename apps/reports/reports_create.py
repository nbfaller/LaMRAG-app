# Dash related dependencies
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# App definition
from app import app
from apps import dbconnect as db

userreg_tag_required = html.Sup("*", className = 'text-danger')
hyperlink_style = {
    'text-decoration' : 'none',
    'color' : 'inherit'
}

layout = html.Div(
    [
        dcc.Geolocation(id = 'rept_cre_geoloc'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H1("File a report"),
                                        html.P(
                                            [
                                                "Kinihanglan pun-on an mga patlang nga may pula nga asterisk ", userreg_tag_required, ".",
                                                html.Br(),
                                                html.Small(
                                                    ["(Fields with red asterisks ", userreg_tag_required, " are required.)"],
                                                    className = 'text-muted'
                                                )
                                            ]
                                        )
                                    ],
                                    id = 'rept_cre_div_header'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Event",
                                                ],
                                                id = 'rept_cre_label_event_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rept_cre_input_event_id',
                                                    clearable = True,
                                                    className = 'mb-1'
                                                ),
                                                dbc.FormText(
                                                    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                    color = 'secondary'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-3',
                                    id = 'rept_cre_div_event'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Report type",
                                                ],
                                                id = 'rept_cre_label_type_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rept_cre_input_type_id',
                                                    clearable = True,
                                                    className = 'mb-1'
                                                ),
                                                dbc.FormText(
                                                    "Usa la nga initial report an puwede himuon. (Initial reports can only be filed once).",
                                                    color = 'secondary'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-3',
                                    id = 'rept_cre_div_reporttype'
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
                                                                            id = 'rept_cre_geoloc_loc_war',
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
                                                                                    id = 'rept_cre_geoloc_loc_en',
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
                                                    id = 'rept_cre_alert_geolocnotice',
                                                    color = 'warning',
                                                    class_name = 'mb-0',
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
                                dbc.Row(
                                    [
                                        html.H4(
                                            [
                                                html.I(className = 'bi bi-journal-text me-2'),
                                                "Synopsis",
                                                #html.Br(),
                                                #html.Small(" (Present address)", className = 'text-muted')
                                            ]
                                        ),
                                        html.P(
                                            [
                                                dbc.Row(
                                                    dbc.Col(
                                                        """Sa pagsusurat san synopsis, maupay batunon ini
                                                        nga mga pakiana kun sano man naangay o posible:"""
                                                    )
                                                ),
                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Small(
                                                            """(In writing the synopsis, you are encouraged
                                                            to answer the following questions whenever applicable or possible)"""
                                                        )
                                                    ), class_name = 'text-muted mb-1'
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.Li(
                                                                    [
                                                                        html.B("Nano"), " an natabo?",
                                                                        html.Small([" (", html.B("What"), " happened?)"], className = 'text-muted')
                                                                    ]
                                                                ),
                                                                html.Li(
                                                                    [
                                                                        html.B("Diin"), " ini natabo?",
                                                                        html.Small([" (", html.B("Where"), " did this happen?)"], className = 'text-muted')
                                                                    ]
                                                                ),
                                                                html.Li(
                                                                    [
                                                                        html.B("Sira sino"), " an naapektuhan?",
                                                                        html.Small([" (", html.B("Who"), " were affected?)"], className = 'text-muted')
                                                                    ]
                                                                ),
                                                            ],
                                                            class_name = 'col-12 col-md-6'
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.Li(
                                                                    [
                                                                        html.B("Kakan-o"), " ini natabo?",
                                                                        html.Small([" (", html.B("When"), " did this happen?)"], className = 'text-muted')
                                                                    ]
                                                                ),
                                                                html.Li(
                                                                    [
                                                                        html.B("Panano"), " ini natabo?",
                                                                        html.Small([" (", html.B("How"), " did this happen?)"], className = 'text-muted')
                                                                    ]
                                                                ),
                                                                html.Li(
                                                                    [
                                                                        html.B("Kay nano"), " ini natabo?",
                                                                        html.Small([" (", html.B("Why"), " did this happen?)"], className = 'text-muted')
                                                                    ]
                                                                ),
                                                            ],
                                                            class_name = 'col-12 col-md-6'
                                                        )
                                                    ],
                                                    class_name = 'mb-1'
                                                ),
                                                dbc.Row(
                                                    dbc.Col(
                                                        """Diri kinihanglan suraton sa synopsis an baton sa mga pakiana
                                                        nga nababaton san iba nga mga parte sini nga report."""
                                                    )
                                                ),
                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Small(
                                                            """(Writing the answers to questions that can be filled out
                                                            in the rest of this report is not necessary.)""",
                                                            className = 'text-muted'
                                                        )
                                                    )
                                                ),
                                            ],
                                        )
                                    ], #class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rept_cre_input_synopsis',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '15em',
                                                        'width' : '100%',
                                                    },
                                                    className = 'mb-1'
                                                )
                                            ],
                                            class_name = 'align-self-center mb-1 col-12'
                                        )
                                    ], class_name = 'mb-3',
                                    id = 'rept_cre_div_synopsis'
                                ),
                            ]
                        )
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)

@app.callback(
    [
        Output('rept_cre_geoloc', 'update_now'),
    ],
    [
        Input('url', 'pathname'),
    ]
)

def rept_cre_geolocrefresh(pathname):
    if pathname == '/reports/create': return [True]
    else: return [False]

@app.callback(
    [
        Output('rept_cre_geoloc_loc_war', 'href'),
        Output('rept_cre_geoloc_loc_en', 'href')
    ],
    [
        Input('rept_cre_geoloc', 'position'),
        Input('rept_cre_geoloc', 'local_date')
    ]
)

def rept_cre_geolocrefresh(pos, date):
    href = None
    if pos:
        lat = pos['lat']
        lon = pos ['lon']
        href = 'https://www.google.com/maps/place/%s,%s' % (lat, lon)
    return [href, href]