# FIX THIS ERROR
# When you input permanent address first and add present address later
# details in permanent address fields disappear.

# Dash related dependencies
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# App definition
from app import app
from apps import dbconnect as db

user_reg_tag_required = html.Sup("*", className = 'text-danger')

layout = html.Div(
    [
        dbc.Row(
            [
                # Enter offcanvas here?
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H1("User Registration"),
                                        html.P(
                                            [
                                                "Kinihanglan pun-on an mga patlang nga may pula nga asterisk ", user_reg_tag_required, ".",
                                                html.Br(),
                                                html.Small(
                                                    ["(Fields with red asterisks ", user_reg_tag_required, " are required.)"],
                                                    className = 'text-muted'
                                                )
                                            ]
                                        )
                                    ],
                                    id = 'user_reg_div_header'
                                ),
                                dbc.Row(
                                    [

                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "User type", user_reg_tag_required,
                                                    #html.Br(), html.Small(" (Sex assigned at birth)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_usertype_id',
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_usertype_id',
                                                clearable = True
                                            ),
                                            class_name = 'align-self-center mb-1 col-12 col-md-9'
                                        ),
                                    ], className = 'mb-3',
                                    id = 'user_reg_div_usertype'
                                )
                            ]
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
                                        #html.P("""The City Government seeks to promote and protect the ability of its employees to
                                        #    freely express their sexual orientation, gender identity, and expression (SOGIE).
                                        #    Everyone is enjoined to fill out these details whenever applicable.
                                        #""")
                                    ], class_name = 'mb-1'
                                ),
                                # Name
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Ngaran", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Name)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_name'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_fname',
                                                placeholder = ['Primero (First name)']
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_mname',
                                                placeholder = 'Butnga (Middle name)'
                                            ),
                                            md = 3, sm = 12,
                                            class_name = ' align-self-center mb-2 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_lname',
                                                placeholder = 'Apelyido (Last name)'
                                            ),
                                            md = 3, sm = 12,
                                            class_name = 'align-self-center mb-2 col-12 col-md-3'
                                        ),
                                    ],
                                    id = 'user_reg_div_name',
                                    class_name = 'mb-1'
                                ),
                                # Username
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                "Username",
                                                id = 'user_reg_label_username',
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_username',
                                                placeholder = 'Username',
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        ),
                                        dbc.Tooltip(
                                            "Usernames are automatically generated.",
                                            target = 'user_reg_label_username'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                # Birthdate and sex assigned at birth
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Petsa san pagkatawo", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Date of birth)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_birthdate',
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                            #class_name = 'col-md-2 col-sm-11 col-xs-11 mb-3'
                                        ),
                                        dbc.Col(
                                            dcc.DatePickerSingle(
                                                id = 'user_reg_input_birthdate',
                                                placeholder = 'MM/DD/YYYY',
                                                #month_format = 'MMM Do, YYYY',
                                                clearable = True,
                                                #style = {'width' : '100%'}
                                                className = 'w-100'
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Natawo nga babayi/lalaki", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Sex assigned at birth)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_assignedsex',
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                            #class_name = 'col-md-2 col-sm-11 col-xs-11 mb-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_assignedsex_id',
                                                clearable = True
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-3'
                                        ),
                                    ], class_name = 'mb-1'
                                )
                            ], className = 'mb-3'
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
                                            ]
                                        ),
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                "Lived name",
                                                id = 'user_reg_label_livedname'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_livedname',
                                                placeholder = 'Lived name'
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                "Honorific",
                                                id = 'user_reg_label_honorific'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_honorific',
                                                placeholder = 'Example: Mr., Mrs., Ms., Dr.'
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                "Pronouns",
                                                id = 'user_reg_label_pronouns'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_pronouns',
                                                placeholder = 'Example: she/her, he/him, they/them'
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-3'
                                        )
                                    ], class_name = 'mb-1'
                                )
                            ], className = 'mb-3'
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
                                            ]
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                # Office
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    #html.I(className = 'bi bi-telephone me-2'),
                                                    "Opisina", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Office)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_office_id',
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_office_id',
                                                clearable = True,
                                                placeholder = "Pili (select)..."
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                # Designation
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    #html.I(className = 'bi bi-envelope-at me-2'),
                                                    "Puwesto/katungdánan", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Position/designation)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_designation',
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type= 'text',
                                                id = 'user_reg_input_designation',
                                                placeholder = 'Example: City Councilor, Barangay Captain, Administrative Aide I',
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        ),
                                    ], class_name = 'mb-1'
                                )
                            ], className = 'mb-3'
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
                                        #html.P("""The City Government seeks to promote and protect the ability of its employees to
                                        #    freely express their sexual orientation, gender identity, and expression (SOGIE).
                                        #    Everyone is enjoined to fill out these details whenever applicable.
                                        #""")
                                    ], class_name = 'mb-1'
                                ),
                                # Contact number and email
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    #html.I(className = 'bi bi-telephone me-2'),
                                                    "Numero sa cellphone/telepono", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Contact number)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_contactnum',
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_contactnum',
                                                placeholder = '09XXXXXXXXX',
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    #html.I(className = 'bi bi-envelope-at me-2'),
                                                    "Email address"
                                                ],
                                                id = 'user_reg_label_email',
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type= 'text',
                                                id = 'user_reg_input_email',
                                                placeholder = 'example@website.com',
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-3'
                                        ),
                                    ], class_name = 'mb-1'
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
                                                id = 'user_reg_label_facebbok',
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_facebook',
                                                placeholder = 'Ngaran sa Facebook (Facebook name)',
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        ),
                                    ], class_name = 'mb-1'
                                )
                            ], className = 'mb-3'
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
                                            ]
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Rehiyon", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Region)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_present_region_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_present_region_id',
                                                clearable = True,
                                                placeholder = "Pili (select)..."
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Probinsya", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Province)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_present_province_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_present_province_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Siyudad/Bungto", user_reg_tag_required, html.Br(),
                                                    html.Small(" (City/Municipality)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_present_citymun_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_present_citymun_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Barangay",  user_reg_tag_required,
                                                ],
                                                id = 'user_reg_label_present_brgy_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_present_brgy_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Kalsada", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Street)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_input_present_street'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_present_street',
                                                placeholder = 'Kalsada (Street)',
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        ),
                                    ],
                                    id = 'user_reg_div_name',
                                    class_name = 'mb-1'
                                ),
                            ], className = 'mb-3'
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
                                            ]
                                        ),
                                        dbc.Checkbox(
                                            id = "user_reg_cbox_permanent_address",
                                            label = [
                                                "Pareho ini sa akon adlaw-adlaw nga gin-iistaran.", html.Small(" (Same as present address)", className = 'text-muted')
                                            ],
                                            value = False,
                                            #style = {'display' : 'none'},
                                            class_name = 'ms-3'
                                        )
                                        #html.P("""The City Government seeks to promote and protect the ability of its employees to
                                        #    freely express their sexual orientation, gender identity, and expression (SOGIE).
                                        #    Everyone is enjoined to fill out these details whenever applicable.
                                        #""")
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Rehiyon", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Region)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_permanent_region_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_permanent_region_id',
                                                clearable = True,
                                                placeholder = "Pili (select)..."
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Probinsya", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Province)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_permanent_province_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_permanent_province_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Siyudad/Bungto", user_reg_tag_required, html.Br(),
                                                    html.Small(" (City/Municipality)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_label_permanent_citymun_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_permanent_citymun_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Barangay", user_reg_tag_required,
                                                ],
                                                id = 'user_reg_label_permanent_brgy_id'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'user_reg_input_permanent_brgy_id',
                                                clearable = True,
                                                placeholder = "Pili (select)...",
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        )
                                    ], class_name = 'mb-1'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Kalsada", user_reg_tag_required, html.Br(),
                                                    html.Small(" (Street)", className = 'text-muted')
                                                ],
                                                id = 'user_reg_input_permanent_street'
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-3'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'user_reg_input_permanent_street',
                                                placeholder = 'Kalsada (Street)',
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 col-12 col-md-9'
                                        ),
                                    ],
                                    id = 'user_reg_div_name',
                                    class_name = 'mb-1'
                                ),
                            ], className = 'mb-3'
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
                                                id = 'user_reg_btn_submit',
                                                style = {'width': ' 100%'}
                                            ),
                                            #md = 3, sm = 12,
                                            class_name = 'align-self-center col-md-3 mb-2'
                                        )
                                    ],
                                    class_name = 'justify-content-end'
                                )
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

