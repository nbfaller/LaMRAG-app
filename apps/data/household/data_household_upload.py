# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import hashlib
from datetime import datetime, timedelta
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
        dcc.Store(id = 'dat_bar_hou_sto_rescount', data = 0),
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
                                                html.H1(
                                                    [
                                                        "Upload household profile",
                                                        #html.Small(" (User Registration)", className = 'text-muted')
                                                    ]
                                                ),
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
                                            id = 'dat_hou_upl_row_header',
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
                                                                            html.Span(id = 'dat_hou_upl_alert_inputvalidation_span_missing')
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            id = 'dat_hou_upl_alert_inputvalidation',
                                                            is_open = False,
                                                            color = 'warning',
                                                            class_name = label_m,
                                                            dismissable = True,
                                                            #fade = True,
                                                        )
                                                    ]
                                                )
                                            ],
                                            id = 'dat_hou_upl_row_inputvalidation',
                                            class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Barangay", tag_required, #html.Br(),
                                                            #html.Small(" (Event)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_hou_upl_label_brgy_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.Dropdown(
                                                            id = 'dat_hou_upl_input_brgy_id',
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
                                            id = 'dat_hou_upl_row_brgy_id',
                                            class_name = row_m,
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Purok", tag_required, html.Br(),
                                                            #html.Small(" (Purok)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_bar_label_purok',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            id = 'dat_bar_input_purok',
                                                            type = 'number',
                                                            min = 1,
                                                            invalid = False,
                                                            required = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Alayon pagbutang san numero san purok kun diin ini natabó. (Please input the purok number where this incident occurred.)",
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
                                                            "Lokasiyon san balay", tag_required,
                                                            html.Br(),
                                                            html.Small(" (Location of home)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_hou_upl_label_loc',
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
                                                                        id = 'dat_hou_upl_input_loc',
                                                                        #disabled = True,
                                                                        #placeholder = "Pili (select)...",
                                                                        #value = 8
                                                                    ),
                                                                    class_name = 'align-self-center col-12 col-md-6 col-lg-8 mb-2 mb-md-0'
                                                                ),
                                                                dbc.Col(
                                                                    dbc.Switch(
                                                                        id = 'dat_hou_upl_input_selectgps',
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
                                                    dbc.Label(
                                                        [
                                                            "Kadamo san mga na-istar", tag_required, html.Br(),
                                                            html.Small(" (Number of household residents)", className = 'text-muted')
                                                        ],
                                                        id = 'dat_bar_label_rescount',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            id = 'dat_bar_input_rescount',
                                                            type = 'number',
                                                            #value = 1,
                                                            min = 1,
                                                            invalid = False,
                                                            required = True
                                                        ),
                                                        #dbc.FormText(
                                                        #    "Alayon pagbutang san numero san purok kun diin ini natabó. (Please input the purok number where this incident occurred.)",
                                                        #    color = 'secondary',
                                                        #    class_name = ftext_m
                                                        #),
                                                    ],
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9 col-lg-9'
                                                ),
                                            ], class_name = row_m,
                                        ),
                                    ]
                                ),
                                # Household residents
                                html.Div(
                                    [
                                        html.Hr(),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H4(
                                                            [
                                                                html.I(className = 'bi bi-person-vcard me-2'),
                                                                "Mga na-istar sini nga balay",
                                                                #html.Br(),
                                                                html.Small(" (Household residents)", className = 'text-muted')
                                                            ]
                                                        ),
                                                    ]
                                                )
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            id = 'dat_hou_upl_row_residents'
                                        ),
                                    ],
                                    id = 'dat_hou_upl_div_residents',
                                    className = row_m + ' d-none',
                                    #style = {'display' : 'none'}
                                )
                            ]
                        )
                    ],
                    class_name = 'col-lg-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)

dat_hou_upl_pathname = '/data/household/upload'

# Callback for changing number of household residents
@app.callback(
    [
        Output('dat_bar_hou_sto_rescount', 'data')
    ],
    [
        Input('dat_bar_input_rescount', 'value')
    ]
)

def dat_hou_upl_setrescount(count):
    return [count]

