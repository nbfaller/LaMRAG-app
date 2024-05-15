# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import hashlib
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
        dcc.Geolocation(id = 'rep_cre_geoloc'),
        # Use this dcc.Store to facilitate URL redirection
        # once a new report is made, similar to logging in
        dcc.Store(id = 'rep_cre_newreport_id', data = 1),
        dcc.Store(id = 'rep_cre_newversion_id', data = 1),
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
                                                html.H1("File a report"),
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
                                            id = 'rep_cre_row_header',
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
                                                                            html.Span(id = 'rep_cre_alert_inputvalidation_span_missing')
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            id = 'rep_cre_alert_inputvalidation',
                                                            is_open = False,
                                                            color = 'warning',
                                                            class_name = label_m,
                                                            dismissable = True,
                                                            #fade = True,
                                                        )
                                                    ]
                                                )
                                            ],
                                            id = 'rep_cre_row_inputvalidation',
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
                                                                            """Pahibaro: Kukuhaon san LáMRAG an imo ngaran, an petsa yana, ug
                                                                            an oras yana kaparte sini nga report. Mababaruan mo kun panano ini gingagamit didi: """,
                                                                            html.Br(),
                                                                            html.Small(
                                                                                [
                                                                                    """(Please note that LáMRAG will record your name, the date today, and the current time
                                                                                    as part of this report. You can learn how your location is used here: )"""
                                                                                ],
                                                                                className = 'text-muted'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            id = 'rep_cre_alert_geolocnotice',
                                                            color = 'info',
                                                            class_name = 'mb-3',
                                                            dismissable = True
                                                        )
                                                    ]
                                                )
                                            ],
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Barangay", tag_required, #html.Br(),
                                                            #html.Small(" (Event)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_brgy_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.Dropdown(
                                                            id = 'rep_cre_input_brgy_id',
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
                                            id = 'rep_cre_row_brgy_id',
                                            class_name = row_m,
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
                                                        class_name = label_m
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
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                )
                                            ],
                                            id = 'rep_cre_row_event',
                                            class_name = row_m,
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
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.Dropdown(
                                                            id = 'rep_cre_input_reporttype_id',
                                                            #required = True,
                                                            clearable = True,
                                                        ),
                                                        dbc.FormText(
                                                            "Usa la nga initial report an puwede himuon. (Initial reports can only be filed once.)",
                                                            color = 'secondary',
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                )
                                            ],
                                            id = 'rep_cre_row_reporttype',
                                            class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Purok san panhitabó", tag_required, html.Br(),
                                                            html.Small(" (Purok of occurrence)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_purok',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            id = 'rep_cre_input_purok',
                                                            type = 'number',
                                                            min = '1',
                                                            invalid = False,
                                                            required = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Alayon pagbutang san numero san purok kun diin ini natabó. (Please input the purok number where this incident occurred.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Petsa san panhitabó", tag_required, html.Br(),
                                                            html.Small(" (Date of occurrence)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_date',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-2'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.DatePickerSingle(
                                                            id = 'rep_cre_input_date',
                                                            placeholder = 'MM/DD/YYYY',
                                                            #month_format = 'MMM Do, YYYY',
                                                            clearable = True,
                                                            #style = {'width' : '100%'}
                                                            className = 'w-100'
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-4'
                                                ),
                                            ], class_name = row_m,
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Oras san panhitabó", #tag_required,
                                                            html.Br(),
                                                            html.Small(" (Time of occurrence)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_time',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.InputGroup(
                                                            [
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_time_hh',
                                                                    placeholder = 'HH',
                                                                    type = 'number',
                                                                    min = 1,
                                                                    max = 12,
                                                                    invalid = False
                                                                ),
                                                                dbc.InputGroupText(":"),
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_time_mm',
                                                                    placeholder = 'MM',
                                                                    type = 'number',
                                                                    min = 0,
                                                                    max = 59,
                                                                    invalid = False
                                                                ),
                                                                dbc.InputGroupText(":"),
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_time_ss',
                                                                    placeholder = 'SS',
                                                                    type = 'number',
                                                                    min = 0,
                                                                    max = 59,
                                                                    invalid = False
                                                                ),
                                                                dbc.Select(
                                                                    id = 'rep_cre_input_time_ampm',
                                                                    placeholder = 'AM/PM',
                                                                    options = ['AM', 'PM']
                                                                )
                                                            ]
                                                        ),
                                                        dbc.FormText(
                                                            """Awtomátikó nga ginkukuha san LáMRAG an oras yana komo oras san panhitabó. Alayon pagbalyo sini kun sa iba nga oras nahitabó an imo ginhihimuan report.
                                                            (LáMRAG automatically sets the current time as the time of occurrence. Please change this if the event you are reporting occurred at a different time.)""",
                                                            color = 'secondary',
                                                            class_name = ftext_m
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                ),
                                            ], class_name = row_m,
                                        )
                                    ],
                                    id = 'rep_cre_div_basicdetails',
                                    className = header_m
                                ),
                                # Related incidents
                                html.Div(
                                    [
                                        html.Hr(),
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
                                                    ]
                                                )
                                            ], class_name = row_m
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
                                                        class_name = label_m
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
                                                        #    class_name = ftext_m
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
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            id = 'rep_cre_input_relinc_qty',
                                                            type = 'number',
                                                            #value = 1,
                                                            min = 1,
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-2'
                                                ),
                                            ], class_name = row_m,
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
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.Textarea(
                                                            id = 'rep_cre_input_relinc_description',
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
                                            ], class_name = row_m
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
                                                        class_name = label_m
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
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Kamutangan san insidente", tag_required, html.Br(),
                                                            html.Small(" (Status)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_relincstatus_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                            id = 'rep_cre_input_relincstatus_id',
                                                            #clearable = True,
                                                            disabled = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                ),
                                            ], class_name = row_m,
                                        ),
                                    ],
                                    id = 'rep_cre_div_relinc',
                                    className = row_m,
                                    style = {'display' : 'none'}
                                ),
                                # Casualties
                                html.Div(
                                    [
                                        html.Hr(),
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
                                                    ]
                                                )
                                            ], class_name = row_m
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
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                            id = 'rep_cre_input_casualtytype_id',
                                                            #clearable = True,
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
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
                                            ], class_name = subhead_m
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
                                                        class_name = label_m
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
                                            ], class_name = row_m,
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
                                                        class_name = label_m
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
                                                        #    class_name = ftext_m
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
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                            id = 'rep_cre_input_casualty_assignedsex_id',
                                                            #clearable = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-3'
                                                ),
                                            ], class_name = row_m,
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
                                            ], class_name = subhead_m
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
                                                        class_name = label_m
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
                                            ], class_name = row_m
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
                                                        class_name = label_m
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
                                            ], class_name = row_m
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
                                                        class_name = label_m
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
                                            ], class_name = row_m
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
                                                        class_name = label_m
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
                                            ], class_name = row_m
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
                                                        class_name = label_m
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
                                            class_name = row_m
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
                                            ], class_name = subhead_m
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
                                                        class_name = label_m
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
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Ginkuhaan san impormasyon", tag_required, html.Br(),
                                                            html.Small(" (Source of data)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_casualty_source',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            type = 'text',
                                                            id = 'rep_cre_input_casualty_infosource',
                                                            placeholder = 'Example: BDRRMC, CDRRMO, PDRRMO, DILG, BFP, PNP, OCD, etc.',
                                                            invalid = False
                                                        ),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                )
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Kamutangan san pagprubar", tag_required, html.Br(),
                                                            html.Small(" (Validation status)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_casualtystatus_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                            id = 'rep_cre_input_casualtystatus_id',
                                                            #clearable = True,
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                ),
                                            ], class_name = row_m,
                                        ),
                                    ],
                                    id = 'rep_cre_div_casualty',
                                    className = row_m,
                                    style = {'display' : 'none'}
                                ),
                                # Public utilities
                                html.Div(
                                    [
                                        html.Hr(),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H4(
                                                            [
                                                                html.I(className = 'bi bi-gear-wide-connected me-2'),
                                                                "Kamutangan san panpubliko nga utilidad",
                                                                #html.Br(),
                                                                html.Small(" (Status of public utilities)", className = 'text-muted')
                                                            ]
                                                        ),
                                                    ]
                                                )
                                            ], class_name = row_m
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
                                                        class_name = label_m
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
                                                            "Naghahatag san serbisyo", tag_required, html.Br(),
                                                            html.Small(" (Service provider)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_pubutil_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                        #dcc.Dropdown(
                                                            id = 'rep_cre_input_pubutil_id',
                                                            #clearable = True,
                                                            disabled = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                ),
                                            ], class_name = row_m,
                                        ),
                                        dbc.Row(
                                            dbc.Col(
                                                id = 'rep_cre_col_pubutilinttype_desc',
                                                class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                            ),
                                            class_name = label_m,
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Klase san pag-úndang", tag_required, html.Br(),
                                                            html.Small(" (Type of interruption/outage)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_pubutilinttype_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                        #dcc.Dropdown(
                                                            id = 'rep_cre_input_pubutilinttype_id',
                                                            #clearable = True,
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
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
                                                            "Petsa san pag-undang",  tag_required, html.Br(),
                                                            html.Small(" (Date of interruption/outage)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_pubutilint_int_date',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.DatePickerSingle(
                                                            id = 'rep_cre_input_pubutilint_int_date',
                                                            placeholder = 'MM/DD/YYYY',
                                                            #month_format = 'MMM Do, YYYY',
                                                            clearable = True,
                                                            #style = {'width' : '100%'}
                                                            className = 'w-100',
                                                            disabled = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-2'
                                                ),
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Oras san pag-undang", #tag_required,
                                                            html.Br(),
                                                            html.Small(" (Time of interruption/outage)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_pubutilint_int_time',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.InputGroup(
                                                            [
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_pubutilint_int_time_hh',
                                                                    placeholder = 'HH',
                                                                    type = 'number',
                                                                    min = 1,
                                                                    max = 12,
                                                                    invalid = False,
                                                                    disabled = True
                                                                ),
                                                                dbc.InputGroupText(":"),
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_pubutilint_int_time_mm',
                                                                    placeholder = 'MM',
                                                                    type = 'number',
                                                                    min = 0,
                                                                    max = 59,
                                                                    invalid = False,
                                                                    disabled = True
                                                                ),
                                                                dbc.InputGroupText(":"),
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_pubutilint_int_time_ss',
                                                                    placeholder = 'SS',
                                                                    type = 'number',
                                                                    min = 0,
                                                                    max = 59,
                                                                    invalid = False,
                                                                    disabled = True
                                                                ),
                                                                dbc.Select(
                                                                    id = 'rep_cre_input_pubutilint_int_time_ampm',
                                                                    placeholder = 'AM/PM',
                                                                    options = ['AM', 'PM'],
                                                                    disabled = True
                                                                )
                                                            ]
                                                        ),
                                                        #dbc.FormText(
                                                        #    """Awtomátikó. nga ginkukuha san LáMRAG an oras yana komo oras san panhitabó. Alayon pagbalyo sini kun sa iba nga oras nahitabó an imo ginhihimuan report.
                                                        #    (LáMRAG automatically sets the current time as the time of occurrence. Please change this if the event you are reporting occurred at a different time.)""",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-4'
                                                ),
                                            ], class_name = row_m,
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Petsa san pagbalik", html.Br(),
                                                            html.Small(" (Date of restoration)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_pubutilint_res_date',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.DatePickerSingle(
                                                            id = 'rep_cre_input_pubutilint_res_date',
                                                            placeholder = 'MM/DD/YYYY',
                                                            #month_format = 'MMM Do, YYYY',
                                                            clearable = True,
                                                            #style = {'width' : '100%'}
                                                            className = 'w-100'
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
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
                                                        id = 'rep_cre_label_pubutilint_res_time',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.InputGroup(
                                                            [
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_pubutilint_res_time_hh',
                                                                    placeholder = 'HH',
                                                                    type = 'number',
                                                                    min = 1,
                                                                    max = 12,
                                                                    invalid = False
                                                                ),
                                                                dbc.InputGroupText(":"),
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_pubutilint_res_time_mm',
                                                                    placeholder = 'MM',
                                                                    type = 'number',
                                                                    min = 0,
                                                                    max = 59,
                                                                    invalid = False
                                                                ),
                                                                dbc.InputGroupText(":"),
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_pubutilint_res_time_ss',
                                                                    placeholder = 'SS',
                                                                    type = 'number',
                                                                    min = 0,
                                                                    max = 59,
                                                                    invalid = False
                                                                ),
                                                                dbc.Select(
                                                                    id = 'rep_cre_input_pubutilint_res_time_ampm',
                                                                    placeholder = 'AM/PM',
                                                                    options = ['AM', 'PM']
                                                                )
                                                            ]
                                                        ),
                                                        #dbc.FormText(
                                                        #    """Awtomátikó. nga ginkukuha san LáMRAG an oras yana komo oras san panhitabó. Alayon pagbalyo sini kun sa iba nga oras nahitabó an imo ginhihimuan report.
                                                        #    (LáMRAG automatically sets the current time as the time of occurrence. Please change this if the event you are reporting occurred at a different time.)""",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-4'
                                                ),
                                            ], class_name = row_m,
                                        )
                                    ],
                                    id = 'rep_cre_div_pubutil',
                                    className = row_m,
                                    style = {'display' : 'none'}
                                ),
                                # Damaged house
                                html.Div(
                                    [
                                        html.Hr(),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H4(
                                                            [
                                                                html.I(className = 'bi bi-house-x-fill me-2'),
                                                                "Narubat nga balay",
                                                                #html.Br(),
                                                                html.Small(" (Damaged house)", className = 'text-muted')
                                                            ]
                                                        ),
                                                    ]
                                                )
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            dbc.Col(
                                                id = 'rep_cre_col_dmgdhousetype_desc',
                                                class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                            ),
                                            class_name = label_m,
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Klase san pagkarubat", tag_required, html.Br(),
                                                            html.Small(" (Type of damage)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_dmgdhousetype_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                            id = 'rep_cre_input_dmgdhousetype_id',
                                                            #clearable = True,
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
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
                                                    [
                                                        html.H5(
                                                            [
                                                                html.I(className = 'bi bi-person-vcard me-2'),
                                                                "Primero nga impormasyon san tag-iya",
                                                                #html.Br(),
                                                                html.Small(" (Basic information of homeowner)", className = 'text-muted')
                                                            ]
                                                        ),
                                                    ]
                                                )
                                            ], class_name = subhead_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Ngaran", tag_required, html.Br(),
                                                            html.Small(" (Name)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_dmgdhouse_name',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            type = 'text',
                                                            id = 'rep_cre_input_dmgdhouse_fname',
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
                                                            id = 'rep_cre_input_dmgdhouse_mname',
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
                                                            id = 'rep_cre_input_dmgdhouse_lname',
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
                                                            "Edad (tuig)", tag_required, html.Br(),
                                                            html.Small(" (Age in years)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_dmgdhouse_age',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            type = 'number',
                                                            id = 'rep_cre_input_dmgdhouse_age',
                                                            #placeholder = 'Primero (First name)',
                                                            min = 0,
                                                            invalid = False
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
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
                                                        id = 'rep_cre_label_dmgdhouse_assignedsex_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                            id = 'rep_cre_input_dmgdhouse_assignedsex_id',
                                                            #clearable = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-3'
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
                                                        id = 'rep_cre_label_dmgdhouse_geoloc',
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
                                                                        id = 'rep_cre_input_dmgdhouse_loc',
                                                                        #disabled = True,
                                                                        #placeholder = "Pili (select)...",
                                                                        #value = 8
                                                                    ),
                                                                    class_name = 'align-self-center col-12 col-md-6 col-lg-8 mb-2 mb-md-0'
                                                                ),
                                                                dbc.Col(
                                                                    dbc.Switch(
                                                                        id = 'rep_cre_input_selectgps',
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
                                    ],
                                    id = 'rep_cre_div_dmgdhouse',
                                    className = row_m,
                                    style = {'display' : 'none'}
                                ),
                                # Infrastructure
                                html.Div(
                                    [
                                        html.Hr(),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H4(
                                                            [
                                                                html.I(className = 'bi bi-building-fill-slash me-2'),
                                                                "Narubat nga imprastruktura",
                                                                #html.Br(),
                                                                html.Small(" (Damaged infrastructure)", className = 'text-muted')
                                                            ]
                                                        ),
                                                    ]
                                                )
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Tipo san imprastruktura", tag_required, html.Br(),
                                                            html.Small(" (Infrastructure type)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_infratype_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                        #dcc.Dropdown(
                                                            id = 'rep_cre_input_infratype_id',
                                                            #clearable = True,
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
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
                                                            "Klase", tag_required, html.Br(),
                                                            html.Small(" (Classification)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_infraclass_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                        #dcc.Dropdown(
                                                            id = 'rep_cre_input_infraclass_id',
                                                            #clearable = True,
                                                            #disabled = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
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
                                                            "Ngaran/deskripsiyon", tag_required, html.Br(),
                                                            html.Small(" (Name/description)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_dmgdinfra_desc',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            id = 'rep_cre_input_dmgdinfra_description',
                                                            placeholder = 'Example: Road name, bridge name, name of building/structure/equipment',
                                                            invalid = False,
                                                            #disabled = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
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
                                                            "Kadamo san narubat", tag_required, html.Br(),
                                                            html.Small(" (Quantity of damage)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_dmgdinfra_qty',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.InputGroup(
                                                            [
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_dmgdinfra_qty',
                                                                    #placeholder = 'Example: Road name, bridge name, name of building/structure/equipment',
                                                                    type = 'number',
                                                                    min = 1,
                                                                    value = 1,
                                                                    invalid = False,
                                                                    #disabled = True
                                                                ),
                                                                dbc.Select(
                                                                    id = 'rep_cre_input_dmgdinfra_qtyunit_id',
                                                                )
                                                            ]
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Kantidad san narubat", #tag_required,
                                                            html.Br(),
                                                            html.Small(" (Cost of damage)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_dmgdinfra_cost',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-2'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.InputGroup(
                                                            [
                                                                dbc.InputGroupText("₱"),
                                                                dbc.Input(
                                                                    id = 'rep_cre_input_dmgdinfra_cost',
                                                                    #placeholder = 'Example: Road name, bridge name, name of building/structure/equipment',
                                                                    type = 'number',
                                                                    min = 0,
                                                                    #value = 1,
                                                                    invalid = False,
                                                                    #disabled = True
                                                                ),
                                                            ]
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-4'
                                                ),
                                            ], class_name = row_m,
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Kamutangan", tag_required, html.Br(),
                                                            html.Small(" (Status)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_dmgdinfratype_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Select(
                                                        #dcc.Dropdown(
                                                            id = 'rep_cre_label_dmgdinfratype_id',
                                                            #clearable = True,
                                                            #disabled = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                ),
                                            ], class_name = row_m,
                                        ),
                                    ],
                                    id = 'rep_cre_div_dmgdinfra',
                                    className = row_m,
                                    style = {'display' : 'none'}
                                ),
                                # Submit button
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Iba pa nga komento", html.Br(),
                                                            html.Small(" (Remarks)", className = 'text-muted')
                                                        ],
                                                        id = 'rep_cre_label_remarks',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.Textarea(
                                                            id = 'rep_cre_input_remarks',
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
                                            ], class_name = row_m
                                        ),
                                        html.Hr(),
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
                                                        href = '#',
                                                        type = 'submit'
                                                    ),
                                                    #md = 3, sm = 12,
                                                    class_name = 'align-self-center col-md-3 mb-2'
                                                )
                                            ],
                                            class_name = 'justify-content-end'
                                        )
                                    ],
                                    id = 'rep_cre_div_submit',
                                    #className = footer_m,
                                    style = {'display' : 'none'}
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
                                                html.H4("Confirm report creation"),
                                                html.P(
                                                    [
                                                        """Alayon pagbutang san imo password para makumpirma an paghimo sini nga report.
                                                        Alayon liwat pagseguro nga sakto an ngatanan nga impormasyon nga imo ginhatag.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """(Please enter your password to confirm the creation of this report.
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
                                                                id = 'rep_cre_alert_passwordvalidation_col_text'
                                                            )
                                                        ]
                                                    ),
                                                    id = 'rep_cre_alert_passwordvalidation',
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
                                                    id = 'rep_cre_input_password',
                                                    placeholder = ['Enter password'],
                                                    invalid = False
                                                ),
                                            ]
                                        )
                                    ], class_name = row_m
                                ),
                            ],
                            id = 'rep_cre_modal_confirm_body'
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
                                                id = 'rep_cre_btn_confirm',
                                                style = {'width': ' 100%'},
                                                type = 'submit'
                                            ),
                                            class_name = 'align-self-center col-12 col-md-auto'
                                        )
                                    ],
                                    class_name = 'justify-content-end'
                                )
                            ],
                            id = 'rep_cre_modal_confirm_footer'
                        )
                    ]
                )
            ],
            id = 'rep_cre_modal_confirm',
            is_open = False,
            centered = True,
            scrollable = True,
            backdrop = True,
            #size = 'lg',
        ),
    ]
)

