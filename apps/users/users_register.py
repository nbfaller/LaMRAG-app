# FIX THIS ERROR
# When you input permanent address first and add present address later
# details in permanent address fields disappear.

# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import hashlib
# App definition
from application import app
from apps import dbconnect as db

usr_reg_tag_required = html.Sup("*", className = 'text-danger')

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
        dcc.Store(id = 'usr_reg_store_regsuccess', data = False, storage_type = 'session'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H1(
                                                    [
                                                        "User Registration",
                                                        #html.Small(" (User Registration)", className = 'text-muted')
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        "Kinihanglan pun-on an mga patlang nga may pula nga asterisk ", usr_reg_tag_required, ".",
                                                        html.Br(),
                                                        html.Small(
                                                            ["(Fields with red asterisks ", usr_reg_tag_required, " are required.)"],
                                                            className = 'text-muted'
                                                        )
                                                    ], className = p_m
                                                )
                                            ],
                                            id = 'usr_reg_row_header',
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
                                                                            html.Span(id = 'usr_reg_alert_inputvalidation_span_missing')
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            id = 'usr_reg_alert_inputvalidation',
                                                            is_open = False,
                                                            color = 'warning',
                                                            class_name = label_m,
                                                            dismissable = True,
                                                            #fade = True,
                                                        )
                                                    ]
                                                )
                                            ],
                                            id = 'usr_reg_row_inputvalidation',
                                            class_name = row_m
                                        ),
                                        dbc.Row(
                                            [

                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Klase san magamit", usr_reg_tag_required,
                                                            html.Br(), html.Small(" (User type)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_usertype_id',
                                                        class_name = row_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_usertype_id',
                                                        clearable = True,
                                                        value = 1
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                ),
                                            ], className = 'mb-1 mb-md-0',
                                            id = 'usr_reg_row_usertype'
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
                                                                            html.Span(id = 'usr_reg_alert_usertype_text_war'),
                                                                            html.Br(),
                                                                            html.Small(
                                                                                id = 'usr_reg_alert_usertype_text_en',
                                                                                className = 'text-muted'
                                                                            ),
                                                                            html.Br(), html.Br(),
                                                                            "Kun gintuyo mo ini, puwede mo pasagdan ini nga pahibaro.",
                                                                            html.Br(),
                                                                            html.Small(
                                                                                "(If this was intended, you can disregard this warning.)",
                                                                                className = 'text-muted'
                                                                            ),
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            id = 'usr_reg_alert_usertype',
                                                            is_open = False,
                                                            color = 'warning',
                                                            class_name = label_m,
                                                            dismissable = False,
                                                            #fade = True,
                                                        )
                                                    ]
                                                )
                                            ],
                                            id = 'usr_reg_row_alert_usertype',
                                            class_name = row_m
                                        )
                                    ], className = header_m,
                                ),
                                html.Hr(),
                                # Basic identity
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-person-vcard-fill me-2'),
                                                        "Primero nga impormasyon",
                                                        #html.Br(),
                                                        html.Small(" (Basic information)", className = 'text-muted')
                                                    ]
                                                ),
                                            ], class_name = row_m
                                        ),
                                        # Name
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Ngaran", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Name)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_name',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_fname',
                                                        placeholder = ['Primero (First name)'],
                                                        invalid = False
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_mname',
                                                        placeholder = 'Butnga (Middle name)'
                                                    ),
                                                    md = 3, sm = 12,
                                                    class_name = ' align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_lname',
                                                        placeholder = 'Apelyido (Last name)',
                                                        invalid = False
                                                    ),
                                                    md = 3, sm = 12,
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                            ],
                                            id = 'usr_reg_row_name',
                                            class_name = row_m
                                        ),
                                        # Input validation for name
                                        dbc.Row(
                                            [
                                                dbc.Col(
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
                                                                        "Mayda ka na account sa LáMRAG. Usa la nga account an puwede ihatag sa kada magamit. Alayon pag-contact san administrator para mabuligan ka.",
                                                                        html.Br(),
                                                                        html.Small(
                                                                            "(You already have an account in LáMRAG. Each user can only have one account. Please contact the administrator for guidance.)",
                                                                            className = 'text-muted'
                                                                        ),
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        id = 'usr_reg_alert_namevalidation',
                                                        is_open = False,
                                                        color = 'warning',
                                                        class_name = label_m,
                                                        dismissable = True,
                                                        #fade = True,
                                                    )
                                                )
                                            ]
                                        ),
                                        # Username
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        "Username",
                                                        id = 'usr_reg_label_username',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_username',
                                                        placeholder = 'Username',
                                                        disabled = True
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                ),
                                                dbc.Tooltip(
                                                    "Usernames are automatically generated.",
                                                    target = 'usr_reg_label_username'
                                                )
                                            ], class_name = row_m
                                        ),
                                        # Birthdate and sex assigned at birth
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Petsa san pagkatawo", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Date of birth)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_birthdate',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.DatePickerSingle(
                                                        id = 'usr_reg_input_birthdate',
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
                                                            "Natawo nga babayi/lalaki", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Sex assigned at birth)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_assignedsex',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_assignedsex_id',
                                                        clearable = True
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                            ], class_name = row_m
                                        )
                                    ], className = div_m
                                ),
                                # Affirmative identity
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-rainbow me-2'),
                                                        "Apirmatibo nga identidad",
                                                        #html.Br(),
                                                        html.Small(" (Affirmative identity)", className = 'text-muted')
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        """Guin-aaghat ug guinpapanalipdan san Siyudadnon nga Gobyerno an katungod san iya mga
                                                        empleyado nga magpahayag san ira sexual orientation, gender identity, ug expression (SOGIE).
                                                        Guin-aaghat an ngatanan nga maghatag sini nga impormasyon kun sano man ini naangay.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """(The City Government seeks to promote and protect the ability of its employees to
                                                            freely express their sexual orientation, gender identity, and expression (SOGIE).
                                                            Everyone is enjoined to fill out these details whenever applicable.)""",
                                                            className = 'text-muted'
                                                        )
                                                    ], className = p_m
                                                ),
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        "Lived name",
                                                        id = 'usr_reg_label_livedname',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_livedname',
                                                        placeholder = 'Lived name'
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
                                                            "Honoripiko",
                                                            html.Br(), html.Small(" (Honorific)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_honorific',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_honorific',
                                                        placeholder = 'Example: Mr., Mrs., Ms., Dr.'
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Mga pronoun",
                                                            html.Br(), html.Small(" (Pronouns)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_pronouns',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_pronouns',
                                                        placeholder = 'Example: she/her, he/him, they/them'
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                )
                                            ], class_name = row_m
                                        )
                                    ], className = div_m
                                ),
                                html.Hr(),
                                # Employment information
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-briefcase-fill me-2'),
                                                        "Detalye san trabaho",
                                                        html.Small(" (Work information)", className = 'text-muted')
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        "Alayon paghatag san mga detalye san imo puwesto o katungdanan sa lokal nga gobyerno.",
                                                        html.Br(),
                                                        html.Small(
                                                            [
                                                                "(Please provide the details of your position or designation in the local government.)",
                                                            ],
                                                            className = 'text-muted'
                                                        )
                                                    ], className = p_m
                                                )
                                            ], class_name = row_m
                                        ),
                                        # Office
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            #html.I(className = 'bi bi-telephone me-2'),
                                                            "Opisina", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Office)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_office_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_office_id',
                                                        clearable = True,
                                                        placeholder = "Pili (select)..."
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                )
                                            ], class_name = row_m
                                        ),
                                        # Designation
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            #html.I(className = 'bi bi-envelope-at me-2'),
                                                            "Puwesto/katungdánan", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Position/designation)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_designation',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type= 'text',
                                                        id = 'usr_reg_input_designation',
                                                        placeholder = 'Example: City Councilor, Barangay Captain, Administrative Aide I',
                                                        invalid = False
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                ),
                                            ], class_name = row_m
                                        )
                                    ], className = div_m
                                ),
                                html.Hr(),
                                # Contact information
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-telephone-fill me-2'),
                                                        "Contact information",
                                                        #html.Br(),
                                                        #html.Small(" (Basic information)", className = 'text-muted')
                                                    ]
                                                ),
                                            ], class_name = row_m
                                        ),
                                        # Contact number and email
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            #html.I(className = 'bi bi-telephone me-2'),
                                                            "Numero sa cellphone/telepono", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Contact number)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_contactnum',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_contactnum',
                                                        placeholder = '09XXXXXXXXX',
                                                        invalid = False
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            #html.I(className = 'bi bi-envelope-at me-2'),
                                                            "Email address"
                                                        ],
                                                        id = 'usr_reg_label_email',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type= 'text',
                                                        id = 'usr_reg_input_email',
                                                        placeholder = 'example@website.com',
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                            ], class_name = row_m
                                        ),
                                        # Facebook
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            #html.I(className = 'bi bi-facebook me-2'),
                                                            "Ngaran sa Facebook", html.Br(),
                                                            html.Small(" (Facebook name)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_facebbok',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-0 mb-md-2 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_facebook',
                                                        placeholder = 'Ngaran sa Facebook (Facebook name)',
                                                    ),
                                                    class_name = 'align-self-center mb-0 mb-md-2 col-12 col-md-9'
                                                ),
                                            ], class_name = row_m
                                        )
                                    ], className = div_m
                                ),
                                html.Hr(),
                                # Present address
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-pin-map-fill me-2'),
                                                        "Adlaw-adlaw nga gin-iistaran",
                                                        #html.Br(),
                                                        html.Small(" (Present address)", className = 'text-muted')
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        "Asya ini an imo adlaw-adlaw nga urkuyan nga imo gin-uulian pagkatapos trabaho. Puwede ini maiba sa imo ",
                                                        html.B("permanente nga gin-iistaran"),
                                                        " nga nakasurat sa imo mga ID, lisensiya, o iba nga legal o opisyal nga papeles.",
                                                        html.Br(),
                                                        html.Small(
                                                            [
                                                                "(This is your everyday residence where you go home after work. This can differ from your ",
                                                                html.B("permanent residence"),
                                                                " which is written on your IDs, licenses, or other legal or official documents.)"
                                                            ],
                                                            className = 'text-muted'
                                                        )
                                                    ], className = p_m
                                                )
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Rehiyon", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Region)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_present_region_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_present_region_id',
                                                        clearable = True,
                                                        placeholder = "Pili (select)..."
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
                                                            "Probinsya", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Province)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_present_province_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_present_province_id',
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
                                                            "Siyudad/bungto", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (City/municipality)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_present_citymun_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_present_citymun_id',
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
                                                            "Barangay",  usr_reg_tag_required,
                                                        ],
                                                        id = 'usr_reg_label_present_brgy_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_present_brgy_id',
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
                                                            "Kalsada", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Street)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_present_street',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_present_street',
                                                        placeholder = 'House No., Lot No., Block No., Street/Road, Village/Subdivision, Purok/Sitio',
                                                        disabled = True,
                                                        invalid = False
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                ),
                                            ],
                                            class_name = row_m
                                        ),
                                    ], className = div_m
                                ),
                                # Permanent address
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-house-fill me-2'),
                                                        "Permanente nga gin-iistaran",
                                                        #html.Br(),
                                                        html.Small(" (Permanent address)", className = 'text-muted')
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        """Asya ini an imo permanente nga urkuyan nga nakasurat sa imo mga ID,
                                                        lisensiya, o iba nga mga legal o opisyal nga papeles.""",
                                                        html.Br(),
                                                        html.Small(
                                                            [
                                                                """(This is your permanent residence that is written on your IDs,
                                                                licenses, or other legal or official documents.)"""
                                                            ],
                                                            className = 'text-muted'
                                                        )
                                                    ], className = p_m
                                                ),
                                                dbc.Checkbox(
                                                    id = "usr_reg_cbox_permanent_address",
                                                    label = [
                                                        "Pareho ini sa akon adlaw-adlaw nga gin-iistaran.", html.Small(" (Same as present address)", className = 'text-muted')
                                                    ],
                                                    value = False,
                                                    #style = {'display' : 'none'},
                                                    class_name = 'ms-3'
                                                )
                                            ], class_name = row_m
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        [
                                                            "Rehiyon", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Region)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_permanent_region_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_permanent_region_id',
                                                        clearable = True,
                                                        placeholder = "Pili (select)..."
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
                                                            "Probinsya", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Province)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_permanent_province_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_permanent_province_id',
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
                                                            "Siyudad/bungto", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (City/municipality)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_permanent_citymun_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_permanent_citymun_id',
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
                                                            "Barangay", usr_reg_tag_required,
                                                        ],
                                                        id = 'usr_reg_label_permanent_brgy_id',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id = 'usr_reg_input_permanent_brgy_id',
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
                                                            "Kalsada", usr_reg_tag_required, html.Br(),
                                                            html.Small(" (Street)", className = 'text-muted')
                                                        ],
                                                        id = 'usr_reg_label_permanent_street',
                                                        class_name = label_m
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-3'
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type = 'text',
                                                        id = 'usr_reg_input_permanent_street',
                                                        placeholder = 'House No., Lot No., Block No., Street/Road, Village/Subdivision, Purok/Sitio',
                                                        disabled = True,
                                                        invalid = False
                                                    ),
                                                    class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-9'
                                                ),
                                            ],
                                            class_name = row_m
                                        ),
                                    ], className = div_m
                                ),
                                html.Hr(),
                                # Register button
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Button(
                                                        [
                                                            html.I(className = 'bi bi-check-circle-fill me-2'),
                                                            "Rehistro (Register)"
                                                        ],
                                                        id = 'usr_reg_btn_submit',
                                                        style = {'width': ' 100%'},
                                                        type = 'submit'
                                                    ),
                                                    class_name = 'align-self-center col-md-3 mb-2'
                                                )
                                            ],
                                            class_name = 'justify-content-end'
                                        )
                                    ], className = footer_m
                                )
                            ]
                        ),
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
                                                html.H4("Complete your registration"),
                                                html.P(
                                                    [
                                                        """Alayon paghimo san imo password para mahuman imo pagrehistro.
                                                        Alayon liwat pagseguro nga sakto an ngatanan nga impormasyon nga imo ginhatag.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """(Please create your password to finish your registration.
                                                            Also, please ensure that the information that you're submitting is correct.)
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
                                                                id = 'usr_reg_alert_passwordvalidation_col_text'
                                                            )
                                                        ]
                                                    ),
                                                    id = 'usr_reg_alert_passwordvalidation',
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
                                                    id = 'usr_reg_input_password_initial',
                                                    placeholder = ['Enter password'],
                                                    invalid = False
                                                ),
                                            ]
                                        )
                                    ], class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'password',
                                                    id = 'usr_reg_input_password_confirm',
                                                    placeholder = ['Confirm password'],
                                                    invalid = False
                                                ),
                                            ]
                                        )
                                    ], class_name = label_m
                                )
                            ],
                            id = 'usr_reg_modal_confirm_body'
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
                                                id = 'usr_reg_btn_confirm',
                                                style = {'width': ' 100%'},
                                                type = 'submit'
                                            ),
                                            class_name = 'align-self-center col-12 col-md-auto'
                                        )
                                    ],
                                    class_name = 'justify-content-end'
                                )
                            ],
                            id = 'usr_reg_modal_confirm_footer'
                        )
                    ]
                )
            ],
            id = 'usr_reg_modal_confirm',
            is_open = False,
            centered = True,
            scrollable = True,
            backdrop = True,
            #size = 'lg',
        ),
        dbc.Modal(
            [
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H4("Success!"),
                                        html.P(
                                            [
                                                """Narehistro na an imo account.""",
                                                html.Br(),
                                                html.Small(
                                                    """(Your account has been registered.)
                                                    """,
                                                    className = 'text-muted'
                                                )
                                            ], className = p_m
                                        ),
                                    ]
                                )
                            ], class_name = 'mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        [
                                            html.I(className = 'bi bi-person-vcard-fill me-2'),
                                            "Kadto sa profile", html.Br(),
                                            html.Small("(Go to profile)")
                                        ],
                                        id = 'usr_reg_btn_newprofile',
                                        color = 'primary',
                                        outline = True,
                                        style = {'width': ' 100%'},
                                        external_link = True
                                    ),
                                    class_name = 'align-self-center mb-2 col-12 col-md-4'
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        [
                                            html.I(className = 'bi bi-arrow-clockwise me-2'),
                                            "Pag-rehistro bag-o", html.Br(),
                                            html.Small("(Register another user)")
                                        ],
                                        id = 'usr_reg_btn_newreg',
                                        color = 'primary',
                                        outline = True,
                                        style = {'width': ' 100%'},
                                        href = '/users/register',
                                        external_link = True
                                    ),
                                    class_name = 'align-self-center mb-2 col-12 col-md-4'
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        [
                                            html.I(className = 'bi bi-arrow-return-left me-2'),
                                            "Balik sa dashboard", html.Br(),
                                            html.Small("(Return to dashboard)")
                                        ],
                                        id = 'usr_reg_btn_return',
                                        color = 'primary',
                                        outline = False,
                                        style = {'width': ' 100%'},
                                        href = '/dashboard',
                                        external_link = True
                                    ),
                                    class_name = 'align-self-center mb-0 col-12 col-md-4'
                                )
                            ]
                        )
                    ]
                ),
            ],
            id = 'usr_reg_modal_regsuccess',
            is_open = False,
            centered = True,
            backdrop = 'static',
            keyboard = False,
            scrollable = True,
            size = 'lg'
        )
    ]
)

usr_reg_url_pathname = '/users/register'

# Callback for populating regions and other basic dropdown menus
@app.callback(
    [
        Output('usr_reg_input_present_region_id', 'options'),
        Output('usr_reg_input_permanent_region_id', 'options'),
        Output('usr_reg_input_assignedsex_id', 'options'),
        Output('usr_reg_input_office_id', 'options'),
        Output('usr_reg_input_usertype_id', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)

def usr_reg_populatedropdowns(pathname):
    if pathname == usr_reg_url_pathname:
        dropdowns = []

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
        dropdowns.append(regions)

        # Assgined sex
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.assignedsex
        """
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        sexes = df.to_dict('records')
        dropdowns.append(sexes)

        # Offices
        #sql = """SELECT COALESCE(NULLIF(label, ''), name) AS label, id AS value
        sql = """SELECT name AS label, id AS value
        FROM utilities.office
        """
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        offices = df.to_dict('records')
        dropdowns.append(offices)

        # User types
        #sql = """SELECT COALESCE(NULLIF(label, ''), name) AS label, id AS value
        sql = """SELECT label AS label, id AS value
        FROM utilities.usertype
        """
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        usertypes = df.to_dict('records')
        dropdowns.append(usertypes)

        return dropdowns
    else:
        raise PreventUpdate

