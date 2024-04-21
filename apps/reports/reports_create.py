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
        dcc.Geolocation(id = 'rep_cre_geoloc'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Common information
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H1("File a report"),
                                        html.P(
                                            [
                                                "Kinihanglan pun-on an mga patlang nga may pula nga asterisk ", tag_required, ".",
                                                html.Br(),
                                                html.Small(
                                                    ["(Fields with red asterisks ", tag_required, " are required.)"],
                                                    className = 'text-muted'
                                                )
                                            ]
                                        )
                                    ],
                                    id = 'rep_cre_row_header',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Panhitabó", tag_required, html.Br(),
                                                    html.Small(" (Event)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_event_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_event_id',
                                                    clearable = True,
                                                ),
                                                dbc.FormText(
                                                    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                    color = 'secondary',
                                                    class_name = 'mt-1'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ],
                                    id = 'rep_cre_row_event',
                                    class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Klase san report", tag_required, html.Br(),
                                                    html.Small(" (Report type)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_reporttype_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_reporttype_id',
                                                    clearable = True,
                                                ),
                                                dbc.FormText(
                                                    "Usa la nga initial report an puwede himuon. (Initial reports can only be filed once.)",
                                                    color = 'secondary',
                                                    class_name = 'mt-1'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ],
                                    id = 'rep_cre_row_reporttype',
                                    class_name = 'mb-2'
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
                                                                            id = 'rep_cre_geoloc_loc_war',
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
                                                                                    id = 'rep_cre_geoloc_loc_en',
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
                                                    id = 'rep_cre_alert_geolocnotice',
                                                    color = 'info',
                                                    class_name = 'mb-0',
                                                    dismissable = True
                                                )
                                            ]
                                        )
                                    ],
                                    class_name = 'mb-2'
                                )
                            ],
                            id = 'rep_cre_div_basicdetails',
                            className = 'mb-3'
                        ),
                        html.Hr(),
                        # Related incidents
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-exclamation-triangle-fill me-2'),
                                                        "Insidente",
                                                        #html.Br(),
                                                        html.Small(" (Related incident)", className = 'text-muted')
                                                    ]
                                                ),
                                                #html.P(
                                                #    [
                                                #        "Pinduta la an plus button", html.I(className = 'bi bi-plus-square ms-2 me-2'), "kun kinihanglan mo mag-report san damo nga insidente.",
                                                #        html.Br(),
                                                #        html.Small(
                                                #            ["(Click on the plus button", html.I(className = 'bi bi-plus-square ms-2 me-2'), "if you want to report multiple related incidents.)"],
                                                #            className = 'text-muted'
                                                #        )
                                                #    ]
                                                #)
                                            ]
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Klase san insidente", tag_required, html.Br(),
                                                    html.Small(" (Type of incident)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Select(
                                                #dcc.Dropdown(
                                                    id = 'rep_cre_input_relinctype_id',
                                                    #clearable = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-4'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Kantidad san insidente", tag_required, html.Br(),
                                                    html.Small(" (Quantity of incident)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_qty',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    id = 'rep_cre_input_relinc_qty',
                                                    type = 'number',
                                                    value = 1,
                                                    min = 1,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-2'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Purok san insidente", tag_required, html.Br(),
                                                    html.Small(" (Purok of occurrence)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_purok',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    id = 'rep_cre_input_relinc_purok',
                                                    type = 'number',
                                                    min = '1',
                                                    invalid = False,
                                                ),
                                                #dbc.FormText(
                                                #    "Alayon pagbutang san numero san purok kun diin ini natabó. (Please input the purok number where this incident occurred.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-3'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Petsa san insidente", tag_required, html.Br(),
                                                    html.Small(" (Date of occurrence)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_date',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-2'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.DatePickerSingle(
                                                    id = 'rep_cre_input_relinc_date',
                                                    placeholder = 'MM/DD/YYYY',
                                                    #month_format = 'MMM Do, YYYY',
                                                    clearable = True,
                                                    #style = {'width' : '100%'}
                                                    className = 'w-100'
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-4'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Oras san insidente", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (Time of occurrence)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_time',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.InputGroup(
                                                    [
                                                        dbc.Input(
                                                            id = 'rep_cre_input_relinc_time_hh',
                                                            placeholder = 'HH',
                                                            type = 'number',
                                                            min = 1,
                                                            max = 12,
                                                            invalid = False
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            id = 'rep_cre_input_relinc_time_mm',
                                                            placeholder = 'MM',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            id = 'rep_cre_input_relinc_time_ss',
                                                            placeholder = 'SS',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False
                                                        ),
                                                        dbc.Select(
                                                            id = 'rep_cre_input_relinc_time_ampm',
                                                            placeholder = 'AM/PM',
                                                            options = ['AM', 'PM']
                                                        )
                                                    ]
                                                ),
                                                #dbc.FormText(
                                                #    """Awtomátikó nga ginkukuha san LáMRAG an oras yana komo oras san panhitabó. Alayon pagbalyo sini kun sa iba nga oras nahitabó an imo ginhihimuan report.
                                                #    (LáMRAG automatically sets the current time as the time of occurrence. Please change this if the event you are reporting occurred at a different time.)""",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Deskripsiyon", html.Br(),
                                                    html.Small(" (Description)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_desc',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_relinc_desc',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '5em',
                                                        'width' : '100%',
                                                    },
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Mga ginhimo pagkatapos", html.Br(),
                                                    html.Small(" (Actions taken)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_actions',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_relinc_actions',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '5em',
                                                        'width' : '100%',
                                                    },
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Iba pa nga komento", html.Br(),
                                                    html.Small(" (Remarks)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_remarks',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_relinc_remarks',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '5em',
                                                        'width' : '100%',
                                                    },
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Estado san insidente", tag_required, html.Br(),
                                                    html.Small(" (Status)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relincstatus_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_relincstatus_id',
                                                    clearable = True,
                                                    disabled = True
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                            ],
                            id = 'rep_cre_div_relinc',
                            className = 'mt-3 mb-3'
                        ),
                        html.Hr(),
                        # Casualties
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-hospital-fill me-2'),
                                                        "Nadisgrasiya nga tawo",
                                                        #html.Br(),
                                                        html.Small(" (Casualty)", className = 'text-muted')
                                                    ]
                                                ),
                                                #html.P(
                                                #    [
                                                #        "Pinduta la an plus button", html.I(className = 'bi bi-plus-square ms-2 me-2'), "kun kinihanglan mo mag-report san damo nga insidente.",
                                                #        html.Br(),
                                                #        html.Small(
                                                #            ["(Click on the plus button", html.I(className = 'bi bi-plus-square ms-2 me-2'), "if you want to report multiple related incidents.)"],
                                                #            className = 'text-muted'
                                                #        )
                                                #    ]
                                                #)
                                            ]
                                        )
                                    ], class_name = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Klase san disgrasiya", tag_required, html.Br(),
                                                    html.Small(" (Type of casualty)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualtytype_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_casualtytype_id',
                                                    clearable = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Purok san disgrasiya", tag_required, html.Br(),
                                                    html.Small(" (Purok of occurrence)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_purok',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    id = 'rep_cre_input_casualty_purok',
                                                    type = 'number',
                                                    min = '1',
                                                    invalid = False,
                                                ),
                                                #dbc.FormText(
                                                #    "Alayon pagbutang san numero san purok kun diin ini natabó. (Please input the purok number where this incident occurred.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-3'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Petsa san disgrasiya", tag_required, html.Br(),
                                                    html.Small(" (Date of occurrence)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_date',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-2'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.DatePickerSingle(
                                                    id = 'rep_cre_input_casualty_date',
                                                    placeholder = 'MM/DD/YYYY',
                                                    #month_format = 'MMM Do, YYYY',
                                                    clearable = True,
                                                    #style = {'width' : '100%'}
                                                    className = 'w-100'
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-4'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Oras san disgrasiya", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (Time of occurrence)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_time',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.InputGroup(
                                                    [
                                                        dbc.Input(
                                                            id = 'rep_cre_input_casualty_time_hh',
                                                            placeholder = 'HH',
                                                            type = 'number',
                                                            min = 1,
                                                            max = 12,
                                                            invalid = False
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            id = 'rep_cre_input_casualty_time_mm',
                                                            placeholder = 'MM',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            id = 'rep_cre_input_casualty_time_ss',
                                                            placeholder = 'SS',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False
                                                        ),
                                                        dbc.Select(
                                                            id = 'rep_cre_input_casualty_time_ampm',
                                                            placeholder = 'AM/PM',
                                                            options = ['AM', 'PM']
                                                        )
                                                    ]
                                                ),
                                                #dbc.FormText(
                                                #    """Awtomátikó nga ginkukuha san LáMRAG an oras yana komo oras san panhitabó. Alayon pagbalyo sini kun sa iba nga oras nahitabó an imo ginhihimuan report.
                                                #    (LáMRAG automatically sets the current time as the time of occurrence. Please change this if the event you are reporting occurred at a different time.)""",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H5(
                                                    [
                                                        html.I(className = 'bi bi-person-vcard me-2'),
                                                        "Primero nga impormasyon san nadisgrasya",
                                                        #html.Br(),
                                                        html.Small(" (Basic information of casualty)", className = 'text-muted')
                                                    ]
                                                ),
                                            ]
                                        )
                                    ], class_name = 'mt-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Ngaran", tag_required, html.Br(),
                                                    html.Small(" (Name)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_name',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'text',
                                                    id = 'rep_cre_input_casualty_fname',
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
                                                    id = 'rep_cre_input_casualty_mname',
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
                                                    id = 'rep_cre_input_casualty_lname',
                                                    placeholder = 'Apelyido (Last name)',
                                                    invalid = False
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Edad (tuig)", tag_required, html.Br(),
                                                    html.Small(" (Age in years)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_age',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'number',
                                                    id = 'rep_cre_input_casualty_age',
                                                    #placeholder = 'Primero (First name)',
                                                    min = 0,
                                                    invalid = False
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-3'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Natawo nga babayi/lalaki", tag_required, html.Br(),
                                                    html.Small(" (Sex assigned at birth)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_assignedsex_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_casualty_assignedsex_id',
                                                    clearable = True
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-3'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H5(
                                                    [
                                                        html.I(className = 'bi bi-house me-2'),
                                                        "Gin-iistaran san nadisgrasya",
                                                        #html.Br(),
                                                        html.Small(" (Residence of casualty)", className = 'text-muted')
                                                    ],
                                                ),
                                            ]
                                        )
                                    ], class_name = 'mt-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Rehiyon", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (Region)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_region_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_cre_input_casualty_region_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                #value = 8
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Probinsya", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (Province)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_province_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_cre_input_casualty_province_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Siyudad/bungto", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (City/municipality)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_citymun_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_cre_input_casualty_citymun_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Barangay", #tag_required,
                                                    #html.Br(),
                                                    #html.Small(" (Barangay of residence)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_brgy_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                         dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_cre_input_casualty_brgy_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Kalsada", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (Street)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_street',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'rep_cre_input_casualty_street',
                                                placeholder = 'House No., Lot No., Block No., Street/Road, Village/Subdivision, Purok/Sitio',
                                                disabled = True,
                                                invalid = False
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                        ),
                                    ],
                                    class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H5(
                                                    [
                                                        html.I(className = 'bi bi-file-medical me-2'),
                                                        "Dugang nga impormasyon",
                                                        #html.Br(),
                                                        html.Small(" (Additional information)", className = 'text-muted')
                                                    ]
                                                ),
                                            ]
                                        )
                                    ], class_name = 'mt-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Rason san pagkadisgrasiya", html.Br(),
                                                    html.Small(" (Cause of casualty)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_cause',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 mb-md-1 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_casualty_cause',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '5em',
                                                        'width' : '100%',
                                                    },
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Iba pa nga komento", html.Br(),
                                                    html.Small(" (Remarks)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_remarks',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_casualty_remarks',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '5em',
                                                        'width' : '100%',
                                                    },
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Ginkuhaan sini nga impormasyon", html.Br(),
                                                    html.Small(" (Source of data)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_source',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'text',
                                                    id = 'rep_cre_input_casualty_source',
                                                    placeholder = 'Example: BDRRMC, CDRRMO, PDRRMO, DILG, BFP, PNP, OCD, etc.',
                                                    invalid = False
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Naprubaran na?", tag_required, html.Br(),
                                                    html.Small(" (Validated)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualtystatus_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_casualtystatus_id',
                                                    clearable = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                            ],
                            id = 'rep_cre_div_casual',
                            className = 'mt-3 mb-3'
                        ),
                        html.Hr(),
                        # Public utilities
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-gear-wide-connected me-2'),
                                                        "Pag-úndang san panpubliko nga utilidad",
                                                        #html.Br(),
                                                        html.Small(" (Interruption of public utilities)", className = 'text-muted')
                                                    ]
                                                ),
                                                #html.P(
                                                #    [
                                                #        "Pinduta la an plus button", html.I(className = 'bi bi-plus-square ms-2 me-2'), "kun kinihanglan mo mag-report san damo nga insidente.",
                                                #        html.Br(),
                                                #        html.Small(
                                                #            ["(Click on the plus button", html.I(className = 'bi bi-plus-square ms-2 me-2'), "if you want to report multiple related incidents.)"],
                                                #            className = 'text-muted'
                                                #        )
                                                #    ]
                                                #)
                                            ]
                                        )
                                    ], class_name = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Klase san utilidad", tag_required, html.Br(),
                                                    html.Small(" (Type of utility)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_pubutiltype_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Select(
                                                #dcc.Dropdown(
                                                    id = 'rep_cre_input_pubutiltype_id',
                                                    #clearable = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Naghahatag san serbisyo", tag_required, html.Br(),
                                                    html.Small(" (Service provider)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_pubutil_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Select(
                                                #dcc.Dropdown(
                                                    id = 'rep_cre_input_pubutil_id',
                                                    #clearable = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Klase san pag-úndang", tag_required, html.Br(),
                                                    html.Small(" (Type of interruption)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_utilinttype_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Select(
                                                #dcc.Dropdown(
                                                    id = 'rep_cre_input_utilinttype_id',
                                                    #clearable = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Petsa san pag-úndang o pagparong", tag_required, html.Br(),
                                                    html.Small(" (Date of interruption or outage)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_pubutilint_intdate',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.DatePickerSingle(
                                                    id = 'rep_cre_input_pubutilint_intdate',
                                                    placeholder = 'MM/DD/YYYY',
                                                    #month_format = 'MMM Do, YYYY',
                                                    clearable = True,
                                                    #style = {'width' : '100%'}
                                                    className = 'w-100'
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-2'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Oras san pag-úndang o pagparong", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (Time of interruption or outage)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_pubutilint_inttime',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.InputGroup(
                                                    [
                                                        dbc.Input(
                                                            id = 'rep_cre_input_pubutilint_inttime_hh',
                                                            placeholder = 'HH',
                                                            type = 'number',
                                                            min = 1,
                                                            max = 12,
                                                            invalid = False
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            id = 'rep_cre_input_pubutilint_inttime_mm',
                                                            placeholder = 'MM',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            id = 'rep_cre_input_pubutilint_inttime_ss',
                                                            placeholder = 'SS',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False
                                                        ),
                                                        dbc.Select(
                                                            id = 'rep_cre_input_pubutilint_inttime_ampm',
                                                            placeholder = 'AM/PM',
                                                            options = ['AM', 'PM']
                                                        )
                                                    ]
                                                ),
                                                #dbc.FormText(
                                                #    """Awtomátikó. nga ginkukuha san LáMRAG an oras yana komo oras san panhitabó. Alayon pagbalyo sini kun sa iba nga oras nahitabó an imo ginhihimuan report.
                                                #    (LáMRAG automatically sets the current time as the time of occurrence. Please change this if the event you are reporting occurred at a different time.)""",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-4'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Petsa san pagbalik", html.Br(),
                                                    html.Small(" (Date of restoration)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_pubutilint_resdate',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.DatePickerSingle(
                                                    id = 'rep_cre_input_pubutilint_resdate',
                                                    placeholder = 'MM/DD/YYYY',
                                                    #month_format = 'MMM Do, YYYY',
                                                    clearable = True,
                                                    #style = {'width' : '100%'}
                                                    className = 'w-100'
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-2'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Oras san pagbalik", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (Time of restoration)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_pubutilint_restime',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.InputGroup(
                                                    [
                                                        dbc.Input(
                                                            id = 'rep_cre_input_pubutilint_restime_hh',
                                                            placeholder = 'HH',
                                                            type = 'number',
                                                            min = 1,
                                                            max = 12,
                                                            invalid = False
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            id = 'rep_cre_input_pubutilint_restime_mm',
                                                            placeholder = 'MM',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            id = 'rep_cre_input_pubutilint_restime_ss',
                                                            placeholder = 'SS',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False
                                                        ),
                                                        dbc.Select(
                                                            id = 'rep_cre_input_pubutilint_restime_ampm',
                                                            placeholder = 'AM/PM',
                                                            options = ['AM', 'PM']
                                                        )
                                                    ]
                                                ),
                                                #dbc.FormText(
                                                #    """Awtomátikó. nga ginkukuha san LáMRAG an oras yana komo oras san panhitabó. Alayon pagbalyo sini kun sa iba nga oras nahitabó an imo ginhihimuan report.
                                                #    (LáMRAG automatically sets the current time as the time of occurrence. Please change this if the event you are reporting occurred at a different time.)""",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-4'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Iba pa nga komento", html.Br(),
                                                    html.Small(" (Remarks)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_pubutilint_remarks',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_pubutilint_remarks',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '5em',
                                                        'width' : '100%',
                                                    },
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                            ],
                            id = 'rep_cre_div_pubutil'
                        ),
                        html.Hr(),
                        # Submit button
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(className = 'bi bi-send-fill me-2'),
                                                    "Submit report"
                                                ],
                                                id = 'rep_cre_btn_submit',
                                                style = {'width': ' 100%'},
                                                href = '#'
                                            ),
                                            #md = 3, sm = 12,
                                            class_name = 'align-self-center col-md-3 mb-2'
                                        )
                                    ],
                                    class_name = 'justify-content-end'
                                )
                            ], className = 'mt-3'
                        )
                    ],
                    class_name = 'col-lg-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)

