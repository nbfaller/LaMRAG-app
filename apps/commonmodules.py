# Dash related dependencies
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
import pytz
# App definition
from app import app
from apps import dbconnect as db

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

# Navbar
@app.callback(
    [
        Output('cm_sidebar', 'is_open')
    ],
    [
        Input('cm_navbar_btn_burger', 'n_clicks')
    ]
)

def cm_opensidebar(btn):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'cm_navbar_btn_burger' and btn:
            return [True]
        else: raise PreventUpdate
    else: raise PreventUpdate

# Callback for setting navbar greeting and showing buttons if logged in
@app.callback(
    [
        # Navbar
        Output('com_mod_hti_icon', 'className'),
        Output('com_mod_ddm_navbarmenu', 'class_name'),
        Output('com_mod_spa_timegreeting', 'children'),
        Output('com_mod_htb_name', 'children'),
        # Burger button
        Output('com_mod_col_burger', 'class_name'),
        # Dropdown header
        Output('com_mod_bdg_loggedinusertype', 'children'),
        Output('com_mod_hh4_loggedinname', 'children'),
        Output('com_mod_hh4_loggedindesig', 'children'),
        Output('com_mod_hh4_loggedinoffice', 'children')
    ],
    [
        Input('app_sessionlogout', 'data')
    ],
    [
        State('app_currentuser_id', 'data')
    ],
)

def com_mod_setgreeting(sessionlogout, user_id):
    # Navbar
    class_name = 'd-none'
    icon_className = None
    timegreeting = 'adlaw'
    name = None
    # Burger button
    burger = 'd-none ms-4'
    # Dropdown header
    usertype = None
    fullname = None
    desig = None
    office = None
    if not(sessionlogout):
        class_name = 'd-block'
        burger = 'd-block ms-4'
        time = datetime.now(pytz.timezone('Asia/Manila')).hour
        if time >= 0 and time < 12:
            if time >= 0 and time < 5: icon_className = 'bi bi-moon-fill me-2'
            elif time >= 5 and time < 7: icon_className = 'bi bi-sunrise-fill me-2'
            else: icon_className = 'bi bi-brightness-low-fill me-2'
            timegreeting = "aga"
        elif time >= 12 and time < 13:
            icon_className = 'bi bi-brightness-high-fill me-2'
            timegreeting = "udto"
        elif time >= 13 and time < 18:
            if time >= 13 and time < 16: icon_className = 'bi bi-brightness-high-fill me-2'
            elif time >= 16 and time < 17: icon_className = 'bi bi-brightness-low-fill me-2'
            else: icon_className = 'bi bi-sunset-fill me-2'
            timegreeting = "kulop"
        else:
            icon_className = 'bi bi-moon-fill me-2'
            timegreeting = "gab-i"
        sql = """SELECT u.fname, u.livedname, u.mname, u.lname, ut.label AS usertype, u.designation AS desig, o.name AS office FROM users.user AS u
            INNER JOIN utilities.usertype AS ut ON u.usertype_id = ut.id
            INNER JOIN utilities.office AS o ON u.office_id = o.id
            WHERE u.id = %s;"""
        values = [user_id]
        cols = ['fname', 'livedname', 'mname', 'lname', 'usertype', 'desig', 'office']
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0]:
            # Name in navbar
            if df['livedname'][0]: name = df['livedname'][0]
            else: name = df['fname'][0]
            # Fullname in dropdown header
            if df['mname'][0]: fullname = "%s %s. %s" % (name, df['mname'][0][0], df['lname'][0])
            else: fullname = "%s %s" % (name, df['lname'][0])
            # Other details in dropdown header
            usertype = df['usertype'][0]
            desig = df['desig'][0]
            office = df['office'][0]
    else: raise PreventUpdate
    return [icon_className, class_name, timegreeting, name, burger, usertype, fullname, desig, office]

nav_external_link = True