# Callback for setting permanent region as present region when checkbox is selected
@app.callback(
    [
        Output('usr_reg_input_permanent_region_id', 'value'),
        Output('usr_reg_input_permanent_region_id', 'disabled')
    ],
    [
        Input('usr_reg_cbox_permanent_address', 'value')
    ],
    [
        State('usr_reg_input_present_region_id', 'value')
    ],
    prevent_initial_call = True
)

def usr_reg_sameregion(cbox, region):
    if cbox: return [region, True]
    else: return [None, False]

# Callback for populating present provinces once present region is selected
@app.callback(
    [
        Output('usr_reg_input_present_province_id', 'options'),
        Output('usr_reg_input_present_province_id', 'disabled'),
        Output('usr_reg_input_present_province_id', 'value'),
    ],
    [
        Input('usr_reg_input_present_region_id', 'value'),
    ],
    prevent_initial_call = True
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

# Callback for populating permanent provinces once permanent region is selected
@app.callback(
    [
        Output('usr_reg_input_permanent_province_id', 'options'),
        Output('usr_reg_input_permanent_province_id', 'disabled'),
        Output('usr_reg_input_permanent_province_id', 'value'),
    ],
    [
        Input('usr_reg_input_permanent_region_id', 'value'),
        Input('usr_reg_cbox_permanent_address', 'value'),
    ],
    [
        State('usr_reg_input_present_province_id', 'value')
    ],
    prevent_initial_call = True
)

def usr_reg_populatepermanentprovinces(region, cbox, present_province):
    provinces = []
    disabled = True
    value = None
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
        if cbox: value = present_province
        else: disabled = False
    return [provinces, disabled, value]

# Callback for populating present cities/municipalities once present province is selected
@app.callback(
    [
        Output('usr_reg_input_present_citymun_id', 'options'),
        Output('usr_reg_input_present_citymun_id', 'disabled'),
        Output('usr_reg_input_present_citymun_id', 'value'),
    ],
    [
        Input('usr_reg_input_present_region_id', 'value'),
        Input('usr_reg_input_present_province_id', 'value'),
    ],
    prevent_initial_call = True
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

# Callback for populating permanent cities/municipalities once permanent province is selected
@app.callback(
    [
        Output('usr_reg_input_permanent_citymun_id', 'options'),
        Output('usr_reg_input_permanent_citymun_id', 'disabled'),
        Output('usr_reg_input_permanent_citymun_id', 'value'),
    ],
    [
        Input('usr_reg_input_permanent_region_id', 'value'),
        Input('usr_reg_input_permanent_province_id', 'value'),
        Input('usr_reg_cbox_permanent_address', 'value'),
    ],
    [
        State('usr_reg_input_present_citymun_id', 'value')
    ],
    prevent_initial_call = True
)

def usr_reg_populatepermanentcitymuns(region, province, cbox, present_citymun):
    citymun = []
    disabled = True
    value = None
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
        if cbox: value = present_citymun
        else: disabled = False
    return [citymun, disabled, value]

# Callback for populating present barangays once present city/municipality is selected
@app.callback(
    [
        Output('usr_reg_input_present_brgy_id', 'options'),
        Output('usr_reg_input_present_brgy_id', 'disabled'),
        Output('usr_reg_input_present_brgy_id', 'value'),
    ],
    [
        Input('usr_reg_input_present_region_id', 'value'),
        Input('usr_reg_input_present_province_id', 'value'),
        Input('usr_reg_input_present_citymun_id', 'value'),
    ],
    prevent_initial_call = True
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

# Callback for populating permanent barangays once permanent city/municipality is selected
@app.callback(
    [
        Output('usr_reg_input_permanent_brgy_id', 'options'),
        Output('usr_reg_input_permanent_brgy_id', 'disabled'),
        Output('usr_reg_input_permanent_brgy_id', 'value'),
    ],
    [
        Input('usr_reg_input_permanent_region_id', 'value'),
        Input('usr_reg_input_permanent_province_id', 'value'),
        Input('usr_reg_input_permanent_citymun_id', 'value'),
        Input('usr_reg_cbox_permanent_address', 'value'),
    ],
    [
        State('usr_reg_input_present_brgy_id', 'value')
    ],
    prevent_initial_call = True
)

def usr_reg_populatepermanentbrgys(region, province, citymun, cbox, present_brgy):
    brgy = []
    disabled = True
    value = None
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
        if cbox: value = present_brgy
        else: disabled = False
    return [brgy, disabled, value]

# Callback for enabling present street address once present city/municipality is selected
@app.callback(
    [
        Output('usr_reg_input_present_street', 'disabled'),
        Output('usr_reg_input_present_street', 'value'),
    ],
    [
        Input('usr_reg_input_present_region_id', 'value'),
        Input('usr_reg_input_present_province_id', 'value'),
        Input('usr_reg_input_present_citymun_id', 'value'),
        Input('usr_reg_input_present_brgy_id', 'value'),
    ],
    prevent_initial_call = True
)

def usr_reg_enablepresentstreet(region, province, citymun, brgy):
    disabled = True
    if region and province and citymun and brgy: disabled = False
    return [disabled, None]

# Callback for enabling permanent street address once permanent city/municipality is selected
@app.callback(
    [
        Output('usr_reg_input_permanent_street', 'disabled'),
        Output('usr_reg_input_permanent_street', 'value'),
    ],
    [
        Input('usr_reg_input_permanent_region_id', 'value'),
        Input('usr_reg_input_permanent_province_id', 'value'),
        Input('usr_reg_input_permanent_citymun_id', 'value'),
        Input('usr_reg_input_permanent_brgy_id', 'value'),
        Input('usr_reg_cbox_permanent_address', 'value'),
    ],
    [
        State('usr_reg_input_present_street', 'value')
    ],
    prevent_initial_call = True
)

def usr_reg_enablepermanentstreet(region, province, citymun, brgy, cbox, present_street):
    disabled = True
    value = None
    if region and province and citymun and brgy:
        if cbox: value = present_street
        else: disabled = False
    return [disabled, value]

# Callback for generating usernames
@app.callback(
    [
        Output('usr_reg_input_username', 'value')
    ],
    [
        Input('usr_reg_input_fname', 'value'),
        Input('usr_reg_input_livedname', 'value'),
        Input('usr_reg_input_mname', 'value'),
        Input('usr_reg_input_lname', 'value'),
    ]
)

def usr_reg_generateusername(fname, livedname, mname, lname):
    if fname and lname:
        username = ''

        # Generate first character between lived name and first name
        if livedname: username += livedname[0]
        else: username += fname[0]

        # Generate second character using middle name (if any)
        if mname: username += mname[0]

        # Complete username with last name
        username += lname
        username = username.replace(" ", "")
        username = username.replace("-", "")
        #user_username = user_username.replace("ñ", "n")

        # Search database for similar usernames
        sql = """SELECT username
            FROM users.user
            WHERE username LIKE %s;
        """
        values = [f"%{username.lower()}%"]
        cols = ['username']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df[df['username'] == username.lower()]

        if not df.empty:
            lastchar = df.tail().values[0][0][-1]
            if lastchar.isnumeric():
                return [username.lower()+str(int(lastchar)+1)]
            else:
                return [username.lower()+"1"]
        else:
            return [username.lower()]
    else: raise PreventUpdate

# Callback for generating an alert when changing user type
@app.callback(
    [
        Output('usr_reg_row_usertype', 'class_name'),
        Output('usr_reg_row_alert_usertype', 'class_name'),
        Output('usr_reg_alert_usertype', 'is_open'),
        Output('usr_reg_alert_usertype', 'color'),
        Output('usr_reg_alert_usertype_text_war', 'children'),
        Output('usr_reg_alert_usertype_text_en', 'children')
    ],
    [
        Input('usr_reg_input_usertype_id', 'value')
    ],
    prevent_initial_call = True
)

def usr_reg_displayusertypealert(usertype):
    above_class_name = None
    class_name = None
    is_open = False
    color = None
    war = ''
    en = '('
    if usertype and usertype > 1:
        sql = """SELECT alert_war AS war, alert_en AS en, alert_color AS color
        FROM utilities.usertype WHERE id = %s;
        """
        values = [usertype]
        cols = ['war', 'en', 'color']
        df = db.querydatafromdatabase(sql, values, cols)
        above_class_name = 'mb-3'
        class_name = 'mb-3'
        is_open = True
        color = df['color'][0]
        war = df['war']
        en += df['en'] + ")"
    return [above_class_name, class_name, is_open, color, war, en]

# Callback for confirming registration
@app.callback(
    [
        # Modal
        Output('usr_reg_modal_confirm', 'is_open'),
        #Output('usr_reg_modal_confirm_body', 'children'),
        # Overall validation alert
        Output('usr_reg_alert_inputvalidation', 'is_open'),
        Output('usr_reg_alert_inputvalidation', 'class_name'),
        Output('usr_reg_alert_inputvalidation_span_missing', 'children'),
        # Name validation alert
        Output('usr_reg_alert_namevalidation', 'is_open'),
        Output('usr_reg_alert_namevalidation', 'class_name'),
        # Input validation
        Output('usr_reg_input_fname', 'invalid'),
        Output('usr_reg_input_lname', 'invalid'),
        Output('usr_reg_input_designation', 'invalid'),
        Output('usr_reg_input_contactnum', 'invalid'),
        Output('usr_reg_input_present_street', 'invalid'),
        Output('usr_reg_input_permanent_street', 'invalid')
    ],
    [
        Input('usr_reg_btn_submit', 'n_clicks')
    ],
    [
        # User type
        State('usr_reg_input_usertype_id', 'value'), # REQUIRED
        # Basic information
        State('usr_reg_input_fname', 'value'), # REQUIRED
        State('usr_reg_input_mname', 'value'),
        State('usr_reg_input_lname', 'value'), # REQUIRED
        State('usr_reg_input_username', 'value'),
        State('usr_reg_input_birthdate', 'date'), # REQUIRED
        State('usr_reg_input_assignedsex_id', 'value'), # REQUIRED
        # Affirmative identity
        State('usr_reg_input_livedname', 'value'),
        State('usr_reg_input_honorific', 'value'),
        State('usr_reg_input_pronouns', 'value'),
        # Work information
        State('usr_reg_input_office_id', 'value'), # REQUIRED
        State('usr_reg_input_designation', 'value'), # REQUIRED
        # Contact information
        State('usr_reg_input_contactnum', 'value'), # REQUIRED
        State('usr_reg_input_email', 'value'),
        State('usr_reg_input_facebook', 'value'),
        # Present address
        State('usr_reg_input_present_region_id', 'value'), # REQUIRED
        State('usr_reg_input_present_province_id', 'value'), # REQUIRED
        State('usr_reg_input_present_citymun_id', 'value'), # REQUIRED
        State('usr_reg_input_present_brgy_id', 'value'), # REQUIRED
        State('usr_reg_input_present_street', 'value'), # REQUIRED
        # Permanent address
        State('usr_reg_input_permanent_region_id', 'value'), # REQUIRED
        State('usr_reg_input_permanent_province_id', 'value'), # REQUIRED
        State('usr_reg_input_permanent_citymun_id', 'value'), # REQUIRED
        State('usr_reg_input_permanent_brgy_id', 'value'), # REQUIRED
        State('usr_reg_input_permanent_street', 'value'), # REQUIRED
    ],
    prevent_initial_call = True
)

def usr_reg_confirmregistration(
    btn, usertype_id,
    # Basic information
    fname, mname, lname, username, birthdate, assignedsex_id,
    # Affirmative identity
    livedname, honorific, pronouns,
    # Work information
    office_id, designation,
    # Contact information
    contactnum, email, facebook,
    # Present address
    present_region_id, present_province_id, present_citymun_id, present_brgy_id, present_street,
    # Permanent address
    permanent_region_id, permanent_province_id, permanent_citymun_id, permanent_brgy_id, permanent_street,
):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'usr_reg_btn_submit' and btn:
            # Modal
            modal_open = False
            modal_body = ''
            # Overall validation alert
            alert_open = False
            alert_class_name = None
            alert_span = []
            # Name validation alert
            alert_name_open = False
            alert_name_class_name = None
            # Input validation
            fname_invalid = False
            lname_invalid = False
            designation_invalid = False
            contactnum_invalid = False
            present_street_invalid = False
            permanent_street_invalid = False

            sql = """SELECT id FROM users.user
            WHERE fname = %s AND mname = %s AND lname = %s;
            """
            values = [fname, mname, lname]
            cols = ['id']
            df = db.querydatafromdatabase(sql, values, cols)
            if not df.empty:
                alert_name_open = True
                alert_name_class_name = 'mb-3'
            
            if (not(usertype_id) or not(fname) or not(lname) or not (birthdate) or not (assignedsex_id)
                or not(office_id) or not(designation) or not (contactnum)
                or not(present_region_id) or not (present_province_id) or not (present_citymun_id) or not(present_brgy_id) or not(present_street)
                or not(permanent_region_id) or not (permanent_province_id) or not (permanent_citymun_id) or not(permanent_brgy_id) or not(permanent_street)
            ):
                alert_open = True
                alert_class_name = 'mb-3'
                if not(usertype_id):
                    # Add input validation here
                    alert_span += html.Li(
                        [
                            "Klase san magamit", html.Br(),
                            html.Small(" (User type)", className = 'ms-3 text-muted'),
                        ]
                    ),
                if not(fname):
                    fname_invalid = True
                    alert_span += html.Li(
                        [
                            "Primero nga ngaran", html.Br(),
                            html.Small(" (First name)", className = 'ms-3 text-muted'),
                        ]
                    ),
                if not(lname):
                    lname_invalid = True
                    alert_span += html.Li(
                        [
                            "Apelyido", html.Br(),
                            html.Small(" (Last name)", className = 'ms-3 text-muted'),
                        ]
                    ),
                if not(birthdate):
                    # Add input validation here
                    alert_span += html.Li(
                        [
                            "Petsa san pagkatawo", html.Br(),
                            html.Small(" (Date of birth)", className = 'ms-3 text-muted'),
                        ]
                    ),
                if not(assignedsex_id):
                    # Add input validation here
                    alert_span += html.Li(
                        [
                            "Natawo nga babayi/lalaki", html.Br(),
                            html.Small(" (Sex assigned at birth)", className = 'ms-3 text-muted'),
                        ]
                    ),
                if not(office_id):
                    # Add input validation here
                    alert_span += html.Li(
                        [
                            "Opisina", html.Br(),
                            html.Small(" (Office)", className = 'ms-3 text-muted'),
                        ]
                    ),
                if not(designation):
                    designation_invalid = True
                    alert_span += html.Li(
                        [
                            "Puwesto/katungdánan", html.Br(),
                            html.Small(" (Position/designation)", className = 'ms-3 text-muted'),
                        ]
                    ),
                if not(contactnum):
                    contactnum_invalid = True
                    alert_span += html.Li(
                        [
                            "Numero sa cellphone/telepono", html.Br(),
                            html.Small(" (Contact number)", className = 'ms-3 text-muted'),
                        ]
                    ),
                if not(present_region_id) or not(present_province_id) or not (present_citymun_id) or not (present_brgy_id) or not (present_street):
                    # Add input validation here
                    present_street_invalid = True
                    text_war = 'Adlaw-adlaw nga gin-iistaran: '
                    text_en = 'Present address: '
                    len = 0
                    if not present_region_id:
                        text_war += 'Rehiyon'
                        text_en += 'Region'
                        len += 1
                    if not present_province_id:
                        if len > 0:
                            text_war += ', '
                            text_en += ', '
                        text_war += 'Probinsya'
                        text_en += 'Province'
                        len += 1
                    if not present_citymun_id:
                        if len > 0:
                            text_war += ', '
                            text_en += ', '
                        text_war += 'Siyudad/bungto'
                        text_en += 'City/municipality'
                        len += 1
                    if not present_brgy_id:
                        if len > 0:
                            text_war += ', '
                            text_en += ', '
                        text_war += 'Barangay'
                        text_en += 'Barangay'
                        len += 1
                    if not present_street:
                        if len > 0:
                            text_war += ', '
                            text_en += ', '
                        text_war += 'Kalsada'
                        text_en += 'Street'
                        len += 1
                    alert_span.append(
                        html.Li(
                            [
                                text_war, html.Br(),
                                html.Small(" (%s)" % text_en, className = 'ms-3 text-muted')
                            ]
                        )
                    )
                if not(permanent_region_id) or not(permanent_province_id) or not (permanent_citymun_id) or not (permanent_brgy_id) or not (permanent_street):
                    # Add input validation here
                    permanent_street_invalid = True
                    text_war = 'Permanente nga gin-iistaran: '
                    text_en = 'Permanent address: '
                    len = 0
                    if not permanent_region_id:
                        text_war += 'Rehiyon'
                        text_en += 'Region'
                        len += 1
                    if not permanent_province_id:
                        if len > 0:
                            text_war += ', '
                            text_en += ', '
                        text_war += 'Probinsya'
                        text_en += 'Province'
                        len += 1
                    if not permanent_citymun_id:
                        if len > 0:
                            text_war += ', '
                            text_en += ', '
                        text_war += 'Siyudad/bungto'
                        text_en += 'City/municipality'
                        len += 1
                    if not permanent_brgy_id:
                        if len > 0:
                            text_war += ', '
                            text_en += ', '
                        text_war += 'Barangay'
                        text_en += 'Barangay'
                        len += 1
                    if not permanent_street:
                        if len > 0:
                            text_war += ', '
                            text_en += ', '
                        text_war += 'Kalsada'
                        text_en += 'Street'
                        len += 1
                    alert_span.append(
                        html.Li(
                            [
                                text_war, html.Br(),
                                html.Small(" (%s)" % text_en, className = 'ms-3 text-muted')
                            ]
                        )
                    )
            else:
                modal_open = True
            return [
                # Modal
                modal_open, #modal_body,
                # Overall validation alert
                alert_open, alert_class_name, alert_span,
                # Name validation alert
                alert_name_open, alert_name_class_name,
                # Input validation
                fname_invalid, lname_invalid, designation_invalid, contactnum_invalid, present_street_invalid, permanent_street_invalid
            ]
        else: raise PreventUpdate
    else: raise PreventUpdate

# Callback for creating new user
@app.callback(
    [
        #Output('url', 'pathname'),
        # Success modal
        #Output('usr_reg_modal_regsuccess', 'is_open'),
        Output('usr_reg_store_regsuccess', 'data'),
        # Alert
        Output('usr_reg_alert_passwordvalidation', 'is_open'),
        Output('usr_reg_alert_passwordvalidation', 'class_name'),
        Output('usr_reg_alert_passwordvalidation', 'color'),
        Output('usr_reg_alert_passwordvalidation_col_text', 'children'),
        # Input validation
        Output('usr_reg_input_password_initial', 'invalid'),
        Output('usr_reg_input_password_confirm', 'invalid')
    ],
    [
        Input('usr_reg_btn_confirm', 'n_clicks')
    ],
    [
        # Password
        State('usr_reg_input_password_initial', 'value'), # REQUIRED
        State('usr_reg_input_password_confirm', 'value'), # REQUIRED
        # User type
        State('usr_reg_input_usertype_id', 'value'), # REQUIRED
        # Basic information
        State('usr_reg_input_fname', 'value'), # REQUIRED
        State('usr_reg_input_mname', 'value'),
        State('usr_reg_input_lname', 'value'), # REQUIRED
        State('usr_reg_input_username', 'value'),
        State('usr_reg_input_birthdate', 'date'), # REQUIRED
        State('usr_reg_input_assignedsex_id', 'value'), # REQUIRED
        # Affirmative identity
        State('usr_reg_input_livedname', 'value'),
        State('usr_reg_input_honorific', 'value'),
        State('usr_reg_input_pronouns', 'value'),
        # Work information
        State('usr_reg_input_office_id', 'value'), # REQUIRED
        State('usr_reg_input_designation', 'value'), # REQUIRED
        # Contact information
        State('usr_reg_input_contactnum', 'value'), # REQUIRED
        State('usr_reg_input_email', 'value'),
        State('usr_reg_input_facebook', 'value'),
        # Present address
        State('usr_reg_input_present_region_id', 'value'), # REQUIRED
        State('usr_reg_input_present_province_id', 'value'), # REQUIRED
        State('usr_reg_input_present_citymun_id', 'value'), # REQUIRED
        State('usr_reg_input_present_brgy_id', 'value'), # REQUIRED
        State('usr_reg_input_present_street', 'value'), # REQUIRED
        # Permanent address
        State('usr_reg_input_permanent_region_id', 'value'), # REQUIRED
        State('usr_reg_input_permanent_province_id', 'value'), # REQUIRED
        State('usr_reg_input_permanent_citymun_id', 'value'), # REQUIRED
        State('usr_reg_input_permanent_brgy_id', 'value'), # REQUIRED
        State('usr_reg_input_permanent_street', 'value'), # REQUIRED
    ],
    prevent_initial_call = True
)

def usr_reg_submitregistration(
    btn,
    # Password
    password_initial, password_confirm,
    # User type
    usertype_id,
    # Basic information
    fname, mname, lname, username, birthdate, assignedsex_id,
    # Affirmative identity
    livedname, honorific, pronouns,
    # Work information
    office_id, designation,
    # Contact information
    contactnum, email, facebook,
    # Present address
    present_region_id, present_province_id, present_citymun_id, present_brgy_id, present_street,
    # Permanent address
    permanent_region_id, permanent_province_id, permanent_citymun_id, permanent_brgy_id, permanent_street,
):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'usr_reg_btn_confirm' and btn:
            success_modal = False
            reg_success = False
            #confirm_modal = True
            # Alert
            alert_open = False
            alert_class_name = None
            alert_color = None
            alert_col_text = None
            # Input validation
            password_initial_invalid = False
            password_confirm_invalid = False
            if not(password_initial) or not(password_confirm):
                alert_open = True
                alert_class_name = 'mb-3'
                alert_color = 'warning'
                if not(password_initial): password_initial_invalid = True
                if not(password_confirm): password_confirm_invalid = True
                if (not(password_initial) and not(password_confirm)) or (not(password_initial) and password_confirm):
                    alert_col_text = [
                        "Alayon paghimo san imo password.",
                        html.Br(),
                        html.Small(
                            "(Please create your password.)",
                            className = 'text-muted'
                        ),
                    ]
                else: #elif password_initial and not(password_confirm):
                    alert_col_text = [
                        "Alayon pagkumpirma san imo password.",
                        html.Br(),
                        html.Small(
                            "(Please confirm your password.)",
                            className = 'text-muted'
                        ),
                    ]
            elif password_initial != password_confirm:
                alert_open = True
                alert_class_name = 'mb-3'
                alert_color = 'warning'
                alert_col_text = [
                    "Dapat pareho an imo password sa duha nga patlang.",
                    html.Br(),
                    html.Small(
                        "(Your password in both fields must match.)",
                        className = 'text-muted'
                    ),
                ]
            elif len(password_initial) < 8:
                alert_open = True
                alert_class_name = 'mb-3'
                alert_color = 'warning'
                alert_col_text = [
                    "Dapat diri kulang san walo (8) nga mga letra, numero, o simbolo an imo password.",
                    html.Br(),
                    html.Small(
                        "(Your password should have a minimum of eight (8) characters.)",
                        className = 'text-muted'
                    ),
                ]
            else:
                success_modal = True
                reg_success = True
                #confirm_modal = False
                alert_open = True
                alert_class_name = 'mb-3'
                alert_color = 'success'
                alert_col_text = [
                    "Nakarawat an imo password. Ibabalyo ka na sa imo profile.",
                    html.Br(),
                    html.Small(
                        "(Your password has been accepted. You will be redirected to your profile.)",
                        className = 'text-muted'
                    ),
                ]
                #url = '/users/profile?id=%s' % 1 # Note: add code for determing latest id number to grant
                regsuccess = True
                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
                sql = """INSERT INTO users.user (usertype_id, password,
                    fname, mname, lname, username, birthdate, assignedsex_id,
                    livedname, honorific, pronouns, office_id, designation,
                    contactnum, email, facebook,
                    present_region_id, present_province_id, present_citymun_id, present_brgy_id, present_street,
                    permanent_region_id, permanent_province_id, permanent_citymun_id, permanent_brgy_id, permanent_street)
                    VALUES (%s, %s,
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s)
                """
                values = [
                    usertype_id, encrypt_string(password_initial),
                    # Basic information
                    fname, mname, lname, username, birthdate, assignedsex_id,
                    # Affirmative identity
                    livedname, honorific, pronouns,
                    # Work information
                    office_id, designation,
                    # Contact information
                    contactnum, email, facebook,
                    # Present address
                    present_region_id, present_province_id, present_citymun_id, present_brgy_id, present_street,
                    # Permanent address
                    permanent_region_id, permanent_province_id, permanent_citymun_id, permanent_brgy_id, permanent_street,
                ]
                db.modifydatabase(sql, values)
            return [
                #success_modal,
                reg_success, #confirm_modal,
                alert_open, alert_class_name, alert_color, alert_col_text,
                password_initial_invalid, password_confirm_invalid
            ]
        else: raise PreventUpdate
    else: raise PreventUpdate