rep_cre_url_pathname = '/reports/create'

# Callback for recording GPS location
@app.callback(
    [
        Output('rep_cre_geoloc', 'update_now'),
    ],
    [
        Input('rep_cre_input_selectgps', 'value'),
    ]
)

def rep_cre_geolocrefresh(selectgps):
    if selectgps: return [True]
    else: return [False]

# Callback for setting URL links of hyperlinks for GPS location
@app.callback(
    [
        Output('rep_cre_input_dmgdhouse_loc', 'value'),
        Output('rep_cre_input_dmgdhouse_loc', 'disabled'),
    ],
    [
        Input('rep_cre_input_selectgps', 'value'),
    ],
    [
        State('rep_cre_geoloc', 'position'),
        State('rep_cre_geoloc', 'local_date')
    ],
    prevent_initial_call = True
)

def rep_cre_geolocset(selectgps, pos, date):
    geoloc = None
    disabled = False
    if selectgps:
        lat = pos['lat']
        lon = pos ['lon']
        geoloc = '%s, %s' % (lat, lon)
        disabled = True
    return [geoloc, disabled]

# Callback for populating basic dropdown menus and descriptions
@app.callback(
    [
        # Report type
        Output('rep_cre_input_reporttype_id', 'options'),
        # Event
        Output('rep_cre_input_event_id', 'options'),
        # Barangay
        Output('rep_cre_input_brgy_id', 'options'),
        Output('rep_cre_input_brgy_id', 'disabled'),
        Output('rep_cre_input_brgy_id', 'value'),
        # Related incident
        Output('rep_cre_input_relinctype_id', 'options'),
        # Assigned sex at birth
        Output('rep_cre_input_casualty_assignedsex_id', 'options'),
        Output('rep_cre_input_dmgdhouse_assignedsex_id', 'options'),
        # Casualty
        Output('rep_cre_input_casualty_region_id', 'options'),
        Output('rep_cre_input_casualty_region_id', 'value'),
        Output('rep_cre_input_casualtytype_id', 'options'),
        Output('rep_cre_input_casualtystatus_id', 'options'),
        # Public utility status
        Output('rep_cre_input_pubutiltype_id', 'options'),
        Output('rep_cre_input_pubutilinttype_id', 'options'),
        Output('rep_cre_col_pubutilinttype_desc', 'children'),
        # Damaged house/infrastructure
        Output('rep_cre_input_dmgdhousetype_id', 'options'),
        Output('rep_cre_label_dmgdinfratype_id', 'options'),
        Output('rep_cre_col_dmgdhousetype_desc', 'children'),
        # Infrastructure
        Output('rep_cre_input_infratype_id', 'options'),
        Output('rep_cre_input_infraclass_id', 'options'),
        Output('rep_cre_input_dmgdinfra_qtyunit_id', 'options'),
        Output('rep_cre_input_dmgdinfra_qtyunit_id', 'value'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data')
    ]
)

def rep_cre_populatedropdowns(pathname, region, province, citymun, brgy):
    if pathname == rep_cre_url_pathname:
        dropdowns = []

        # Report types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.reporttype;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        reporttypes = df.to_dict('records')
        dropdowns.append(reporttypes)

        # Events
        sql = """SELECT event.name AS label, event.id AS value
        FROM events.event
        INNER JOIN events.eventbrgy ON event.id = eventbrgy.event_id
        LEFT JOIN utilities.eventtype ON event.type_id = eventtype.id
        WHERE eventbrgy.region_id = %s AND eventbrgy.province_id = %s AND eventbrgy.citymun_id = %s AND eventbrgy.brgy_id = %s;
        """
        values = [region, province, citymun, brgy]
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        events = df.to_dict('records')
        dropdowns.append(events)

        # Barangays
        sql = """SELECT name AS label, id AS value
        FROM utilities.addressbrgy
        WHERE region_id = %s AND province_id = %s AND citymun_id = %s;
        """
        values = [region, province, citymun]
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        brgys = df.to_dict('records')
        dropdowns.append(brgys)

        if brgy:
            dropdowns.append(True)
            dropdowns.append(brgy)
        else:
            dropdowns.append(False)
            dropdowns.append(None)

        # Related incident types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.relinctype;
        """
        values = []
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

        # Public utility types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') as label, id as value
        FROM utilities.pubutiltype;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        pubutiltypes = df.to_dict('records')
        dropdowns.append(pubutiltypes)

        # Public utility interruption types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') as label, id as value, desc_war, desc_en
        FROM utilities.pubutilinttype;
        """
        values = []
        cols = ['label', 'value', 'desc_war', 'desc_en']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        pubutilinttypes = df[['label', 'value']].to_dict('records')
        dropdowns.append(pubutilinttypes)

        pubutilinttype_list = []
        pubutilinttypes = df.to_dict('records')
        for i in pubutilinttypes:
            pubutilinttype_list.append(
                html.Li(
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
                    className = 'mb-1'
                )
            )

        pubutilinttype_desc = dbc.Alert(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.I(className = 'bi bi-exclamation-circle-fill me-2'),
                            class_name = alert_i_m
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        "Maupay hinumduman an karuyag signgon sini nga mga klase san pag-úndang", html.Br(),
                                        html.Small("(It would be helpful to remember the following definitions for interruption/outage type):", className = 'text-muted')
                                    ],
                                    className = 'mb-2'
                                ),
                                html.Div(pubutilinttype_list)
                            ]
                        )
                    ]
                ),
            ],
            color = 'info',
            class_name = row_m,
            dismissable = True
        )
        dropdowns.append(pubutilinttype_desc)

        # Damaged house types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') as label, id as value, desc_war, desc_en
        FROM utilities.dmgdinfratype;
        """
        values = []
        cols = ['label', 'value', 'desc_war', 'desc_en']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        dmgdinfratypes = df[['label', 'value']].to_dict('records')
        dropdowns.append(dmgdinfratypes)
        dropdowns.append(dmgdinfratypes)

        dmgdhousetype_list = []
        dmgdhousetypes = df.to_dict('records')
        for i in dmgdhousetypes:
            dmgdhousetype_list.append(
                html.Li(
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
                    className = 'mb-1'
                )
            )

        dmgdhousetype_desc = dbc.Alert(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.I(className = 'bi bi-exclamation-circle-fill me-2'),
                            class_name = alert_i_m
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        "Maupay hinumduman an karuyag signgon sini nga mga klase san pagkarubat san balay", html.Br(),
                                        html.Small("(It would be helpful to remember the following definitions for damaged house types):", className = 'text-muted')
                                    ],
                                    className = 'mb-2'
                                ),
                                html.Div(dmgdhousetype_list),
                                html.Div(
                                    [
                                        "Ginkuhaan sini nga mga depinisyon: ", html.A("Memorandum Circular No. 6, s. 2019 san DSWD", href = 'https://www.dswd.gov.ph/issuances/MCs/MC_2019-006.pdf', style = hyperlink_style), html.Br(),
                                        html.Small(["(Source of definitions: ", html.A("Memorandum Circular No. 6, s. 2019 san DSWD", href = 'https://www.dswd.gov.ph/issuances/MCs/MC_2019-006.pdf', style = hyperlink_style), ")"], className = 'text-muted')
                                    ],
                                    className = 'mb-2'
                                ),
                            ]
                        )
                    ]
                ),
            ],
            color = 'info',
            class_name = row_m,
            dismissable = True
        )
        dropdowns.append(dmgdhousetype_desc)

        # Infrastructure types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') as label, id as value, desc_war, desc_en
        FROM utilities.infratype;
        """
        values = []
        cols = ['label', 'value', 'desc_war', 'desc_en']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        infratypes = df[['label', 'value']].to_dict('records')
        dropdowns.append(infratypes)

        # Infrastructure classes
        sql = """SELECT CONCAT(label_war, ' (', label_en, ')') as label, id as value
        FROM utilities.infraclass;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        infraclasses = df.to_dict('records')
        dropdowns.append(infraclasses)

        # Infrastructure quantity units
        sql = """SELECT CONCAT(label_war, ' (', label_en, ')') as label, id as value
        FROM utilities.qtyunit;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        infraclasses = df.to_dict('records')
        dropdowns.append(infraclasses)
        dropdowns.append(1)

        return dropdowns
    else: raise PreventUpdate