rep_cre_url_pathname = '/reports/create'

# Callback for recording GPS location
@app.callback(
    [
        Output('rep_cre_geoloc', 'update_now'),
    ],
    [
        Input('url', 'pathname'),
    ]
)

def rep_cre_geolocrefresh(pathname):
    if pathname == '/reports/create': return [True]
    else: return [False]

# Callback for setting URL links of hyperlinks for GPS location
@app.callback(
    [
        Output('rep_cre_geoloc_loc_war', 'href'),
        Output('rep_cre_geoloc_loc_en', 'href'),
        Output('rep_cre_input_time_hh', 'value'),
        Output('rep_cre_input_time_mm', 'value'),
        Output('rep_cre_input_time_ss', 'value'),
        Output('rep_cre_input_time_ampm', 'value')
    ],
    [
        Input('rep_cre_geoloc', 'position'),
        Input('rep_cre_geoloc', 'local_date')
    ]
)

def rep_cre_geolocrefresh(pos, date):
    href = None
    hh = None
    mm = None
    ss = None
    ampm = None
    if pos:
        lat = pos['lat']
        lon = pos ['lon']
        href = 'https://www.google.com/maps/place/%s,%s' % (lat, lon)
    if date:
        ampm = date.split(', ')[1].split(' ')[1]
        hh = date.split(', ')[1].split(' ')[0].split(':')[0]
        mm = date.split(', ')[1].split(' ')[0].split(':')[1]
        ss = date.split(', ')[1].split(' ')[0].split(':')[2]
    return [href, href, hh, mm, ss, ampm]

