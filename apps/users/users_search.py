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
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# App definition
from app import app
from apps import dbconnect as db
from utilities.utils import MarginSettings

tag_required = html.Sup("*", className = 'text-danger')
card_style = {
    'border-radius' : '0.75rem',
    'overflow' : 'hidden',
    'box-shadow' : '0 0 32px 4px rgba(135, 113, 90, 0.2)'
}

# Default margins and spacing settings
margins = MarginSettings()

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Header
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H1(
                                            "Search users",
                                            id = 'usr_src_h1_header'
                                        ),
                                    ],
                                    class_name = margins.row,
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Input(
                                                id = 'usr_src_input_search',
                                                type = 'text',
                                                placeholder = "Search by last name, first name, lived name, middle name, office, or designation."
                                                #value = 1
                                               ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ], className = 'mb-1 mb-md-0',
                                    id = 'usr_src_row_search',
                                    class_name = margins.row
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Filter by:", #html.Br(),
                                                    #html.Small(" (Year)", className = 'text-muted')
                                                ],
                                                id = 'usr_src_label_filter',
                                                class_name = margins.label
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-2'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'usr_src_input_usertype_id',
                                                multi = True,
                                                #type = 'text',
                                                #placeholder = "Search by last name, first name, lived name, or middle name"
                                                #value = 1
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-4'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'usr_src_input_office_id',
                                                multi = True
                                                #type = 'text',
                                                #placeholder = "Search by last name, first name, lived name, or middle name"
                                                #value = 1
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-6'
                                        ),
                                    ], className = 'mb-1 mb-md-0',
                                    id = 'usr_src_row_filter',
                                    class_name = margins.row
                                ),
                            ],
                            id = 'usr_src_div_header',
                            className = margins.header
                        ),
                        html.Div(
                            id = 'usr_src_div_results',
                            className = margins.div,
                            style = {
                                'max-width' : '100%',
                                'overflow' : 'scroll'
                            }
                        ),
                        html.Div(
                            [
                                html.Hr(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-key me-2'),
                                                        "Kabug-osan nga kadamo san nag-login",
                                                        #html.Br(),
                                                        html.Small(" (Cumulative number of log-ins)", className = 'text-muted')
                                                    ]
                                                ),
                                            ]
                                        )
                                    ], class_name = margins.row
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                #dbc.Card(
                                                    #dbc.CardBody(
                                                        dcc.Graph(
                                                            id = 'usr_src_gra_logins',
                                                            animate = True,
                                                            #style = {'max-height' : '15em'}
                                                        )
                                                    #),
                                                    #style = card_style
                                                #)
                                            ]
                                        )
                                    ],
                                    id = 'usr_src_row_logins',
                                    class_name = margins.row
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
                                                                class_name = margins.alert_icon
                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    html.H5(
                                                                        [
                                                                            "Panano ko dapat basahon ini nga chart?",
                                                                            html.Small(" (How should I read this chart?)", className = 'text-muted')
                                                                        ]
                                                                    ),
                                                                    """An stacked bar chart in usa nga klase san chart nga nagpapakita san
                                                                    pagbabag-o sa kadamo san usa nga kantidad nga puwede matunga sa iba-iba nga
                                                                    mga grupo o klasipikasiyon. Gamit sini nga chart, makikit-an naton an
                                                                    pagdamo san mga nagla-log in sa LáMRAG. Labaw sini, makikit-an naton an kadamo
                                                                    san mga log-in base sa iba-iba nga klase san mga nagamit pinaagi san iba-iba
                                                                    nga mga kolor (kun regular user, administrator, o superadministrator sira).""",
                                                                    html.Br(),
                                                                    html.Small(
                                                                        """(Stacked bar charts are used to show the change in value of a quantity that
                                                                        can be divided into classifications or parts. Using this specific chart, we can
                                                                        see the number of people who log into LáMRAG as time passes. Beyond this, however,
                                                                        we can see the number of log-ins for each type of user, whether they be regular
                                                                        users, administrators, or superadministrators, hence the variety of colors.)""",
                                                                        className = 'text-muted'
                                                                    ),
                                                                    #html.Span(id = 'rep_cre_alert_inputvalidation_span_missing')
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                    is_open = True,
                                                    color = 'info',
                                                    class_name = margins.label,
                                                    dismissable = False,
                                                    #fade = True,
                                                )
                                            ]
                                        )
                                    ],
                                    style = {'display' : 'none'}
                                    #class_name = margins.row
                                ),
                            ],
                            id = 'usr_src_div_logchart'
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.A(
                                                    [
                                                        html.I(className = 'bi bi-arrow-return-left me-2'),
                                                        "Balik sa dashboard",
                                                        html.Small(" (Return to dashboard)", className = 'text-muted')
                                                    ],
                                                    href = '/dashboard'
                                                )
                                            ],
                                            class_name = 'col-auto'
                                        )
                                    ],
                                    class_name = margins.row + ' justify-content-end'
                                )
                            ],
                            id = 'usr_src_div_footer',
                            className = margins.footer
                        )
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        ),
    ]
)

usr_src_url_pathname = '/users/search'