# Callback for showing report forms based on type
@app.callback(
    [
        Output('rep_cre_div_submit', 'style'),
        Output('rep_cre_div_relinc', 'style'),
        Output('rep_cre_div_casualty', 'style'),
        Output('rep_cre_div_pubutil', 'style'),
        Output('rep_cre_div_dmgdhouse', 'style'),
        Output('rep_cre_div_dmgdinfra', 'style')
    ],
    [
        Input('rep_cre_input_brgy_id', 'value'),
        Input('rep_cre_input_event_id', 'value'),
        Input('rep_cre_input_reporttype_id', 'value'),
        Input('rep_cre_input_purok', 'value'),
        Input('rep_cre_input_date', 'date'),
    ]
)

def rep_cre_showreportform(brgy, event, type, purok, date):
    conditions = [brgy, event, type, purok, date]
    disp_none = {'display' : 'none'}
    disp_show = {'display' : 'block'}
    style_submit = disp_none
    style_relinc = disp_none
    style_casualty = disp_none
    style_pubutil = disp_none
    style_dmgdhouse = disp_none
    style_dmgdinfra = disp_none
    if all(conditions):
        style_submit = disp_show
        if type == 1: style_relinc = disp_show
        elif type == 2: style_casualty = disp_show
        elif type == 3: style_pubutil = disp_show
        elif type == 4: style_dmgdhouse = disp_show
        elif type == 5: style_dmgdinfra = disp_show
    return [style_submit, style_relinc, style_casualty, style_pubutil, style_dmgdhouse, style_dmgdinfra]

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