# Callback for populating basic dropdown menus
@app.callback(
    [
        Output('rep_cre_input_reporttype_id', 'options'),
        Output('rep_cre_input_relinctype_id', 'options'),
        Output('rep_cre_input_casualty_assignedsex_id', 'options'),
        Output('rep_cre_input_casualty_region_id', 'options'),
        Output('rep_cre_input_casualty_region_id', 'value'),
        Output('rep_cre_input_casualtytype_id', 'options'),
        Output('rep_cre_input_casualtystatus_id', 'options'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('app_region_id', 'data')
    ]
)

def rep_cre_populatedropdowns(pathname, region):
    if pathname == rep_cre_url_pathname:
        dropdowns = []

        # Report types
        sql = """SELECT label AS label, id AS value
        FROM utilities.reporttype;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        reporttypes = df.to_dict('records')
        dropdowns.append(reporttypes)

        # Related incident types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.relinctype;
        """
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        relinctypes = df.to_dict('records')
        dropdowns.append(relinctypes)

        # Assgined sex
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.assignedsex
        """
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        sexes = df.to_dict('records')
        dropdowns.append(sexes)

        # Regions (and setting app-locked region as default value)
        sql = """SELECT name as label, id as value
        FROM utilities.addressregion;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        regions = df.to_dict('records')
        dropdowns.append(regions)
        dropdowns.append(region)

        # Casualty type
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') as label, id as value
        FROM utilities.casualtytype;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        casualtytypes = df.to_dict('records')
        dropdowns.append(casualtytypes)

        # Casualty status
        sql = """SELECT CONCAT(label_war, ' (', label_en, ')') as label, id as value
        FROM utilities.casualtystatus;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        casualtystatuses = df.to_dict('records')
        dropdowns.append(casualtystatuses)

        return dropdowns
    else: raise PreventUpdate

# Callback for populating present provinces once present region is selected
@app.callback(
    [
        Output('rep_cre_input_casualty_province_id', 'options'),
        Output('rep_cre_input_casualty_province_id', 'disabled'),
        Output('rep_cre_input_casualty_province_id', 'value'),
    ],
    [
        Input('rep_cre_input_casualty_region_id', 'value'),
    ],
    prevent_initial_call = True
)

def rep_cre_populatepresentprovinces(region):
    provinces = []
    disabled = True
    if region:
        sql = """SELECT name as label, id as value
        FROM utilities.addressprovince
        WHERE region_id = %s;
        """
        values = [region]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        
        provinces = df.to_dict('records')
        disabled = False
    return [provinces, disabled, None]

# Callback for populating present cities/municipalities once present province is selected
@app.callback(
    [
        Output('rep_cre_input_casualty_citymun_id', 'options'),
        Output('rep_cre_input_casualty_citymun_id', 'disabled'),
        Output('rep_cre_input_casualty_citymun_id', 'value'),
    ],
    [
        Input('rep_cre_input_casualty_region_id', 'value'),
        Input('rep_cre_input_casualty_province_id', 'value'),
    ],
    prevent_initial_call = True
)

def rep_cre_populatepresentcitymuns(region, province):
    citymun = []
    disabled = True
    if region and province:
        sql = """SELECT name as label, id as value
        FROM utilities.addresscitymun
        WHERE region_id = %s AND province_id = %s;
        """
        values = [region, province]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        
        citymun = df.to_dict('records')
        disabled = False
    return [citymun, disabled, None]

# Callback for populating present barangays once present city/municipality is selected
@app.callback(
    [
        Output('rep_cre_input_casualty_brgy_id', 'options'),
        Output('rep_cre_input_casualty_brgy_id', 'disabled'),
        Output('rep_cre_input_casualty_brgy_id', 'value'),
    ],
    [
        Input('rep_cre_input_casualty_region_id', 'value'),
        Input('rep_cre_input_casualty_province_id', 'value'),
        Input('rep_cre_input_casualty_citymun_id', 'value'),
    ],
    prevent_initial_call = True
)

def rep_cre_populatepresentbrgys(region, province, citymun):
    brgy = []
    disabled = True
    if region and province and citymun:
        sql = """SELECT name as label, id as value
        FROM utilities.addressbrgy
        WHERE region_id = %s AND province_id = %s AND citymun_id = %s;
        """
        values = [region, province, citymun]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        
        brgy = df.to_dict('records')
        disabled = False
    return [brgy, disabled, None]

# Callback for enabling present street address once present city/municipality is selected
@app.callback(
    [
        Output('rep_cre_input_casualty_street', 'disabled'),
        Output('rep_cre_input_casualty_street', 'value'),
    ],
    [
        Input('rep_cre_input_casualty_region_id', 'value'),
        Input('rep_cre_input_casualty_province_id', 'value'),
        Input('rep_cre_input_casualty_citymun_id', 'value'),
        Input('rep_cre_input_casualty_brgy_id', 'value'),
    ],
    prevent_initial_call = True
)

def rep_cre_enablepresentstreet(region, province, citymun, brgy):
    disabled = True
    if region and province and citymun and brgy: disabled = False
    return [disabled, None]

# Callback for populating related incident status dropdown once incident type is selected
@app.callback(
    [
        Output('rep_cre_input_relincstatus_id', 'options'),
        Output('rep_cre_input_relincstatus_id', 'value'),
        Output('rep_cre_input_relincstatus_id', 'disabled')
    ],
    [
        Input('rep_cre_input_relinctype_id', 'value')
    ],
    prevent_initial_call = True
)

def rep_cre_populaterelincstatus(type):
    options = None
    disabled = True
    if type:
        sql = """SELECT CONCAT(label_war, ' (', label_en, ')') AS label,
            id AS value FROM utilities.relincstatus
            WHERE relinctype_id = %s;"""
        values = [type]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        if df.shape[0] > 0:
            options = df.to_dict('records')
            disabled = False
    return [options, None, disabled]