# # Callback for populating basic dropdown menus
@app.callback(
    [
        # Dropdowns
        Output('dat_hou_upl_input_brgy_id', 'options'),
        Output('dat_hou_upl_input_brgy_id', 'value'),
        #Output({'type' : 'dat_hou_upl_input_assignedsex_id', 'index' : ALL}, 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data'),
    ]
)

def dat_hou_upl_populatedropdowns(pathname, region, province, citymun, brgy):
    if pathname == dat_hou_upl_pathname:
        dropdowns = []

        # Barangays
        sql = """SELECT name as label, id as value
        FROM utilities.addressbrgy
        WHERE region_id = %s AND province_id = %s AND citymun_id = %s;
        """
        values = [region, province, citymun]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        brgys = df.to_dict('records')
        dropdowns.append(brgys)
        dropdowns.append(brgy)

        # Assgined sex
        #sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        #FROM utilities.assignedsex;
        #"""
        #values = []
        #df = db.querydatafromdatabase(sql, values, cols)
        #df = df.sort_values('value')
        #sexes = df.to_dict('records')
        #dropdowns.append(sexes)
        
        return dropdowns
    else: raise PreventUpdate

# Callback for populating form based on number of residents
@app.callback(
    [
        # Residents div
        Output('dat_hou_upl_row_residents', 'children'),
        Output('dat_hou_upl_div_residents', 'className'),
        #Output({'type' : 'dat_hou_upl_input_assignedsex_id', 'index' : ALL}, 'options'),
    ],
    [
        Input('dat_bar_hou_sto_rescount', 'data'),
    ]
)