def rep_cre_populateprovinces(region):
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

def rep_cre_populatecitymuns(region, province):
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

def rep_cre_populatebrgys(region, province, citymun):
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

def rep_cre_enablestreet(region, province, citymun, brgy):
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
    value = None
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
            if df.shape[0] == 1:
                value = df['value'][0]
                disabled = True
            else:
                value = None
                disabled = False
        else:
            options = df.to_dict('records')
            value = None
            disabled = True
    return [options, value, disabled]

# Callback for populating local public utility once utility type is selected
@app.callback(
    [
        Output('rep_cre_input_pubutil_id', 'options'),
        Output('rep_cre_input_pubutil_id', 'value'),
        Output('rep_cre_input_pubutil_id', 'disabled'),
    ],
    [
        Input('rep_cre_input_pubutiltype_id', 'value')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data')
    ],
    prevent_initial_update = True
)

def rep_cre_setpubutil(pubutiltype, region, province, citymun, brgy):
    options = None
    value = None
    disabled = True
    if pubutiltype:
        pubutiltype = int(pubutiltype)
        sql = """SELECT CONCAT(acronym, ' (', name, ')') AS label, id AS value
            FROM utilities.pubutil WHERE type_id = %s;"""
        values = [pubutiltype]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        options = df.to_dict('records')
        if pubutiltype == 1 or pubutiltype == 2:
            if pubutiltype == 1:
                sql = """SELECT pubutil_elec_id AS pubutil_id FROM utilities.addressbrgy
                    WHERE region_id = %s AND province_id = %s AND citymun_id = %s AND id = %s;"""
            else:
                sql = """SELECT pubutil_water_id AS pubutil_id FROM utilities.addressbrgy
                    WHERE region_id = %s AND province_id = %s AND citymun_id = %s AND id = %s;"""
            values = [region, province, citymun, brgy]
            cols = ['pubutil_id']
            df = db.querydatafromdatabase(sql, values, cols)
            value = df.at[0, 'pubutil_id']
        else:
            disabled = False
    return [options, value, disabled]

