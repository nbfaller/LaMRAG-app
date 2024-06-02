# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
# App definition
from app import app
from apps import dbconnect as db

tag_required = html.Sup("*", className = 'text-danger')
card_style = {
    'border-radius' : '0.75rem',
    'overflow' : 'hidden',
    'box-shadow' : '0 0 32px 4px rgba(135, 113, 90, 0.2)'
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
                                            "User dashboard",
                                            id = 'com_das_h1_header'
                                        ),
                                        html.P(
                                            "User information",
                                            id = 'com_das_htp_userdetails',
                                            className = p_m
                                        )
                                    ],
                                    class_name = row_m,
                                ),
                            ],
                            id = 'com_das_div_header',
                            className = header_m
                        ),
                        html.Hr(),
                        # Cards
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardBody(
                                                            [
                                                                html.H4(
                                                                    [
                                                                        html.I(className = 'bi bi-file-earmark-bar-graph-fill me-2'),
                                                                        "Mga ginsumite nga report",
                                                                        html.Small(" (Reports filed)", className = 'text-muted')
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    style = card_style
                                                )
                                            ],
                                            class_name = 'mb-2 mb-lg-0 col-12 col-lg-7'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardBody(
                                                            [
                                                                html.H4(
                                                                    [
                                                                        html.I(className = 'bi bi-calendar-event-fill me-2'),
                                                                        "Mga aktibo nga panhitabó",
                                                                        html.Small(" (Active events)", className = 'text-muted')
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    style = card_style
                                                )
                                            ],
                                            class_name = 'mb-2 mb-lg-0 col-12 col-lg-5'
                                        ),
                                    ],
                                    class_name = row_m,
                                )
                            ],
                            id = 'com_das_div_cards',
                            className = div_m
                        )
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)

com_das_pathname = '/dashboard'

@app.callback(
    [
        Output('com_das_htp_userdetails', 'children'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('app_currentuser_id', 'data'),
        #State('app_usertype_id', 'data')
    ]
)

def com_das_setpagedetails(
    pathname, user_id, #type_id
):
    if pathname == com_das_pathname:
        details = "User information"
        sql = """SELECT u.lname, u.fname, u.mname, u.livedname,
            ut.label
            FROM users.user AS u
            LEFT JOIN utilities.usertype AS ut ON u.usertype_id = ut.id
            WHERE u.id = %s;
            """
        values = [user_id]
        cols = ['lname', 'fname', 'mname', 'livedname', 'usertype']
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0]:
            lname = df['lname'][0]
            mname = df['mname'][0][0] + "." if df['mname'][0] else None
            fname = df['livedname'][0] if df['livedname'][0] else df['fname'][0]
            usertype = df['usertype'][0]
            
            details = "%s %s %s • %s" % (fname, mname, lname, usertype)
        
        return [details]
    else: raise PreventUpdate