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
                                    id = 'rep_cre_row_header'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ], class_name = 'mb-2',
                                    id = 'rep_cre_row_event'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
                                        )
                                    ], class_name = 'mb-2',
                                    id = 'rep_cre_row_reporttype'
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
                                    ]
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
                                                        html.I(className = 'bi bi-pencil-square me-2'),
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_relinctype_id',
                                                    clearable = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Purok kun diin nanhitabó", tag_required, html.Br(),
                                                    html.Small(" (Affected/concerned purok)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_purok',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    id = 'rep_cre_input_relinc_purok',
                                                    type =  'text', #'number',
                                                    #min = '1',
                                                    invalid = False,
                                                ),
                                                #dbc.FormText(
                                                #    "Alayon pagbutang san numero san purok kun diin ini natabó. (Please input the purok number where this incident occurred.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-4'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-2'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Petsa san panhitabó", tag_required, html.Br(),
                                                    html.Small(" (Date of occurrence)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_date',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-2'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Oras san panhitabó", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (Time of occurrence)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_time',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-2'
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
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-5'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
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
                                                id = 'rep_cre_label_relinc_status_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_relinc_status_id',
                                                    clearable = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
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
                                                        "Disgrasiya",
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
                                                id = 'rep_cre_label_casualtype_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_casual_id',
                                                    clearable = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-3'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Purok kun diin nanhitabó", tag_required, html.Br(),
                                                    html.Small(" (Purok of occurrence)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casual_purok',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    id = 'rep_cre_input_relinc_purok',
                                                    type = 'text', #'number',
                                                    #min = '1',
                                                    invalid = False,
                                                ),
                                                #dbc.FormText(
                                                #    "Alayon pagbutang san numero san purok kun diin ini natabó. (Please input the purok number where this incident occurred.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-3'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Ngaran san nadisgrasiya", tag_required, html.Br(),
                                                    html.Small(" (Name of casualty)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casual_name',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'text',
                                                    id = 'rep_cre_input_casual_fname',
                                                    placeholder = 'Primero (First name)',
                                                    invalid = False
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'text',
                                                    id = 'rep_cre_input_casual_mname',
                                                    placeholder = 'Butnga (Middle name)',
                                                    invalid = False
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'text',
                                                    id = 'rep_cre_input_casual_lname',
                                                    placeholder = 'Apelyido (Last name)',
                                                    invalid = False
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Edad san nadisgrasiya", tag_required, html.Br(),
                                                    html.Small(" (Age of casualty)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casual_age',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'number',
                                                    id = 'rep_cre_input_casual_age',
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-3'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Natawo nga babayi/lalaki", tag_required, html.Br(),
                                                    html.Small(" (Sex assigned at birth)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casual_assignedsex_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_casual_assignedsex_id',
                                                    clearable = True
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-3'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H5(
                                                    [
                                                        html.I(className = 'bi bi-person me-2'),
                                                        "Gin-iistaran san nadisgrasya",
                                                        #html.Br(),
                                                        html.Small(" (Residence of casualty)", className = 'text-muted')
                                                    ]
                                                ),
                                            ]
                                        )
                                    ], class_name = 'mb-2'
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
                                                id = 'rep_cre_label_casual_region_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_cre_input_casual_region_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                value = 8
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
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
                                                id = 'rep_cre_label_casual_province_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_cre_input_casual_province_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
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
                                                id = 'rep_cre_label_casual_citymun_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_cre_input_casual_citymun_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
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
                                                id = 'rep_cre_label_casual_brgy_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
                                        ),
                                         dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_cre_input_casual_brgy_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Kalsada", #usr_reg_tag_required,
                                                    html.Br(),
                                                    html.Small(" (Street)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casual_street',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'rep_cre_input_casual_street',
                                                placeholder = 'House No., Lot No., Block No., Street/Road, Village/Subdivision, Purok/Sitio',
                                                disabled = True,
                                                invalid = False
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9'
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
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Rason san pagkadisgrasiya", html.Br(),
                                                    html.Small(" (Cause of casualty)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casual_cause',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 mb-md-1 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_casual_cause',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '5em',
                                                        'width' : '100%',
                                                    },
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
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
                                                id = 'rep_cre_label_casual_remarks',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_casual_remarks',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '5em',
                                                        'width' : '100%',
                                                    },
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
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
                                                id = 'rep_cre_label_casual_source',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'text',
                                                    id = 'rep_cre_input_casual_source',
                                                    placeholder = 'Example: BDRRMC, CDRRMO, PDRRMO, DILG, BFP, PNP, OCD, etc.',
                                                    invalid = False
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
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
                                                id = 'rep_cre_label_casual_validated_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_label_casual_validated_id',
                                                    clearable = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                #    color = 'secondary',
                                                #    class_name = 'mt-1'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = 'mb-2',
                                ),
                            ],
                            id = 'rep_cre_div_casual',
                            className = 'mt-3 mb-3'
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
                    class_name = 'col-md-10'
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
        Output('rep_cre_input_relinc_time_hh', 'value'),
        Output('rep_cre_input_relinc_time_mm', 'value'),
        Output('rep_cre_input_relinc_time_ss', 'value'),
        Output('rep_cre_input_relinc_time_ampm', 'value')
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
        Output('rep_cre_input_casual_assignedsex_id', 'options'),
        Output('rep_cre_input_casual_region_id', 'options'),
    ],
    [
        Input('url', 'pathname')
    ]
)