# Callback for setting common date/time as utility interruption date/time
@app.callback(
    [
        Output('rep_cre_input_pubutilint_int_date', 'date'),
        Output('rep_cre_input_pubutilint_int_time_hh', 'value'),
        Output('rep_cre_input_pubutilint_int_time_mm', 'value'),
        Output('rep_cre_input_pubutilint_int_time_ss', 'value'),
        Output('rep_cre_input_pubutilint_int_time_ampm', 'value')
    ],
    [
        Input('rep_cre_input_date', 'date'),
        Input('rep_cre_input_time_hh', 'value'),
        Input('rep_cre_input_time_mm', 'value'),
        Input('rep_cre_input_time_ss', 'value'),
        Input('rep_cre_input_time_ampm', 'value')
    ]
)

def rep_cre_setpubutilintdatetime(date, hh, mm, ss, ampm):
    return[date, hh, mm, ss, ampm]

# Callback for confirming report creation
@app.callback(
    [
        # Modal
        Output('rep_cre_modal_confirm', 'is_open'),
        # Overall validation alert
        Output('rep_cre_alert_inputvalidation', 'is_open'),
        Output('rep_cre_alert_inputvalidation', 'class_name'),
        Output('rep_cre_alert_inputvalidation_span_missing', 'children'),
        # Report type 1 (Related incident) input validation
        Output('rep_cre_input_relinctype_id', 'invalid'),
        Output('rep_cre_input_relinc_qty', 'invalid'),
        Output('rep_cre_input_relincstatus_id', 'invalid'),
        # Report type 2 (Casualty) input validation
        Output('rep_cre_input_casualtytype_id', 'invalid'),
        Output('rep_cre_input_casualty_fname', 'invalid'),
        Output('rep_cre_input_casualty_lname', 'invalid'),
        Output('rep_cre_input_casualty_age', 'invalid'),
        Output('rep_cre_input_casualty_assignedsex_id', 'invalid'),
        Output('rep_cre_input_casualty_infosource', 'invalid'),
        Output('rep_cre_input_casualtystatus_id', 'invalid'),
        # Report type 3 (Public utility status) input validation
        Output('rep_cre_input_pubutiltype_id', 'invalid'),
        Output('rep_cre_input_pubutil_id', 'invalid'),
        Output('rep_cre_input_pubutilinttype_id', 'invalid'),
        # Report type 4 (Damaged house) input validation
        Output('rep_cre_input_dmgdhousetype_id', 'invalid'),
        Output('rep_cre_input_dmgdhouse_fname', 'invalid'),
        Output('rep_cre_input_dmgdhouse_lname', 'invalid'),
        Output('rep_cre_input_dmgdhouse_age', 'invalid'),
        Output('rep_cre_input_dmgdhouse_assignedsex_id', 'invalid'),
        Output('rep_cre_input_dmgdhouse_loc', 'invalid'),
        # Report type 5 (Damaged infrastructure) input validation
        Output('rep_cre_input_infratype_id', 'invalid'),
        Output('rep_cre_input_infraclass_id', 'invalid'),
        Output('rep_cre_input_dmgdinfra_description', 'invalid'),
        Output('rep_cre_input_dmgdinfra_qty', 'invalid'),
        Output('rep_cre_input_dmgdinfra_qtyunit_id', 'invalid'),
        Output('rep_cre_label_dmgdinfratype_id', 'invalid'),
    ],
    [
        Input('rep_cre_btn_submit', 'n_clicks')
    ],
    [
        # Common information
        State('rep_cre_input_brgy_id', 'value'),
        State('rep_cre_input_event_id', 'value'),
        State('rep_cre_input_reporttype_id', 'value'),
        State('rep_cre_input_purok', 'value'),
        State('rep_cre_input_date', 'date'),
            # OPTIONAL
            #State('rep_cre_input_time_hh', 'value'),
            #State('rep_cre_input_time_mm', 'value'),
            #State('rep_cre_input_time_ss', 'value'),
            #State('rep_cre_input_time_ampm', 'value'),
            #State('rep_cre_input_remarks', 'value'),
        # Report type 1: Related incidents
        State('rep_cre_input_relinctype_id', 'value'),
        State('rep_cre_input_relinc_qty', 'value'),
        State('rep_cre_input_relincstatus_id', 'value'),
            # OPTIONAL
            #State('rep_cre_input_relinc_description', 'value'),
            #State('rep_cre_input_relinc_actions', 'value'),
        # Report type 2: Casualty
        State('rep_cre_input_casualtytype_id', 'value'),
        State('rep_cre_input_casualty_fname', 'value'),
        State('rep_cre_input_casualty_lname', 'value'),
        State('rep_cre_input_casualty_age', 'value'),
        State('rep_cre_input_casualty_assignedsex_id', 'value'),
        State('rep_cre_input_casualty_infosource', 'value'),
        State('rep_cre_input_casualtystatus_id', 'value'),
            # OPTIONAL
            #State('rep_cre_input_casualty_mname', 'value'),
            #State('rep_cre_input_casualty_region_id', 'value'),
            #State('rep_cre_input_casualty_province_id', 'value'),
            #State('rep_cre_input_casualty_citymun_id', 'value'),
            #State('rep_cre_input_casualty_brgy_id', 'value'),
            #State('rep_cre_input_casualty_street', 'value'),
            #State('rep_cre_input_casualty_cause', 'value'),
        # Report type 3: Public utility status
        State('rep_cre_input_pubutiltype_id', 'value'), # Not needed in database
        State('rep_cre_input_pubutil_id', 'value'),
        State('rep_cre_input_pubutilinttype_id', 'value'),
            # OPTIONAL
            #State('rep_cre_input_pubutilint_res_date', 'date'),
            #State('rep_cre_input_pubutilint_res_time_hh', 'value'),
            #State('rep_cre_input_pubutilint_res_time_mm', 'value'),
            #State('rep_cre_input_pubutilint_res_time_ss', 'value'),
            #State('rep_cre_input_pubutilint_res_time_ampm', 'value'),
        # Report type 4: Damaged house
        State('rep_cre_input_dmgdhousetype_id', 'value'),
        State('rep_cre_input_dmgdhouse_fname', 'value'),
        State('rep_cre_input_dmgdhouse_lname', 'value'),
        State('rep_cre_input_dmgdhouse_age', 'value'),
        State('rep_cre_input_dmgdhouse_assignedsex_id', 'value'),
        State('rep_cre_input_dmgdhouse_loc', 'value'),
            # OPTIONAL
            #State('rep_cre_input_dmgdhouse_mname', 'value'),
            #State('rep_cre_input_selectgps', 'value'),
        # Report type 5: Damaged infrastructure
        State('rep_cre_input_infratype_id', 'value'),
        State('rep_cre_input_infraclass_id', 'value'),
        State('rep_cre_input_dmgdinfra_description', 'value'),
        State('rep_cre_input_dmgdinfra_qty', 'value'),
        State('rep_cre_input_dmgdinfra_qtyunit_id', 'value'),
        State('rep_cre_label_dmgdinfratype_id', 'value'),
            # OPTIONAL
            #State('rep_cre_input_dmgdinfra_cost', 'value'),
    ]
)

