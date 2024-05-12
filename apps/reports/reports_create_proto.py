# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# App definition
from application import application as app
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
                                                id = 'rep_cre_label_event_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_event_id',
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
                                                id = 'rep_cre_label_reporttype_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_reporttype_id',
                                                    clearable = True,
                                                    #className = 'mb-1'
                                                ),
                                                dbc.FormText(
                                                    "Usa la nga initial report an puwede himuon. (Initial reports can only be filed once.)",
                                                    color = 'secondary'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-3',
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
                            id = 'rep_cre_div_basicdetails'
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H4(
                                            [
                                                html.I(className = 'bi bi-journal-text me-2'),
                                                "Synopsis/Overview",
                                                #html.Br(),
                                                #html.Small(" (Present address)", className = 'text-muted')
                                            ]
                                        ),
                                        # Note: Maybe we should create a separate page as a guide for writing synopses?
                                        html.P(
                                            [
                                                dbc.Row(
                                                    dbc.Col(
                                                        """Sa pagsusurat san synopsis/overview, maupay batunon ini
                                                        nga mga pakiana kun sano man naangay o posible:"""
                                                    )
                                                ),
                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Small(
                                                            """(In writing the synopsis/overview, you are encouraged
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
                                                                        html.I(className = 'bi bi-patch-question me-2'), html.B("Nano"), " an natabo?",
                                                                        html.Small([" (", html.B("What"), " happened?)"], className = 'text-muted')
                                                                    ]
                                                                ),
                                                                html.Li(
                                                                    [
                                                                        html.I(className = 'bi bi-geo me-2'), html.B("Diin"), " ini natabo?",
                                                                        html.Small([" (", html.B("Where"), " did this happen?)"], className = 'text-muted')
                                                                    ]
                                                                ),
                                                                html.Li(
                                                                    [
                                                                        html.I(className = 'bi bi-person-circle me-2'), html.B("Sira sino"), " an naapektuhan?",
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
                                                                        html.I(className = 'bi bi-calendar-event me-2'), html.B("Kakan-o"), " ini natabo?",
                                                                        html.Small([" (", html.B("When"), " did this happen?)"], className = 'text-muted')
                                                                    ]
                                                                ),
                                                                html.Li(
                                                                    [
                                                                        html.I(className = 'bi bi-eye me-2'), html.B("Panano"), " ini natabo?",
                                                                        html.Small([" (", html.B("How"), " did this happen?)"], className = 'text-muted')
                                                                    ]
                                                                ),
                                                                html.Li(
                                                                    [
                                                                        html.I(className = 'bi bi-search me-2'), html.B("Kay nano"), " ini natabo?",
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
                                                        """Alayon pag-angay san synopsis/overview sa klase san report nga ginsusurat. Diri kinihanglan suraton an baton sa mga pakiana
                                                        nga nababaton san iba nga mga parte sini nga report. Diri liwat kinihanglan suraton an mga nasurat na sa
                                                        mga nauna nga report."""
                                                    )
                                                ),
                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Small(
                                                            """(Please write the synopsis/overview in a manner appropriate to the chosen type of report. Writing the answers
                                                            to questions that can be filled out in the rest of this report is not necessary. There is also no need
                                                            to write details that are already written in past reports.)""",
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
                                                    id = 'rep_cre_input_synopsis',
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
                                    id = 'rep_cre_row_synopsis'
                                ),
                            ],
                            className = 'mb-3',
                            id = 'rep_cre_div_synopsis'
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H4(
                                            [
                                                html.I(className = 'bi bi-person-fill-exclamation me-2'),
                                                "RDANA",
                                                #html.Br(),
                                                html.Small(" (Rapid Damage Assessment and Needs Analysis)", className = 'text-muted')
                                            ]
                                        ),
                                        # Note: Maybe we should create a separate page as a guide for writing synopses?
                                        html.P(
                                            [
                                                dbc.Row(
                                                    dbc.Col(
                                                        """Sa pagpili san mga klase san rubâ nga na-obserbahan,
                                                        maupay tigamnan ini nga mga kondisyon:"""
                                                    )
                                                ),
                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Small(
                                                            """(In selecting the types of damage observed, it
                                                            would be helpful to take note of these conditions:)"""
                                                        )
                                                    ), class_name = 'text-muted mb-3'
                                                ),
                                                dbc.Row(
                                                    dbc.Accordion(
                                                        dbc.AccordionItem(
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        id = 'rep_cre_col_damagetype_desc1',
                                                                        class_name = 'col-12 col-lg-6'
                                                                    ),
                                                                    dbc.Col(
                                                                        id = 'rep_cre_col_damagetype_desc2',
                                                                        class_name = 'col-12 col-lg-6'
                                                                    )
                                                                ]
                                                            ),
                                                            title = "Mga klase san rubâ (Types of damage)"
                                                        ),
                                                        #flush = True,
                                                        start_collapsed = True
                                                    ),
                                                    #class_name = 'mb-1'
                                                ),
                                            ],
                                        )
                                    ], #class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Nakit-an nga mga rubâ", html.Br(),
                                                    html.Small(" (Damage observed)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_damagetype_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_cre_input_damagetype_id',
                                                    clearable = True,
                                                    multi = True
                                                    #className = 'mb-1'
                                                ),
                                                dbc.FormText(
                                                    "Alayon pagpili san ngatanan nga klase san rubâ nga na-obserbahan. (Please select all kinds of damage that was observed.)",
                                                    color = 'secondary'
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-3',
                                    id = 'rep_cre_row_damagetype'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Deskripsiyon san mga rubâ", html.Br(),
                                                    html.Small(" (Description of damage observed)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_rdana_desc'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_rdana_desc',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '10em',
                                                        'width' : '100%',
                                                    },
                                                    className = 'mb-1'
                                                ),
                                                #dbc.FormText(
                                                #    "Alayon pagpili san ngatanan nga klase san rubâ nga na-obserbahan. (Please select all kinds of damage that was observed.)",
                                                #    color = 'secondary'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-3',
                                    id = 'rep_cre_row_rdana_desc'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Mga apektado nga tawo", html.Br(),
                                                    html.Small(" (Affected individuals)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_rdana_affected'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Textarea(
                                                    id = 'rep_cre_input_drdana_affected',
                                                    #clearable = True,
                                                    wrap = True,
                                                    style = {
                                                        'height' : '10em',
                                                        'width' : '100%',
                                                    },
                                                    className = 'mb-1'
                                                ),
                                                #dbc.FormText(
                                                #    "Alayon pagpili san ngatanan nga klase san rubâ nga na-obserbahan. (Please select all kinds of damage that was observed.)",
                                                #    color = 'secondary'
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-0 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-3',
                                    id = 'rep_cre_row_rdana_affected'
                                ),
                            ], id = 'rep_cre_div_rdana'
                        ),
                        html.Hr(),
                        html.Div(
                            [

                                dbc.Row(
                                    [
                                        html.H4(
                                            [
                                                html.I(className = 'bi bi-clipboard-data-fill me-2'),
                                                "Mga kaupod nga insidénte",
                                                #html.Br(),
                                                html.Small(" (Related incidents)", className = 'text-muted')
                                            ]
                                        ),
                                        # Note: Maybe we should create a separate page as a guide for writing synopses?
                                        html.P(
                                            [
                                                dbc.Row(
                                                    dbc.Col(
                                                        """Alayon pagbutang san mga naihap sini nga mga klase
                                                        san insidénte."""
                                                    )
                                                ),
                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Small(
                                                            """(Please input the numbers of related incidents:)"""
                                                        )
                                                    ), class_name = 'text-muted'
                                                ),
                                            ],
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Mga direkta nga epekto", html.Br(),
                                                    html.Small(" (Direct impact)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_dirimp'
                                            ),
                                            class_name = 'align-self-center mb-1 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'bi bi-tree-fill')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_faltre',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Mga natumba nga puno/poste san kuryente", html.Br(),
                                                                    html.Small("(Fallen trees/toppled electric posts)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-fish')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_misfis',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Mga nawawara nga manaragat", html.Br(),
                                                                    html.Small("(Missing fisherfolk)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'bi bi-life-preserver')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_drowni',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Mga nalumos", html.Br(),
                                                                    html.Small("(Drowning)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-ship')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_marinc',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Mga insidente sa dagat", html.Br(),
                                                                    html.Small("(Maritime incident)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    )
                                                ]
                                            ),
                                            class_name = 'col-12 col-md-9'
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            class_name = 'col-0 col-md-3'
                                        ),
                                        dbc.Col(
                                            html.Hr(
                                                className = 'mt-0 mt-lg-3'
                                            ),
                                            class_name = 'col-12 col-md-9'
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Mga epekto sa mga estruktura ug kalikasan", html.Br(),
                                                    html.Small(" (Structural and/or environmental impact)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_strenv'
                                            ),
                                            class_name = 'align-self-center mb-1 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-hill-rockslide')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_landsl',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Pagtimpag san tuna tungod san uran", html.Br(),
                                                                    html.Small("(Rain-induced landslide)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-person-digging')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_debflo',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Pag-agos san basura", html.Br(),
                                                                    html.Small("(Debris flow)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-sailboat')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_subfis',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Mga nalumos nga baluto para panagat", html.Br(),
                                                                    html.Small("(Submerged fishing boats)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'bi bi-building-fill-x')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_colstr',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Mga narusmok nga estruktura", html.Br(),
                                                                    html.Small("(Collapsed structure)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    )
                                                ]
                                            ),
                                            class_name = 'col-12 col-md-9'
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            class_name = 'col-0 col-md-3'
                                        ),
                                        dbc.Col(
                                            html.Hr(
                                                className = 'mt-0 mt-lg-3'
                                            ),
                                            class_name = 'col-12 col-md-9'
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Mga purok nga ginbaha", html.Br(),
                                                    html.Small(" (Flooded puroks)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_flood'
                                            ),
                                            class_name = 'align-self-center mb-1 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-house-flood-water')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_flocur',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Padayon nga ginbabaha", html.Br(),
                                                                    html.Small("(Currently flooded)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-house-flood-water-circle-arrow-right')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_florec',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Paiban na an baha", html.Br(),
                                                                    html.Small("(Receding flood)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-house')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_flosub',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Nagmara na an baha", html.Br(),
                                                                    html.Small("(Subsided flood)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    )
                                                ]
                                            ),
                                            class_name = 'col-12 col-md-9'
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            class_name = 'col-0 col-md-3'
                                        ),
                                        dbc.Col(
                                            html.Hr(
                                                className = 'mt-0 mt-lg-3'
                                            ),
                                            class_name = 'col-12 col-md-9'
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Mga diri direkta nga epekto", html.Br(),
                                                    html.Small(" (Indirect impact)", className = 'text-muted')
                                                ],
                                                id = 'rep_cre_label_relinc_strenv'
                                            ),
                                            class_name = 'align-self-center mb-1 mb-md-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-plug-circle-xmark')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_elepos',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Mga sunog nga poste san kuryente/rubat nga transformer", html.Br(),
                                                                    html.Small("(Electrical post fire/busted transformer)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-droplet-slash')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_buswat',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Rubat nga linya san tubig", html.Br(),
                                                                    html.Small("(Busted waterpipe)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-house-fire')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_strfir',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Mga nasunog nga estruktura", html.Br(),
                                                                    html.Small("(Structural fire)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupText(
                                                                        html.I(className = 'fa fa-viruses')
                                                                    ),
                                                                    dbc.Input(
                                                                        id = 'rep_cre_input_relinc_disout',
                                                                        type = 'number',
                                                                        value = 0,
                                                                        min = 0
                                                                    )
                                                                ],
                                                                className = 'mb-1'
                                                            ),
                                                            dbc.FormText(
                                                                [
                                                                    "Pagsarang san sakit", html.Br(),
                                                                    html.Small("(Disease outbreak)", className = 'text-secondary'),
                                                                ],
                                                                color = 'dark'
                                                            ),
                                                        ],
                                                        class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                                    )
                                                ]
                                            ),
                                            class_name = 'col-12 col-md-9'
                                        ),
                                    ]
                                ),
                            ], id = 'rep_cre_div_relinc'
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
        Output('rep_cre_geoloc_loc_en', 'href')
    ],
    [
        Input('rep_cre_geoloc', 'position'),
        Input('rep_cre_geoloc', 'local_date')
    ]
)

def rep_cre_geolocrefresh(pos, date):
    href = None
    if pos:
        lat = pos['lat']
        lon = pos ['lon']
        href = 'https://www.google.com/maps/place/%s,%s' % (lat, lon)
    return [href, href]

# Callback for populating basic dropdown menus
@app.callback(
    [
        Output('rep_cre_input_reporttype_id', 'options'),
        Output('rep_cre_input_damagetype_id', 'options'),
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
        FROM utilities.reporttype
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        reporttypes = df.to_dict('records')
        dropdowns.append(reporttypes)

        # Damage types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.damagetype
        """
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        damagetypes = df.to_dict('records')
        dropdowns.append(damagetypes)

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