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
                                                    value = 1,
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
                                                    "Iba pa nga komento", html.Br(),
                                                    html.Small(" (Remarks)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_remarks',
                                                class_name = label_m
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
                                    ], class_name = row_m
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
                                                class_name = label_m
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
                                                #    class_name = ftext_m
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = row_m,
                                ),
                            ],
                            id = 'rep_cre_div_relinc',
                            className = div_m,
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
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_casualtytype_id',
                                                    clearable = True,
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
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_casualty_assignedsex_id',
                                                    clearable = True
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
                                                    "Iba pa nga komento", html.Br(),
                                                    html.Small(" (Remarks)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualty_remarks',
                                                class_name = label_m
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
                                    ], class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Ginkuhaan san impormasyon", html.Br(),
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
                                                    id = 'rep_cre_input_casualty_source',
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
                                                    "Estado san pagprubar", tag_required, html.Br(),
                                                    html.Small(" (Validation status)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_casualtystatus_id',
                                                class_name = label_m
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
                                                #    class_name = ftext_m
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                        ),
                                    ], class_name = row_m,
                                ),
                            ],
                            id = 'rep_cre_div_casualty',
                            className = div_m,
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
                                                        "Kabutangan san panpubliko nga utilidad",
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
                                                    "Petsa san pag-undang", html.Br(),
                                                    html.Small(" (Date of interruption/outage)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_pubutilint_intdate',
                                                class_name = label_m
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
                                                id = 'rep_cre_label_pubutilint_inttime',
                                                class_name = label_m
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
                                                            invalid = False,
                                                            disabled = True
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            id = 'rep_cre_input_pubutilint_inttime_mm',
                                                            placeholder = 'MM',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False,
                                                            disabled = True
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            id = 'rep_cre_input_pubutilint_inttime_ss',
                                                            placeholder = 'SS',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False,
                                                            disabled = True
                                                        ),
                                                        dbc.Select(
                                                            id = 'rep_cre_input_pubutilint_inttime_ampm',
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
                                                id = 'rep_cre_label_pubutilint_resdate',
                                                class_name = label_m
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
                                                id = 'rep_cre_label_pubutilint_restime',
                                                class_name = label_m
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
                                                    "Iba pa nga komento", html.Br(),
                                                    html.Small(" (Remarks)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_pubutilint_remarks',
                                                class_name = label_m
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
                                    ], class_name = row_m
                                ),
                            ],
                            id = 'rep_cre_div_pubutil',
                            className = div_m,
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
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_dmgdhouse_assignedsex_id',
                                                    clearable = True
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
                                                    "Lokasiyon san balay", #tag_required,
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
                                                                id = 'rep_cre_input_dmgdhouse_geoloc',
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
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H5(
                                                    [
                                                        html.I(className = 'bi bi-file-earmark-richtext me-2'),
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
                                                    "Iba pa nga komento", html.Br(),
                                                    html.Small(" (Remarks)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_dmgdhouse_remarks',
                                                class_name = label_m
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_dmgdhouse_remarks',
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
                            ],
                            id = 'rep_cre_div_dmgdhouse',
                            className = div_m,
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
                                                    "Klase san imprastruktura", tag_required, html.Br(),
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
                                                    id = 'rep_cre_input_dmgdinfra_desc',
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
                                                    "Kantidad san narubat", tag_required, html.Br(),
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
                                                            id = 'rep_cre_input_dmgdinfra_qtyunit',
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
                                                    "Presyo san narubat", tag_required, html.Br(),
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
                                                    "Kabutangan", tag_required, html.Br(),
                                                    html.Small(" (Status)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_dmgdinfrastatus_id',
                                                class_name = label_m
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Select(
                                                #dcc.Dropdown(
                                                    id = 'rep_cre_label_dmgdinfrastatus_id',
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
                                                    "Iba pa nga komento", html.Br(),
                                                    html.Small(" (Remarks)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_dmgdinfra_remarks',
                                                class_name = label_m
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_dmgdinfra_remarks',
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
                            ],
                            id = 'rep_cre_div_dmgdinfra',
                            className = div_m,
                            style = {'display' : 'none'}
                        ),
                        # Submit button
                        html.Div(
                            [
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
                                                href = '#'
                                            ),
                                            #md = 3, sm = 12,
                                            class_name = 'align-self-center col-md-3 mb-2'
                                        )
                                    ],
                                    class_name = 'justify-content-end'
                                )
                            ],
                            id = 'rep_cre_div_submit',
                            className = footer_m,
                            style = {'display' : 'none'}
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
        Input('rep_cre_input_selectgps', 'value'),
    ]
)

def rep_cre_geolocrefresh(selectgps):
    if selectgps: return [True]
    else: return [False]

# Callback for setting URL links of hyperlinks for GPS location
@app.callback(
    [
        Output('rep_cre_input_dmgdhouse_geoloc', 'value'),
        Output('rep_cre_input_dmgdhouse_geoloc', 'disabled'),
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
        # Casualty
        Output('rep_cre_input_casualty_assignedsex_id', 'options'),
        Output('rep_cre_input_casualty_region_id', 'options'),
        Output('rep_cre_input_casualty_region_id', 'value'),
        Output('rep_cre_input_casualtytype_id', 'options'),
        Output('rep_cre_input_casualtystatus_id', 'options'),
        # Public utility status
        Output('rep_cre_input_pubutiltype_id', 'options'),
        Output('rep_cre_input_pubutilinttype_id', 'options'),
        Output('rep_cre_col_pubutilinttype_desc', 'children'),
        # Damaged house
        Output('rep_cre_input_dmgdhousetype_id', 'options'),
        Output('rep_cre_col_dmgdhousetype_desc', 'children'),
        # Infrastructure
        Output('rep_cre_input_infratype_id', 'options'),
        Output('rep_cre_input_infraclass_id', 'options'),
        Output('rep_cre_input_dmgdinfra_qtyunit', 'options'),
        Output('rep_cre_input_dmgdinfra_qtyunit', 'value'),
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
        FROM utilities.dmgdhousetype;
        """
        values = []
        cols = ['label', 'value', 'desc_war', 'desc_en']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        dmgdhousetypes = df[['label', 'value']].to_dict('records')
        dropdowns.append(dmgdhousetypes)

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
        Input('rep_cre_input_reporttype_id', 'value')
    ]
)

def rep_cre_showreportform(type):
    disp_none = {'display' : 'none'}
    disp_show = {'display' : 'block'}
    style_submit = disp_none
    style_relinc = disp_none
    style_casualty = disp_none
    style_pubutil = disp_none
    style_dmgdhouse = disp_none
    style_dmgdinfra = disp_none
    if type:
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
        Output('rep_cre_input_pubutilint_intdate', 'date'),
        Output('rep_cre_input_pubutilint_inttime_hh', 'value'),
        Output('rep_cre_input_pubutilint_inttime_mm', 'value'),
        Output('rep_cre_input_pubutilint_inttime_ss', 'value'),
        Output('rep_cre_input_pubutilint_inttime_ampm', 'value')
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