def rep_cre_confirmcreation(
    btn,

    # Common information
    brgy, event, type, purok, date,
        # OPTIONAL, no need for input validation
        #hh, mm, ss, ampm, remarks,
    
    # Report type 1: Related incidents
    relinc_type, relinc_qty, relinc_status,
        # OPTIONAL, no need for input validation
        #relinc_description, relinc_actions,
    
    # Report type 2: Casualty
    casualty_type, casualty_fname, casualty_lname,
    casualty_age, casualty_assignedsex,
    casualty_infosource, casualty_status,
        # OPTIONAL, no need for input validation
        #casualty_mname, casualty_region, casualty_province, casualty_citymun, casualty_brgy, casualty_street,
        #casualty_cause,
    
    # Report type 3: Public utility status
    pubutiltype, pubutil_id, pubutilint_type,
        # OPTIONAL
        #pubutilres_date, pubutilres_time_hh, pubutilres_time_mm, pubutilres_time_ss, pubutilres_time_ampm,
    
    # Report type 4: Damaged house
    dmgdhouse_type, dmgdhouse_fname, dmgdhouse_lname,
    dmgdhouse_age, dmgdhouse_assignedsex,
    dmgdhouse_loc,
        # OPTIONAL
        #dmgdhouse_mname, dmgdhouse_selectgps,
    
    # Report type 5: Damaged infrastructure
    infratype, infraclass, dmgdinfra_description, dmgdinfra_qty, dmgdinfra_qtyunit,
    dmgdinfra_type,
        # OPTIONAL
        #dmgdinfra_cost,
):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'rep_cre_btn_submit' and btn:
            # Modal
            modal_open = False
            # Overall validation alert
            alert_open = False
            alert_class_name = None
            alert_span = []
            # Report type 1 (Related incident) input validation
            relinc_type_invalid = False
            relinc_qty_invalid = False
            relinc_status_invalid = False
            # Report type 2 (Casualty) input validation
            casualty_type_invalid = False
            casualty_fname_invalid = False
            casualty_lname_invalid = False
            casualty_age_invalid = False
            casualty_assignedsex_invalid = False
            casualty_infosource_invalid = False
            casualty_status_invalid = False
            # Report type 3 (Public utility status) input validation
            pubutiltype_invalid = False
            pubutil_id_invalid = False
            pubutilint_type_invalid = False
            # Report type 4 (Damaged house) input validation
            dmgdhouse_type_invalid = False
            dmgdhouse_fname_invalid = False
            dmgdhouse_lname_invalid = False
            dmgdhouse_age_invalid = False
            dmgdhouse_assignedsex_invalid = False
            dmgdhouse_loc_invalid = False
            # Report type 5 (Damaged infrastructure) input validation
            infratype_invalid = False
            infraclass_invalid = False
            dmgdinfra_description_invalid = False
            dmgdinfra_qty_invalid = False
            dmgdinfra_qtyunit_invalid = False
            dmgdinfra_type_invalid = False

            if (not(brgy) or not(event) or not(type) or not (purok) or not (date)):
                alert_open = True
                alert_class_name = 'mb-3'
                if not(brgy):
                    # Add input validation here
                    alert_span.append(
                        html.Li(
                            [
                                "Barangay"#, html.Br(),
                                #html.Small(" (Event type)", className = 'ms-3 text-muted'),
                            ]
                        )
                    )
                if not(event):
                    # Add input validation here
                    alert_span.append(
                        html.Li(
                            [
                                "Panhitabó", html.Br(),
                                html.Small(" (Event)", className = 'ms-3 text-muted'),
                            ]
                        )
                    )
                if not(type):
                    # Add input validation here
                    alert_span.append(
                        html.Li(
                            [
                                "Klase san report", html.Br(),
                                html.Small(" (Report type)", className = 'ms-3 text-muted'),
                            ]
                        )
                    )
                if not(date):
                    # Add input validation here
                    alert_span.append(
                        html.Li(
                            [
                                "Petsa san panhitabó", html.Br(),
                                html.Small(" (Date of occurrence)", className = 'ms-3 text-muted'),
                            ]
                        )
                    )
            else:
                if type == 1:
                    conditions = [not(relinc_type), not(relinc_qty), not(relinc_status)]
                    if (any(conditions)):
                        alert_open = True
                        alert_class_name = 'mb-3'
                        if not(relinc_type):
                            relinc_type_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Klase san insidente", html.Br(),
                                        html.Small(" (Type of incident)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(relinc_qty):
                            relinc_qty_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Kantidad san insidente", html.Br(),
                                        html.Small(" (Quantity of incident)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(relinc_status):
                            relinc_status_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Kamutangan san insidente", html.Br(),
                                        html.Small(" (Status)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                    else: modal_open = True
                elif type == 2:
                    conditions = [
                        not(casualty_type), not(casualty_fname), not(casualty_lname),
                        not(casualty_age), not(casualty_assignedsex),
                        not(casualty_infosource), not(casualty_status)
                    ]
                    if (any(conditions)):
                        alert_open = True
                        alert_class_name = 'mb-3'
                        if not(casualty_type):
                            casualty_type_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Klase san disgrasiya", html.Br(),
                                        html.Small(" (Type of casualty)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(casualty_fname):
                            casualty_fname_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Primero nga ngaran san disgrasiya", html.Br(),
                                        html.Small(" (First name of victim)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(casualty_lname):
                            casualty_lname_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Apelyido san disgrasiya", html.Br(),
                                        html.Small(" (Last name of victim)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(casualty_age):
                            casualty_age_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Edad san disgrasiya", html.Br(),
                                        html.Small(" (Age of victim)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(casualty_assignedsex):
                            casualty_assignedsex_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Kun natawo nga babayi/lalaki an disgrasiya", html.Br(),
                                        html.Small(" (Sex assigned at birth of victim)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(casualty_infosource):
                            casualty_infosource_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Ginkuhaan san impormasyon", html.Br(),
                                        html.Small(" (Source of data)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(casualty_status):
                            casualty_status_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Kamutangan san pagprubar", html.Br(),
                                        html.Small(" (Validation status)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                    else: modal_open = True
                elif type == 3:
                    conditions = [not(pubutiltype), not(pubutil_id), not(pubutilint_type)]
                    if (any(conditions)):
                        alert_open = True
                        alert_class_name = 'mb-3'
                        if not(pubutiltype):
                            pubutiltype_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Klase san utilidad", html.Br(),
                                        html.Small(" (Validation status)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(pubutil_id):
                            pubutil_id_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Naghahatag san serbisyo", html.Br(),
                                        html.Small(" (Service provider)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(pubutilint_type):
                            pubutilint_type_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Klase san pag-úndang", html.Br(),
                                        html.Small(" (Type of interruption/outage)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                    else: modal_open = True
                elif type == 4:
                    conditions = [
                        not(dmgdhouse_type), not(dmgdhouse_fname), not(dmgdhouse_lname),
                        not(dmgdhouse_age), not(dmgdhouse_assignedsex),
                        not(dmgdhouse_loc)
                    ]
                    if(any(conditions)):
                        alert_open = True
                        alert_class_name = 'mb-3'
                        if not(dmgdhouse_type):
                            dmgdhouse_type_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Klase san pagkarubat", html.Br(),
                                        html.Small(" (Type of damage)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(dmgdhouse_fname):
                            dmgdhouse_fname_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Primero nga ngaran san tag-iya san balay", html.Br(),
                                        html.Small(" (First name of homeowner)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(dmgdhouse_lname):
                            dmgdhouse_lname_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Apelyido san tag-iya san balay", html.Br(),
                                        html.Small(" (Last name of homeowner)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(dmgdhouse_age):
                            dmgdhouse_age_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Edad san tag-iya san balay", html.Br(),
                                        html.Small(" (Age of homeowner)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(dmgdhouse_assignedsex):
                            dmgdhouse_assignedsex_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Kun natawo nga babayi/lalaki an tag-iya san balay", html.Br(),
                                        html.Small(" (Sex assigned at birth of homeowner)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(dmgdhouse_loc):
                            dmgdhouse_loc_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Lokasiyon san balay", html.Br(),
                                        html.Small(" (Location of home)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                    else: modal_open = True
                elif type == 5:
                    conditions = [
                        not(infratype), not(infraclass), not(dmgdinfra_description),
                        not(dmgdinfra_qty), not(dmgdinfra_qtyunit),
                        not(dmgdinfra_type)
                    ]
                    if(any(conditions)):
                        alert_open = True
                        alert_class_name = 'mb-3'
                        if not(infratype):
                            infratype_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Tipo san imprastruktura", html.Br(),
                                        html.Small(" (Infrastructure type)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(infraclass):
                            infraclass_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Klase", html.Br(),
                                        html.Small(" (Classification)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(dmgdinfra_description):
                            dmgdinfra_description_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Ngaran/deskripsiyon", html.Br(),
                                        html.Small(" (Name/description)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(dmgdinfra_qty):
                            dmgdinfra_qty_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Kantidad san narubat", html.Br(),
                                        html.Small(" (Quantity of damage)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(dmgdinfra_qtyunit):
                            dmgdinfra_qtyunit_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Pag-ihap san kantidad", html.Br(),
                                        html.Small(" (Units of quantity)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                        if not(dmgdinfra_type):
                            dmgdinfra_type_invalid = True
                            alert_span.append(
                                html.Li(
                                    [
                                        "Kamutangan", html.Br(),
                                        html.Small(" (Status)", className = 'ms-3 text-muted'),
                                    ]
                                )
                            )
                    else: modal_open = True
            return [
                # Modal
                modal_open,
                # Overall validation alert
                alert_open, alert_class_name, alert_span,
                # Report type 1 (Related incident) input validation
                relinc_type_invalid, relinc_qty_invalid, relinc_status_invalid,
                # Report type 2 (Casualty) input validation
                casualty_type_invalid, casualty_fname_invalid, casualty_lname_invalid,
                casualty_age_invalid, casualty_assignedsex_invalid,
                casualty_infosource_invalid, casualty_status_invalid,
                # Report type 3 (Public utility status) input validation
                pubutiltype_invalid, pubutil_id_invalid, pubutilint_type_invalid,
                # Report type 4 (Damaged house) input validation
                dmgdhouse_type_invalid, dmgdhouse_fname_invalid, dmgdhouse_lname_invalid,
                dmgdhouse_age_invalid, dmgdhouse_assignedsex_invalid, dmgdhouse_loc_invalid,
                # Report type 5 (Damaged infrastructure) input validation
                infratype_invalid, infraclass_invalid, dmgdinfra_description_invalid,
                dmgdinfra_qty_invalid, dmgdinfra_qtyunit_invalid, dmgdinfra_type_invalid,
            ]
        else: raise PreventUpdate
    else: raise PreventUpdate

# Callback for creating a new report
@app.callback(
    [
        # Alert
        Output('rep_cre_alert_passwordvalidation', 'is_open'),
        Output('rep_cre_alert_passwordvalidation', 'class_name'),
        Output('rep_cre_alert_passwordvalidation', 'color'),
        Output('rep_cre_alert_passwordvalidation_col_text', 'children'),
        # Input validation
        Output('rep_cre_input_password', 'invalid'),
        Output('rep_cre_input_password', 'valid'),
        # New report and version id
        Output('rep_cre_newreport_id', 'data'),
        Output('rep_cre_newversion_id', 'data')
    ],
    [
        Input('rep_cre_btn_confirm', 'n_clicks')
    ],
    [
        # Password
        State('rep_cre_input_password', 'value'),
        # User details
        State('app_currentuser_id', 'data'),
        # App geolock details
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        # Common information
        State('rep_cre_input_brgy_id', 'value'),
        State('rep_cre_input_event_id', 'value'),
        State('rep_cre_input_reporttype_id', 'value'),
        State('rep_cre_input_purok', 'value'),
        State('rep_cre_input_date', 'date'),
            # OPTIONAL
            State('rep_cre_input_time_hh', 'value'),
            State('rep_cre_input_time_mm', 'value'),
            State('rep_cre_input_time_ss', 'value'),
            State('rep_cre_input_time_ampm', 'value'),
            State('rep_cre_input_remarks', 'value'),
        # Report type 1: Related incidents
        State('rep_cre_input_relinctype_id', 'value'),
        State('rep_cre_input_relinc_qty', 'value'),
        State('rep_cre_input_relincstatus_id', 'value'),
            # OPTIONAL
            State('rep_cre_input_relinc_description', 'value'),
            State('rep_cre_input_relinc_actions', 'value'),
        # Report type 2: Casualty
        State('rep_cre_input_casualtytype_id', 'value'),
        State('rep_cre_input_casualty_fname', 'value'),
        State('rep_cre_input_casualty_lname', 'value'),
        State('rep_cre_input_casualty_age', 'value'),
        State('rep_cre_input_casualty_assignedsex_id', 'value'),
        State('rep_cre_input_casualty_infosource', 'value'),
        State('rep_cre_input_casualtystatus_id', 'value'),
            # OPTIONAL
            State('rep_cre_input_casualty_mname', 'value'),
            State('rep_cre_input_casualty_region_id', 'value'),
            State('rep_cre_input_casualty_province_id', 'value'),
            State('rep_cre_input_casualty_citymun_id', 'value'),
            State('rep_cre_input_casualty_brgy_id', 'value'),
            State('rep_cre_input_casualty_street', 'value'),
            State('rep_cre_input_casualty_cause', 'value'),
        # Report type 3: Public utility status
        #State('rep_cre_input_pubutiltype_id', 'value'), # Not needed in database
        State('rep_cre_input_pubutil_id', 'value'),
        State('rep_cre_input_pubutilinttype_id', 'value'),
            # OPTIONAL
            State('rep_cre_input_pubutilint_res_date', 'date'),
            State('rep_cre_input_pubutilint_res_time_hh', 'value'),
            State('rep_cre_input_pubutilint_res_time_mm', 'value'),
            State('rep_cre_input_pubutilint_res_time_ss', 'value'),
            State('rep_cre_input_pubutilint_res_time_ampm', 'value'),
        # Report type 4: Damaged house
        State('rep_cre_input_dmgdhousetype_id', 'value'),
        State('rep_cre_input_dmgdhouse_fname', 'value'),
        State('rep_cre_input_dmgdhouse_lname', 'value'),
        State('rep_cre_input_dmgdhouse_age', 'value'),
        State('rep_cre_input_dmgdhouse_assignedsex_id', 'value'),
        State('rep_cre_input_dmgdhouse_loc', 'value'),
            # OPTIONAL
            State('rep_cre_input_dmgdhouse_mname', 'value'),
            State('rep_cre_input_selectgps', 'value'),
            State('rep_cre_geoloc', 'position'),
        # Report type 5: Damaged infrastructure
        State('rep_cre_input_infratype_id', 'value'),
        State('rep_cre_input_infraclass_id', 'value'),
        State('rep_cre_input_dmgdinfra_description', 'value'),
        State('rep_cre_input_dmgdinfra_qty', 'value'),
        State('rep_cre_input_dmgdinfra_qtyunit_id', 'value'),
        State('rep_cre_label_dmgdinfratype_id', 'value'),
            # OPTIONAL
            State('rep_cre_input_dmgdinfra_cost', 'value'),
    ]
)

def rep_cre_submitcreation(
    btn, password,
    user_id, region_id, province_id, citymun_id,

    # Common information
    brgy_id, event, type, purok, date,
        # OPTIONAL
        hh, mm, ss, ampm, remarks,
    
    # Report type 1: Related incidents
    relinc_type, relinc_qty, relinc_status,
        # OPTIONAL
        relinc_description, relinc_actions,
    
    # Report type 2: Casualty
    casualty_type, casualty_fname, casualty_lname,
    casualty_age, casualty_assignedsex,
    casualty_infosource, casualty_status,
        # OPTIONAL, no need for input validation
        casualty_mname, casualty_region, casualty_province, casualty_citymun, casualty_brgy, casualty_street,
        casualty_cause,
    
    # Report type 3: Public utility status
    #pubutiltype, # Not needed
    pubutil_id, pubutilint_type,
        # OPTIONAL
        pubutilres_date, pubutilres_time_hh, pubutilres_time_mm, pubutilres_time_ss, pubutilres_time_ampm,
    
    # Report type 4: Damaged house
    dmgdhouse_type, dmgdhouse_fname, dmgdhouse_lname,
    dmgdhouse_age, dmgdhouse_assignedsex,
    dmgdhouse_loc,
        # OPTIONAL
        dmgdhouse_mname, dmgdhouse_selectgps, geoloc_pos,
    
    # Report type 5: Damaged infrastructure
    infratype, infraclass, dmgdinfra_description, dmgdinfra_qty, dmgdinfra_qtyunit,
    dmgdinfra_type,
        # OPTIONAL
        dmgdinfra_cost,
):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'rep_cre_btn_confirm' and btn:
            # Alert
            alert_open = False
            alert_class_name = None
            alert_color = None
            alert_col_text = None
            # Password validation
            password_invalid = False
            password_valid = False
            # New report id
            newreport_id = 1
            newversion_id = 1

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
                    # Get index of latest report for this event (not overall index or report serial number)
                    event_report_id = 1
                    sql = """SELECT event_report_id FROM reports.report WHERE event_id = %s ORDER BY id DESC LIMIT 1;"""
                    values = [event]
                    cols = ['event_report_id']
                    df = db.querydatafromdatabase(sql, values, cols)
                    if df.shape[0] > 0: event_report_id = int(df['event_report_id'][0]) + 1

                    # Actual report creation
                    sql = """INSERT INTO reports.report(event_id, event_report_id,
                    region_id, province_id, citymun_id, brgy_id,
                    type_id, purok)
                    VALUES(%s, %s,
                    %s, %s, %s, %s,
                    %s, %s);"""
                    values = [event, event_report_id, region_id, province_id, citymun_id, brgy_id, type, purok]
                    db.modifydatabase(sql, values)

                    # Get index of latest report
                    sql = """SELECT id FROM reports.report ORDER BY id DESC LIMIT 1;"""
                    values = []
                    cols = ['id']
                    newreport_id = int(db.querydatafromdatabase(sql, values, cols)['id'][0])

                    # Setting up time
                    time = None
                    if hh and mm and ss and ampm:
                        if hh == 12:
                            hh = 0
                        if ampm == 'PM':
                            hh += 12
                        time = '{:02d}'.format(hh) + '{:02d}'.format(mm) + '{:02d}'.format(ss) + '+08'

                    # Get index of latest report version
                    sql = """SELECT id FROM reports.reportversion WHERE report_id = %s ORDER BY id DESC LIMIT 1;"""
                    values = [newreport_id]
                    cols = ['id']
                    df = db.querydatafromdatabase(sql, values, cols)
                    if df.shape[0] > 0: newversion_id = int(df['id'][0]) + 1

                    # New version creation
                    sql = """INSERT INTO reports.reportversion(id, report_id, occurrence_date, occurrence_time,
                    remarks, creator_id) VALUES(%s, %s, %s, %s, %s, %s)"""
                    values = [newversion_id, newreport_id, date, time, remarks, user_id]
                    db.modifydatabase(sql, values)

                    # Creation of report-type specific table rows
                    if type == 1:
                        sql = """INSERT INTO reports.relinc(report_id, version_id,
                        type_id, qty, description, actions_taken, status_id)
                        VALUES(%s, %s, %s, %s, %s, %s, %s);"""
                        values = [
                            newreport_id, newversion_id,
                            relinc_type, relinc_qty, relinc_description, relinc_actions, relinc_status
                        ]
                        db.modifydatabase(sql, values)
                    elif type == 2:
                        sql = """INSERT INTO reports.casualty(report_id, version_id,
                        type_id, fname, mname, lname, age, assignedsex_id,
                        region_id, province_id, citymun_id, brgy_id, street,
                        cause, infosource, status_id)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                        values = [
                            newreport_id, newversion_id,
                            casualty_type, casualty_fname, casualty_mname, casualty_lname, casualty_age, casualty_assignedsex,
                            casualty_region, casualty_province, casualty_citymun, casualty_brgy, casualty_street,
                            casualty_cause, casualty_infosource, casualty_status
                        ]
                        db.modifydatabase(sql, values)
                    elif type == 3:
                        # Setting up restoration time
                        pubutilres_time = None
                        if pubutilres_time_hh and pubutilres_time_mm and pubutilres_time_ss and pubutilres_time_ampm:
                            if pubutilres_time_hh == 12:
                                pubutilres_time_hh = 0
                            if pubutilres_time_ampm == 'PM':
                                pubutilres_time_hh += 12
                            pubutilres_time = '{:02d}'.format(pubutilres_time_hh) + '{:02d}'.format(pubutilres_time_mm) + '{:02d}'.format(pubutilres_time_ss) + '+08'
                        sql = """INSERT INTO reports.pubutilint(report_id, version_id,
                        pubutil_id, inttype_id, int_date, int_time, res_date, res_time)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""
                        values = [
                            newreport_id, newversion_id,
                            pubutil_id, pubutilint_type, date, time, pubutilres_date, pubutilres_time
                        ]
                        db.modifydatabase(sql, values)
                    elif type == 4:
                        dmgdhouse_loc_gps = None
                        if dmgdhouse_selectgps:
                            dmgdhouse_loc_gps = (geoloc_pos['lat'], geoloc_pos['lon'])
                        sql = """INSERT INTO reports.dmgdhouse(report_id, version_id,
                        type_id, fname, mname, lname, age, assignedsex_id,
                        loc_text, loc_gps)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                        values = [
                            newreport_id, newversion_id,
                            dmgdhouse_type, dmgdhouse_fname, dmgdhouse_mname, dmgdhouse_lname, dmgdhouse_age, dmgdhouse_assignedsex,
                            dmgdhouse_loc, dmgdhouse_loc_gps
                        ]
                        db.modifydatabase(sql, values)
                    elif type == 5:
                        sql = """INSERT INTO reports.dmgdinfra(report_id, version_id,
                        infatype_id, infraclass_id, infraname,
                        qty, qtyunit_id, infracost,
                        dmgtype_id)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                        values = [
                            newreport_id, newversion_id,
                            infratype, infraclass, dmgdinfra_description,
                            dmgdinfra_qty, dmgdinfra_qtyunit, dmgdinfra_cost,
                            dmgdinfra_type
                        ]
                        db.modifydatabase(sql, values)

                    alert_open = True
                    alert_class_name = 'mb-3'
                    alert_color = 'success'
                    password_valid = True
                    alert_col_text = [
                        "Nahimo na an report.",
                        html.Br(),
                        html.Small(
                            "(Report submitted.)",
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
            return [
                alert_open, alert_class_name, alert_color, alert_col_text,
                password_invalid, password_valid,
                newreport_id, newversion_id
            ]
        else: raise PreventUpdate
    else: raise PreventUpdate