def rep_cre_populatedropdowns(pathname):
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
        sql = """SELECT CONCAT(label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.assignedsex
        """
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        sexes = df.to_dict('records')
        dropdowns.append(sexes)

        # Regions
        sql = """SELECT name as label, id as value
        FROM utilities.addressregion;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        regions = df.to_dict('records')
        dropdowns.append(regions)

        return dropdowns
    else: raise PreventUpdate

# Callback for populating descriptions taken from the database
@app.callback(
    [
        Output('rep_cre_col_damagetype_desc1', 'children'),
        Output('rep_cre_col_damagetype_desc2', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)

def rep_cre_populatedescriptions(pathname):
    if pathname == rep_cre_url_pathname:
        col1 = []
        col2 = []

        # Damage types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value, desc_war AS desc_war, desc_en AS desc_en
        FROM utilities.damagetype
        """
        values = []
        cols = ['label', 'value', 'desc_war', 'desc_en']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')        
        damagetypes = df.to_dict('records')
        c = 1
        for i in damagetypes:
            item = html.Li(
                [
                    html.B(i['label']), html.Br(),
                    html.Div(
                        [
                            i['desc_war'], html.Br(),
                            html.Small(i['desc_en'], className = 'text-muted')
                        ],
                        className = 'ms-3'
                    )
                ],
                className = 'mb-3'
            ),
            if c % 2 == 1: col1 += item
            else: col2 += item
            c += 1
        return [col1, col2]
    else: raise PreventUpdate

# Callback for populating present provinces once present region is selected
@app.callback(
    [
        Output('rep_cre_input_casual_province_id', 'options'),
        Output('rep_cre_input_casual_province_id', 'disabled'),
        Output('rep_cre_input_casual_province_id', 'value'),
    ],
    [
        Input('rep_cre_input_casual_region_id', 'value'),
    ]
)

def usr_reg_populatepresentprovinces(region):
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
        Output('rep_cre_input_casual_citymun_id', 'options'),
        Output('rep_cre_input_casual_citymun_id', 'disabled'),
        Output('rep_cre_input_casual_citymun_id', 'value'),
    ],
    [
        Input('rep_cre_input_casual_region_id', 'value'),
        Input('rep_cre_input_casual_province_id', 'value'),
    ]
)

def usr_reg_populatepresentcitymuns(region, province):
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
        Output('rep_cre_input_casual_brgy_id', 'options'),
        Output('rep_cre_input_casual_brgy_id', 'disabled'),
        Output('rep_cre_input_casual_brgy_id', 'value'),
    ],
    [
        Input('rep_cre_input_casual_region_id', 'value'),
        Input('rep_cre_input_casual_province_id', 'value'),
        Input('rep_cre_input_casual_citymun_id', 'value'),
    ]
)

def usr_reg_populatepresentbrgys(region, province, citymun):
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
        Output('rep_cre_input_casual_street', 'disabled'),
        Output('rep_cre_input_casual_street', 'value'),
    ],
    [
        Input('rep_cre_input_casual_region_id', 'value'),
        Input('rep_cre_input_casual_province_id', 'value'),
        Input('rep_cre_input_casual_citymun_id', 'value'),
        Input('rep_cre_input_casual_brgy_id', 'value'),
    ]
)

def usr_reg_enablepresentstreet(region, province, citymun, brgy):
    disabled = True
    if region and province and citymun and brgy: disabled = False
    return [disabled, None]