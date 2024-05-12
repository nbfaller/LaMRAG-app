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
        #dcc.Geolocation(id = 'rep_cre_geoloc'),
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
                                    #id = 'rep_cre_row_header',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Panhitabó", tag_required, html.Br(),
                                                    html.Small(" (Event)", className = 'text-muted')
                                                ],
                                                #id = 'rep_cre_label_event_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    #id = 'rep_cre_input_event_id',
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
                                    #id = 'rep_cre_row_event',
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
                                                #id = 'rep_cre_label_reporttype_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    #id = 'rep_cre_input_reporttype_id',
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
                                    #id = 'rep_cre_row_reporttype',
                                    class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Purok san panhitabó", tag_required, html.Br(),
                                                    html.Small(" (Purok of occurrence)", className = 'text-muted')
                                                ],
                                                #id = 'rep_cre_label_purok',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    #id = 'rep_cre_input_purok',
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
                                                    "Petsa san panhitabó", tag_required, html.Br(),
                                                    html.Small(" (Date of occurrence)", className = 'text-muted')
                                                ],
                                                #id = 'rep_cre_label_date',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-2'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.DatePickerSingle(
                                                    #id = 'rep_cre_input_date',
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
                                                    "Oras san panhitabó", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (Time of occurrence)", className = 'text-muted')
                                                ],
                                                #id = 'rep_cre_label_time',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.InputGroup(
                                                    [
                                                        dbc.Input(
                                                            #id = 'rep_cre_input_time_hh',
                                                            placeholder = 'HH',
                                                            type = 'number',
                                                            min = 1,
                                                            max = 12,
                                                            invalid = False
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            #id = 'rep_cre_input_time_mm',
                                                            placeholder = 'MM',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False
                                                        ),
                                                        dbc.InputGroupText(":"),
                                                        dbc.Input(
                                                            #id = 'rep_cre_input_time_ss',
                                                            placeholder = 'SS',
                                                            type = 'number',
                                                            min = 0,
                                                            max = 59,
                                                            invalid = False
                                                        ),
                                                        dbc.Select(
                                                            #id = 'rep_cre_input_time_ampm',
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
                                                                            #id = 'rep_cre_geoloc_loc_war',
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
                                                                                    #id = 'rep_cre_geoloc_loc_en',
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
                                                    #id = 'rep_cre_alert_geolocnotice',
                                                    color = 'info',
                                                    class_name = 'mb-0',
                                                    dismissable = True
                                                )
                                            ]
                                        )
                                    ],
                                    class_name = 'mb-2'
                                ),
                            ],
                            #id = 'rep_cre_div_basicdetails',
                            className = 'mb-3'
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
                                                    "Klase san pagkarubat", tag_required, html.Br(),
                                                    html.Small(" (Type of damage)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_dmgdhousetype_id',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_dmgdhousetype_id',
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
                                                id = 'rep_cre_label_dmgdhouse_name',
                                                class_name = 'mb-0'
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
                                                id = 'rep_cre_label_dmgdhouse_age',
                                                class_name = 'mb-0'
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
                                                id = 'rep_cre_label_dmgdhouse_assignedsex_id',
                                                class_name = 'mb-0'
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
                                            dbc.Label(
                                                [
                                                    "Lokasiyon san balay", #tag_required,
                                                    html.Br(),
                                                    html.Small(" (Location of home)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_dmgdhouse_geoloc',
                                                class_name = 'mb-0'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    id = 'rep_cre_input_dmgdhouse_geoloc',
                                                    disabled = True,
                                                    #placeholder = "Pili (select)...",
                                                    #value = 8
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-2'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Iframe(
                                                    src = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d562.5407776071039!2d124.61192079862425!3d12.06236092006715!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3309db8c252d21d1%3A0xaf1f98f12b16d98f!2sCalbayogCdrrmo!5e1!3m2!1sen!2sph!4v1709188668855!5m2!1sen!2sph',
                                                    width = '100%',
                                                    height = '200em',
                                                    style = {'border' : '0'},
                                                    #allowfullscreen ="",
                                                    loading_state = 'lazy',
                                                    referrerPolicy = 'no-referrer-when-downgrade'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        )
                                    ], class_name = 'mb-2'
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
                                    ], class_name = 'mt-3'
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
                                                class_name = 'mb-0'
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
                                    ], class_name = 'mb-2'
                                ),
                            ],
                            id = 'rep_cre_div_dmgdhouse',
                            className = 'mt-3 mb-3',
                            style = {'display' : 'block'}
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
                                                #id = 'rep_cre_btn_submit',
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
                            #id = 'rep_cre_div_submit',
                            className = 'mt-3',
                            style = {'display' : 'block'}
                        )
                    ],
                    class_name = 'col-lg-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)