navbar = dbc.Navbar(
    [
        dbc.Col(
            dbc.Button(
                html.I(className = 'bi bi-justify-left'),
                id = 'cm_navbar_btn_burger',
                color = 'secondary',
                outline = True,
                style = {
                    'height' : '2em',
                    'width' : '2em',
                    'padding' : '0px',
                },
            ),
            id = 'com_mod_col_burger',
            width = 'auto',
            class_name = 'd-none ms-4'
        ),
        dbc.Col(
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.NavbarBrand(
                                [
                                    html.Img(
                                        src = '/static/lamrag-wordmark-dmsans.png',
                                        style = {'height' : '1.75em'}
                                    ),
                                ],
                                style = {'letter-spacing' : '-0.5px'},
                                class_name = 'm-0'
                            ),
                            width = 'auto'
                        ),
                    ],
                    align = 'center',
                    #class_name = 'g-0',
                    #class_name = 'justify-content-center g-0',
                    class_name = 'justify-content-md-start justify-content-center g-0',
                ),
                href = '/'
            ),
            class_name = 'ms-md-4 me-md-2 ms-0 me-0'
        ),
        dbc.Col(
            [
                dbc.Button(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.I(className = 'bi bi-person-fill'),
                                sm = 'auto',
                                class_name = 'p-auto pe-md-1'
                            ),
                            dbc.Col(
                                "Log-in",
                                sm = 'auto',
                                class_name = 'p-auto ps-md-1 d-none d-md-block'
                            )
                        ],
                        align = 'center',
                        class_name = 'pad-row',
                        style = {
                            'height' : '100%',
                            'margin-left' : 'auto',
                            'margin-right' : 'auto'
                        }
                    ),
                    id = 'cm_navbar_btn_login',
                    href = '/login',
                    color = 'secondary',
                    outline = True,
                    style = {
                        'height' : '2em',
                        'padding' : '0px',
                        'display' : 'none'
                    },
                ),
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem(
                            [
                                dbc.Badge(
                                    id = 'com_mod_bdg_loggedinusertype',
                                    class_name = 'mb-1'
                                ),
                                html.H4(
                                    id = 'com_mod_hh4_loggedinname',
                                    className = 'text-body mb-0'
                                ),
                                html.Small(
                                    id = 'com_mod_hh4_loggedindesig',
                                    className = 'text-body mb-0'
                                ),
                                html.Br(),
                                html.Small(
                                    id = 'com_mod_hh4_loggedinoffice',
                                    className = 'text-body mb-0'
                                )
                            ],
                            header = True
                        ),
                        dbc.DropdownMenuItem(divider = True),
                        dbc.DropdownMenuItem("Dashboard", href = '/dashboard', external_link = nav_external_link),
                        dbc.DropdownMenuItem("Profile", href = '/users/profile', external_link = nav_external_link),
                        dbc.DropdownMenuItem("Change password", href = '', external_link = nav_external_link),
                        dbc.DropdownMenuItem("Log-out", href = '/logout', external_link = nav_external_link, id = 'com_mod_dmi_logout'),
                    ],
                    id = 'com_mod_ddm_navbarmenu',
                    label = [
                        html.Span(
                            [
                                html.I(id = 'com_mod_hti_icon'),
                                "Maupay nga ",
                                html.Span(id = 'com_mod_spa_timegreeting'),
                                ", ",
                                html.B(id = 'com_mod_htb_name')
                            ],
                            className = 'd-none d-md-inline'
                        )
                    ],
                    align_end = True,
                    in_navbar = True,
                    nav = True,
                    class_name = 'd-none'
                ),
            ],
            width = 'auto',
            class_name = 'ms-md-2 me-4'
        ),
    ],
    id = 'cm_navbar',
    dark = True,
    #color = 'dark',
    color = '#203354',
    #color = '#2e215e'
    #color = '#2a3385'
    style = {
        'position' : 'fixed',
        'top' : 0,
        'width' : '100vw',
        'z-index' : '100',
        'padding-top' : '1em',
        'padding-bottom' : '1em'
    }
)

# Sidebar
sidebar_btn_color = 'dark'
sidebar_btn_size = 'sm'
sidebar_btn_style = {'width' : '100%'}
sidebar_btn_col_width = 'auto'
sidebar_btn_row_class_name = 'justify-content-left'
sidebar_header_style = {'font-weight' : 'bold', 'letter-spacing': '0.1em'}