# Callback for populating dropdowns and checklists
@app.callback(
    [
        Output('usr_src_input_usertype_id', 'options'),
        Output('usr_src_input_office_id', 'options'),
    ],
    [
        Input('url', 'pathname')
    ]
)

def usr_src_populatedropdowns(pathname):
    if pathname == usr_src_url_pathname:
        dropdowns = []

        # User types
        sql = """SELECT label AS label, id AS value
        FROM utilities.usertype;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        usertypes = df.to_dict('records')
        dropdowns.append(usertypes)

        # Offices
        sql = """SELECT label AS label, id AS value
        FROM utilities.office;
        """
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        offices = df.to_dict('records')
        dropdowns.append(offices)

        return dropdowns
    else: raise PreventUpdate

# Callback for searching users
@app.callback(
    [
        Output('usr_src_div_results', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('usr_src_input_search', 'value'),
        Input('usr_src_input_usertype_id', 'value'),
        Input('usr_src_input_office_id', 'value')
    ]
)

def usr_src_loadsearchresults(pathname, search, usertype, office):
    if pathname == usr_src_url_pathname:
        # Retrieve users as dataframe
        sql = """SELECT
        u.id AS id,
        CONCAT(u.lname, ', ', COALESCE(u.livedname, u.fname), ' ', LEFT(u.mname, 1)) AS Name,
        o.name AS Office,
        u.designation AS Designation,
        ut.label AS usertype
        FROM users.user AS u
        LEFT JOIN utilities.office AS o ON u.office_id = o.id
        LEFT JOIN utilities.usertype AS ut ON u.usertype_id = ut.id
        WHERE u.is_active
        """
        values = []
        cols = ['ID No.', 'Name', 'Office', 'Designation', 'User type']

        if search:
            sql += """ AND (u.lname ILIKE %s OR u.fname ILIKE %s
            OR u.livedname ILIKE %s OR u.mname ILIKE %s
            OR o.name ILIKE %s OR u.designation ILIKE %s)"""
            values += [f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"]
        
        if usertype:
            c = 1
            sql += """ AND ("""
            for i in usertype:
                sql += """ u.usertype_id = %s"""
                if c < len(usertype): sql += """ OR"""
                values += [i]
                c += 1
            sql += """)"""
        
        if office:
            c = 1
            sql += """ AND ("""
            for i in office:
                sql += """ u.office_id = %s"""
                if c < len(office): sql += """ OR"""
                values += [i]
                c += 1
            sql += """)"""

        sql += """ORDER BY u.lname ASC;"""
        df = db.querydatafromdatabase(sql, values, cols)

        badge_color = None
        for i in df.index:
            # Names as hyperlinks
            df.loc[i, 'Name'] = html.A(
                df['Name'][i],
                href = '/users/user?id=%s' % df['ID No.'][i]
            )
            # User types as badges
            if df['User type'][i] == 'Administrator': badge_color = 'warning'
            elif df['User type'][i] == 'Superadministrator': badge_color = 'danger'
            else: badge_color = 'secondary'
            df.loc[i, 'User type'] = dbc.Badge(
                df['User type'][i],
                color = badge_color
            )

        df = df[['Name', 'Office', 'Designation', 'User type']]

        table = dbc.Table.from_dataframe(
            df,
            striped = False,
            bordered = False,
            hover = True,
            size = 'sm'
        )

        return [table]
    else: raise PreventUpdate

# Callback for generating logins graph
@app.callback(
    [
        Output('usr_src_gra_logins', 'figure'),
    ],
    [
        Input('url', 'pathname')
    ]
)

def sandbox_generatehistogram(pathname):
    if pathname == usr_src_url_pathname:
        sql = """SELECT al.login_time,
        ut.label
        FROM logs.accesslog AS al
        INNER JOIN users.user AS u ON al.user_id = u.id
        LEFT JOIN utilities.usertype AS ut ON u.usertype_id = ut.id;
        """
        values = []
        cols = ['Login time', 'User type']
        df = db.querydatafromdatabase(sql, values, cols)
        #print(df)
        df['Login time'] = pd.to_datetime(df['Login time'])
        df = df.groupby([df['Login time'], 'User type']).size().unstack(fill_value = 0).cumsum().reset_index()
        df.columns.name = None
        #print(df)

        traces = []
        for type in df.columns[1:]:
            traces.append(
                go.Scatter(
                    x = df['Login time'],
                    y = df[type],
                    mode = 'lines',
                    name = type,
                    stackgroup ='one'  # This parameter makes it a stacked area chart
                )
            )

        layout = go.Layout(
            {
                'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                'paper_bgcolor' : 'rgba(0, 0, 0, 0)'
            },
            #title = 'Cumulative user logins',
            xaxis = {
                'title': 'Petsa (Date)'
            },
            yaxis = {
                'title': 'Log-ins'
            },
            font_family = "DM Sans",
            showlegend = True,
            legend = {
                'orientation' : 'h',
                'xanchor' : 'left',
                'yanchor' : 'top',
                'x' : 0.00,
                'y' : -0.25
            },
            template = 'plotly_white',
            margin = {
                't' : 0,
                'b' : 0,
                'l' : 0,
                'r' : 0,
                'pad' : 0
            }
        )

        fig = {'data': traces, 'layout': layout}
        return [fig]
    else: raise PreventUpdate