user_reg_url_pathname = '/users/register'

# Callback for populating regions and other basic dropdown menus
@app.callback(
    [
        Output('user_reg_input_present_region_id', 'options'),
        Output('user_reg_input_permanent_region_id', 'options'),
        Output('user_reg_input_assignedsex_id', 'options'),
        Output('user_reg_input_office_id', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)

def user_reg_populatedropdowns(pathname):
    if pathname == user_reg_url_pathname:
        # Regions
        sql = """SELECT name as label, id as value
        FROM utilities.addressregion;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        regions = df.to_dict('records')

        # Assgined sex
        sql = """SELECT CONCAT(label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.assignedsex
        """
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        sexes = df.to_dict('records')

        # Assgined sex
        #sql = """SELECT CONCAT(label, ' | ', name) AS label, id AS value
        sql = """SELECT COALESCE(NULLIF(label, ''), name) AS label, id AS value
        FROM utilities.office
        """
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        offices = df.to_dict('records')
        return [regions, regions, sexes, offices]
    else:
        raise PreventUpdate

# Callback for setting permanent region as present region when checkbox is selected
@app.callback(
    [
        Output('user_reg_input_permanent_region_id', 'value'),
        Output('user_reg_input_permanent_region_id', 'disabled')
    ],
    [
        Input('user_reg_cbox_permanent_address', 'value')
    ],
    [
        State('user_reg_input_present_region_id', 'value')
    ]
)

def user_reg_sameregion(cbox, region):
    if cbox: return [region, True]
    else: return [None, False]

# Callback for populating present provinces once present region is selected
@app.callback(
    [
        Output('user_reg_input_present_province_id', 'options'),
        Output('user_reg_input_present_province_id', 'disabled'),
        Output('user_reg_input_present_province_id', 'value'),
    ],
    [
        Input('user_reg_input_present_region_id', 'value'),
    ]
)

def user_reg_populatepresentprovinces(region):
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
        Output('user_reg_input_permanent_province_id', 'options'),
        Output('user_reg_input_permanent_province_id', 'disabled'),
        Output('user_reg_input_permanent_province_id', 'value'),
    ],
    [
        Input('user_reg_input_permanent_region_id', 'value'),
        Input('user_reg_cbox_permanent_address', 'value'),
    ],
    [
        State('user_reg_input_present_province_id', 'value')
    ]
)

def user_reg_populatepermanentprovinces(region, cbox, present_province):
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
        Output('user_reg_input_present_citymun_id', 'options'),
        Output('user_reg_input_present_citymun_id', 'disabled'),
        Output('user_reg_input_present_citymun_id', 'value'),
    ],
    [
        Input('user_reg_input_present_region_id', 'value'),
        Input('user_reg_input_present_province_id', 'value'),
    ]
)