sidebar = dbc.Offcanvas(
    [
        # Main buttons
        html.Div(
            [
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-house me-2'),
                                "Home"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-grid-1x2 me-2'),
                                "Dashboard"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/dashboard',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-send-exclamation me-2'),
                                "File a report"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/reports/create',
                    external_link = True,
                    color = 'warning', outline = True, #sidebar_btn_color,
                    size = sidebar_btn_size,
                    style = {
                        'width' : '100%',
                        'border-width' : '0px'
                    }
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-pencil-square me-2'),
                                "Update a report"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/reports/update',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
            ],
            id = 'sidebar_div_mainbtns'
        ),
        html.Hr(),
        # Reports Management
        html.Div(
            [
                html.Sup(
                    [
                        #html.I(className = 'bi bi-clipboard-fill me-2'),
                        "Reports Management"
                    ],
                    style = sidebar_header_style,
                    className = 'mt-3 mb-2 text-uppercase'
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-clipboard-data me-2'),
                                "View reports"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/reports',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-clipboard-plus me-2'),
                                "Request a report"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/reports/request',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-printer me-2'),
                                "Generate a report"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/reports/generate',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
            ], className = 'mb-3',
        ),
        # Events Management
        html.Div(
            [
                html.Sup(
                    [
                        #html.I(className = 'bi bi-clipboard-fill me-2'),
                        "Events Management"
                    ],
                    style = sidebar_header_style,
                    className = 'mt-3 mb-2 text-uppercase'
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-journal-bookmark me-2'),
                                "View events"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/events',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-exclamation-square me-2'),
                                "Create an event"
                            ],
                            width = sidebar_btn_col_width), class_name = sidebar_btn_row_class_name),
                    href = '/events/create',
                    external_link = True,
                    color = 'warning', outline = True, #sidebar_btn_color,
                    size = sidebar_btn_size,
                    style = {
                        'width' : '100%',
                        'border-width' : '0px'
                    }
                )
            ], className = 'mb-3'
        ),
        # User Management
        html.Div(
            [
                html.Sup(
                    [
                        #html.I(className = 'bi bi-person-fill me-2'),
                        "User Management"
                    ],
                    style = sidebar_header_style,
                    className = 'mt-3 mb-2 text-uppercase'
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-search me-2'),
                                "Search users"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/users',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-person-add me-2'),
                                "Register new user"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/users/register',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
            ], className = 'mb-3',
            id = 'sidebar_div_usermgt'
        ),
        # Data Management
        html.Div(
            [
                html.Sup(
                    [
                        #html.I(className = 'bi bi-clipboard-fill me-2'),
                        "Data Management"
                    ],
                    style = sidebar_header_style,
                    className = 'mt-3 mb-2 text-uppercase'
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-houses me-2'),
                                "View barangays"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/data/barangays',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
                dbc.Button(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.I(className = 'bi bi-people me-2'),
                                "View demographics"
                            ],
                            width = sidebar_btn_col_width
                        ), class_name = sidebar_btn_row_class_name
                    ),
                    href = '/data/demographics',
                    external_link = True,
                    color = sidebar_btn_color, size = sidebar_btn_size, style = sidebar_btn_style
                ),
            ], className = 'mb-3',
        ),
        # Footer
        html.Div(
            [
                html.Hr(),
                dbc.Row(
                    [
                        #dbc.Col(
                        #    html.Img(
                        #        src = app.get_asset_url('ph-arms-mono-dark.png'),
                        #        style = {'height' : '3em'},
                        #    ),
                        #    width = 'auto',
                        #),
                        dbc.Col(
                            html.Img(
                                src = app.get_asset_url('city-seal-mono-dark.png'),
                                style = {'height' : '3em'},
                            ),
                            width = 'auto',
                        ),
                        dbc.Col(
                            html.Img(
                                src = app.get_asset_url('cdrrmo-logo-mono-dark.png'),
                                style = {'height' : '3em'},
                            ),
                            width = 'auto'
                        )
                    ], class_name = 'g-2 mb-2'
                ),
                html.P(
                    [
                        html.B("LáMRAG"),
                        """ (Local Management Platform for Risk Analytics & Governance) is the integrated data collection,
                        incident reporting, and data analysis system of the Calbayog City Disaster Risk Reduction & Management Office (CDRRMO).""",
                        html.Br(), html.Br(),
                        "All content is in the public domain unless otherwise stated."
                    ],
                    className = 'text-muted',
                    style = {'font-size' : '0.7625em'}
                )
            ]
        )
    ],
    title = [
        html.Img(
            src = '/static/lamrag-wordmark-dmsans.png',
            style = {'height' : '1.75em'},
            className = 'me-2'
        ),
        #"Local Management Platform for Risk Analytics & Governance"
    ],
    id = 'cm_sidebar',
    style = {
    #    'color' : '#F5F5F5',
        #'width' : '100%',
        'background-color' : '#203354'
    },
    class_name = 'text-bg-dark w-100 w-md-50'
)