def dat_hou_upl_populatedropdowns(count):
    to_return = []
    className = 'mb-2 d-none',

    # Populating dropdowns
    # Assgined sex
    sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
    FROM utilities.assignedsex;
    """
    values = []
    cols = ['label', 'value']
    df = db.querydatafromdatabase(sql, values, cols)
    df = df.sort_values('value')
    sexes = df.to_dict('records')
    
    if count and count >= 1:
        className = 'mb-2 d-block',
        for i in range(1, 1 + count):
            resident = [
                dbc.Col(
                    [
                        html.H4(
                            [
                                html.Span("Residente numero ", className = 'd-inline d-lg-none'),
                                html.Span("No. ", className = 'd-none d-lg-inline'),
                                i
                            ]
                        )
                    ],
                    class_name = 'text-muted text-lg-start col-12 col-lg-1'
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Label(
                                        [
                                            "Ngaran", tag_required, html.Br(),
                                            html.Small(" (Name)", className = 'text-muted')
                                        ],
                                        id = {
                                            'type' : 'dat_hou_upl_label_name',
                                            'index' : i
                                        },
                                        class_name = label_m
                                    ),
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type = 'text',
                                            id = {
                                                'type' : 'dat_hou_upl_input_fname',
                                                'index' : i
                                                },
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
                                            id = {
                                                'type' : 'dat_hou_upl_input_mname',
                                                'index' : i
                                            },
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
                                            id = {
                                                'type' : 'dat_hou_upl_input_lname',
                                                'index' : i
                                            },
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
                                            "Petsa san pagkatawo", tag_required, html.Br(),
                                            html.Small(" (Date of birth)", className = 'text-muted')
                                        ],
                                        id = {
                                            'type' : 'dat_hou_upl_label_birthdate',
                                            'index' : i
                                        },
                                        class_name = label_m
                                    ),
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                ),
                                dbc.Col(
                                    dcc.DatePickerSingle(
                                        id = {
                                            'type' : 'dat_hou_upl_input_birthdate',
                                            'index' : i
                                        },
                                        placeholder = 'MM/DD/YYYY',
                                        #month_format = 'MMM Do, YYYY',
                                        clearable = True,
                                        #style = {'width' : '100%'}
                                        className = 'w-100'
                                    ),
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                ),
                                dbc.Col(
                                    dbc.Label(
                                        [
                                            "Natawo nga babayi/lalaki", tag_required, html.Br(),
                                            html.Small(" (Sex assigned at birth)", className = 'text-muted')
                                        ],
                                        id = {
                                            'type' : 'dat_hou_upl_label_assignedsex_id',
                                            'index' : i
                                        },
                                        class_name = label_m
                                    ),
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                ),
                                dbc.Col(
                                    [
                                        dbc.Select(
                                            id = {
                                                'type ': 'dat_hou_upl_input_assignedsex_id',
                                                'index' : i
                                            },
                                            options = sexes
                                            #clearable = True
                                        ),
                                        #dbc.FormText(
                                        #    "Mga active event la an puwede mahimuan report. (Reports can only be filed for active events.)",
                                        #    color = 'secondary',
                                        #    class_name = ftext_m
                                        #),
                                    ],
                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3 col-lg-3'
                                ),
                            ], className = div_m,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5(
                                            [
                                                html.I(className = 'bi bi-person-plus me-2'),
                                                "Dugang nga impormasiyon",
                                                #html.Br(),
                                                html.Small(" (Additional information)", className = 'text-muted')
                                            ]
                                        ),
                                        html.P(
                                            [
                                                """Guintatalingúha san Siyudadnon nga Gobyerno an paghatag san tangkód
                                                nga serbisyo sa iya mga sinasakupan. Upod sini an paghatag san espésiyal
                                                nga atensiyon o pag-atáman sa mga minorya o bulnerable nga sektor san aton
                                                katilíngban. Tungód sini, guin-aaghat an ngatanan nga mga residente nga magpahibaro kun
                                                api sira sini nga mga sektor.""",
                                                html.Br(),
                                                html.Small(
                                                    """(The city government seeks to deliver equitable services to its constituents.
                                                    This necessitates the provision of specific attention or care to minorities or
                                                    vulnerable sectors of our society. Residents are thus encouraged to identify themselves
                                                    as the following whenever applicable.)""",
                                                    className = 'text-muted'
                                                )
                                            ], className = p_m
                                        ),
                                    ]
                                )
                            ], class_name = row_m
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Checklist(
                                            options = [
                                                {
                                                    'label' : [
                                                        """🧑‍🍼 Usa ako nga solo parent.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """I am a solo parent.""",
                                                            className = 'text-muted'
                                                        )
                                                    ],
                                                    'value' : 1
                                                },
                                                {
                                                    'label' : [
                                                        """🏳️‍🌈 Ginkikilala ko an akon kalugaringon nga queer, non-binary, o LGBTQIA+.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """I identify as queer, non-binary or LGBTQIA+.""",
                                                            className = 'text-muted'
                                                        )
                                                    ],
                                                    'value' : 2
                                                },
                                                {
                                                    'label' : [
                                                        """🛡️ Ginkikilala ko an akon kalugaringon nga indigenous person o miyembro san IP nga grupo.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """I identify as an indigenous person or member of an IP group.""",
                                                            className = 'text-muted'
                                                        )
                                                    ],
                                                    'value' : 3
                                                },
                                            ],
                                            id = {
                                                'type' : 'dat_hou_upl_input_checklist_demography',
                                                'index' : i
                                            },
                                        )
                                    ],
                                    class_name = 'mb-0 col-12 col-md-6'
                                ),
                                dbc.Col(
                                    [
                                        dbc.Checklist(
                                            options = [
                                                {
                                                    'label' : [
                                                        """♿️ May ada ako dugang nga pangingihanlan o sinisiring nga disability.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """I have special needs (i.e., a disability).""",
                                                            className = 'text-muted'
                                                            )
                                                        ],
                                                    'value' : 1
                                                },
                                                {
                                                    'label' : [
                                                        """🩺 Mayda ako panmaiha (chronic) o seryoso nga sakit.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """I have a chronic or serious disease.""",
                                                            className = 'text-muted'
                                                        )
                                                    ],
                                                    'value' : 2
                                                },
                                            ],
                                            id = {
                                                'type' : 'dat_hou_upl_input_checklist_needs',
                                                'index' : i
                                            },
                                        )
                                    ],
                                    class_name = 'mb-0 col-12 col-md-6'
                                ),
                            ], class_name = row_m
                        ),
                        html.Hr()
                    ],
                    class_name = 'col-12 col-lg-11'
                )
            ]
            to_return += resident
    return [to_return, className]