def user_reg_populatepresentcitymuns(region, province):
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
        Output('user_reg_input_permanent_citymun_id', 'options'),
        Output('user_reg_input_permanent_citymun_id', 'disabled'),
        Output('user_reg_input_permanent_citymun_id', 'value'),
    ],
    [
        Input('user_reg_input_permanent_region_id', 'value'),
        Input('user_reg_input_permanent_province_id', 'value'),
        Input('user_reg_cbox_permanent_address', 'value'),
    ],
    [
        State('user_reg_input_present_citymun_id', 'value')
    ]
)

def user_reg_populatepermanentcitymuns(region, province, cbox, present_citymun):
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
        Output('user_reg_input_present_brgy_id', 'options'),
        Output('user_reg_input_present_brgy_id', 'disabled'),
        Output('user_reg_input_present_brgy_id', 'value'),
    ],
    [
        Input('user_reg_input_present_region_id', 'value'),
        Input('user_reg_input_present_province_id', 'value'),
        Input('user_reg_input_present_citymun_id', 'value'),
    ]
)

def user_reg_populatepresentbrgys(region, province, citymun):
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
        Output('user_reg_input_permanent_brgy_id', 'options'),
        Output('user_reg_input_permanent_brgy_id', 'disabled'),
        Output('user_reg_input_permanent_brgy_id', 'value'),
    ],
    [
        Input('user_reg_input_permanent_region_id', 'value'),
        Input('user_reg_input_permanent_province_id', 'value'),
        Input('user_reg_input_permanent_citymun_id', 'value'),
        Input('user_reg_cbox_permanent_address', 'value'),
    ],
    [
        State('user_reg_input_present_brgy_id', 'value')
    ]
)

def user_reg_populatepermanentbrgys(region, province, citymun, cbox, present_brgy):
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
        Output('user_reg_input_present_street', 'disabled'),
        Output('user_reg_input_present_street', 'value'),
    ],
    [
        Input('user_reg_input_present_region_id', 'value'),
        Input('user_reg_input_present_province_id', 'value'),
        Input('user_reg_input_present_citymun_id', 'value'),
        Input('user_reg_input_present_brgy_id', 'value'),
    ]
)

def user_reg_enablepresentstreet(region, province, citymun, brgy):
    disabled = True
    if region and province and citymun and brgy: disabled = False
    return [disabled, None]

# Callback for enabling permanent street address once permanent city/municipality is selected
@app.callback(
    [
        Output('user_reg_input_permanent_street', 'disabled'),
        Output('user_reg_input_permanent_street', 'value'),
    ],
    [
        Input('user_reg_input_permanent_region_id', 'value'),
        Input('user_reg_input_permanent_province_id', 'value'),
        Input('user_reg_input_permanent_citymun_id', 'value'),
        Input('user_reg_input_permanent_brgy_id', 'value'),
        Input('user_reg_cbox_permanent_address', 'value'),
    ],
    [
        State('user_reg_input_present_street', 'value')
    ]
)

def user_reg_enablepermanentstreet(region, province, citymun, brgy, cbox, present_street):
    disabled = True
    value = None
    if region and province and citymun and brgy:
        if cbox: value = present_street
        else: disabled = False
    return [disabled, value]