# Footer
hyperlink_style = {
    'text-decoration' : 'none',
    'color' : 'inherit'
}
footer = html.Footer(
    [
        dbc.Row(
            [
                # Main website information
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                #dbc.Col(
                                #    html.Img(
                                #        src = app.get_asset_url('ph-arms-mono.png'),
                                #        style = {'height' : '5em'},
                                #    ),
                                #    width = 'auto',
                                #),
                                dbc.Col(
                                    html.Img(
                                        src = app.get_asset_url('city-seal-mono.png'),
                                        style = {'height' : '5em'},
                                    ),
                                    width = 'auto',
                                ),
                                dbc.Col(
                                    html.Img(
                                        src = app.get_asset_url('cdrrmo-logo-mono.png'),
                                        style = {'height' : '5em'},
                                    ),
                                    width = 'auto'
                                )
                            ], class_name = 'g-2 mb-2'
                        ),
                        html.Div(
                            [
                                html.P(html.Small("Republic of the Philippines • City of Calbayog"), className = 'mb-0'),
                                html.H4("City Disaster Risk Reduction and Management Office", className = 'mb-0 fw-bold'),
                                html.A(html.P(html.Small([html.I(className = 'bi bi-pin-map-fill me-2'), "Government Center, Magsaysay Extension (Diversion Road), Brgy. Bagacay, Calbayog City, Samar 6710"]), className = 'mb-0'), href = 'https://maps.app.goo.gl/Sjw7n6DwXn5qvUfg9', style = hyperlink_style, target = '_blank')
                            ], className = 'mb-3'
                        ),
                        html.Div(
                            [
                                html.P(
                                    [
                                        html.Small([html.I(className = 'bi bi-question-circle me-2'), "Frequently asked questions"]), html.Br(),
                                        html.Small([html.I(className = 'bi bi-shield-lock me-2'), "Privacy policy"]), html.Br(),
                                        html.Small([html.I(className = 'bi bi-megaphone me-2'), "Feedback form"])
                                    ],
                                className = 'mb-0')
                            ], className = 'mb-3'
                        ),
                        html.P(html.Small("All content is in the public domain unless otherwise stated."), className = 'mb-0')
                    ],
                    md = 6,
                    class_name = 'md-6 pt-4 ps-4 pe-4 pb-3 pb-md-4'
                ),
                # City information
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Img(
                                        src = app.get_asset_url('city-silhouette.png'),
                                        style = {'height' : '5em'},
                                    ),
                                    width = 'auto',
                                )
                            ], class_name = 'g-2 mb-3'
                        ),
                        html.H6("About the city", className = 'mb-0 fw-bold'),
                        html.P(
                            html.Small(
                                """The City of Calbayog is a first-class component city at the northwestern corner of Samar Province.
                                Founded as a Spanish settlement along the Jibatang River, it has since grown into the province's foremost
                                commercial center. It was constituted as a city in 1948 through the merger of the municipalities of Calbayog, Tinambacan,
                                and Oquendo, which now define its three geographical districts."""
                            )
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            html.Small([html.I(className = 'bi bi-house-fill me-2'), "Local Government"], className = 'mb-0 fw-bold')
                                        ),
                                        html.A(html.P(html.Small("Main Website"), className = 'mb-0'), href = 'https://calbayog.gov.ph', style = hyperlink_style, target = '_blank'),
                                        html.A(html.P(html.Small("Public Information Office"), className = 'mb-0'), href = 'https://www.facebook.com/people/Calbayog-City-Public-Information-Office/100090744381505/', style = hyperlink_style, target = '_blank'),
                                        html.A(html.P(html.Small("Office of the City Mayor"), className = 'mb-0'), href = 'https://www.facebook.com/people/Raymund-Monmon-C-Uy/100086298882034/', style = hyperlink_style, target = '_blank'),
                                        html.A(html.P(html.Small("Office of the City Vice Mayor"), className = 'mb-0'), href = 'https://www.facebook.com/RexMDaguman', style = hyperlink_style, target = '_blank'),
                                        html.A(html.P(html.Small("Sangguniang Panlungsod"), className = 'mb-0'), href = 'https://www.facebook.com/calbayogsp/', style = hyperlink_style, target = '_blank'),
                                        html.A(html.P(html.Small("Directory of Offices"), className = 'mb-0'), href = 'https://calbayog.gov.ph/contact-us/', style = hyperlink_style, target = '_blank')
                                    ],
                                    class_name = 'col-lg-4 col-md-6 col-sm-4 col-xs-12',
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            html.Small([html.I(className = 'bi bi-bank2 me-2'), "National Government"], className = 'mb-0 fw-bold')
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.A(html.P(html.Small("GOV.PH"), className = 'mb-0'), href = 'https://www.gov.ph', style = hyperlink_style, target = '_blank'),
                                                        html.A(html.P(html.Small("Official Gazette"), className = 'mb-0'), href = 'https://officialgazette.gov.ph', style = hyperlink_style, target = '_blank'),
                                                        html.A(html.P(html.Small("Open Data Portal"), className = 'mb-0'), href = 'https://data.gov.ph', style = hyperlink_style, target = '_blank'),
                                                        html.A(html.P(html.Small("The President"), className = 'mb-0'), href = 'https://president.gov.ph', style = hyperlink_style, target = '_blank'),
                                                        html.A(html.P(html.Small("Office of the President"), className = 'mb-0'), href = 'https://op-proper.gov.ph', style = hyperlink_style, target = '_blank'),
                                                        html.A(html.P(html.Small("Office of the Vice President"), className = 'mb-0'), href = 'https://ovp.gov.ph', style = hyperlink_style, target = '_blank'),
                                                    ],
                                                    lg = 6,
                                                    md = 12,
                                                    sm = 6,
                                                    xs = 12,
                                                    #class_name = 'col-lg-6'
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.A(html.P(html.Small("Senate of the Philippines"), className = 'mb-0'), href = 'https://senate.gov.ph', style = hyperlink_style, target = '_blank'),
                                                        html.A(html.P(html.Small("House of Representatives"), className = 'mb-0'), href = 'https://congress.gov.ph', style = hyperlink_style, target = '_blank'),
                                                        html.A(html.P(html.Small("Supreme Court"), className = 'mb-0'), href = 'https://sc.judiciary.gov.ph', style = hyperlink_style, target = '_blank'),
                                                        html.A(html.P(html.Small("Court of Appeals"), className = 'mb-0'), href = 'https://ca.judiciary.gov.ph', style = hyperlink_style, target = '_blank'),
                                                        html.A(html.P(html.Small("Sandiganbayan"), className = 'mb-0'), href = 'https://sb.judiciary.gov.ph', style = hyperlink_style, target = '_blank'),
                                                    ],
                                                    lg = 6,
                                                    md = 12,
                                                    sm = 6,
                                                    xs = 12
                                                    #class_name = 'col-lg-6'
                                                )
                                            ]
                                        )
                                    ],
                                    class_name = 'col-lg-8 col-md-6 col-sm-8 col-xs-12'
                                ),
                            ]
                        )
                    ],
                    md = 6,
                    style = {'font-size' : '0.75rem'},
                    class_name = 'md-6 pt-3 ps-4 pe-4 pb-4 pt-md-4'
                )
            ],
            class_name = 'g-0'
        ),
        dbc.Row(
            html.Iframe(
                src = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d562.5407776071039!2d124.61192079862425!3d12.06236092006715!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3309db8c252d21d1%3A0xaf1f98f12b16d98f!2sCalbayogCdrrmo!5e1!3m2!1sen!2sph!4v1709188668855!5m2!1sen!2sph',
                width = '100%',
                height = '200em',
                style = {'border' : '0'},
                #allowfullscreen ="",
                loading_state = 'lazy',
                referrerPolicy = 'no-referrer-when-downgrade'
            ),
            class_name = 'g-0 mb-0'
        )
    ],
    style = {
        'background-color' : '#d4cfc8',
        #'margin-top' : '1em',
        #'position' : 'absolute',
        #'bottom' : '0'
    },
    className = 'text-muted'
)