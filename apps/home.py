# Dash related dependencies
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# Other libraries
import hashlib
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

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Card(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                #html.H4("City proper")
                                            ],
                                            style = {
                                                'color' : '#F5F5F5',
                                                'position' : 'absolute',
                                                'bottom' : '2em',
                                                'padding-left' : '2em',
                                                'padding-right' : '2em',
                                                #'text-shadow' : '0 0 4px rgba(135, 113, 90, 0.6)'
                                            },
                                            #class_name = 'align-self-bottom'
                                        ),
                                        html.Img(
                                            src=app.get_asset_url('banner.jpg'),
                                            style = {
                                                'height' : '30em',
                                                'width' : '100%',
                                                'object-fit' : 'cover',
                                                'z-index' : '-1',
                                                #'border-start-start-radius' : '0.75rem',
                                                #'border-end-start-radius' : '0.75rem'
                                                #'mask-image' : 'linear-gradient(to bottom, rgba(0, 0, 0, 1.0) 50%, transparent 100%)'
                                            }
                                        ),
                                    ],
                                    class_name = 'p-0 col-12 col-md-8'
                                ),
                                dbc.Col(
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    html.H4(
                                                        "Local Management Platform for Risk Analytics & Governance",
                                                        className = 'mb-0'
                                                    ),
                                                    class_name = 'mt-0 mb-3'
                                                ),
                                                html.Hr(className = 'mb-0'),
                                                dbc.Form(
                                                    [
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
                                                                                        id = 'com_hom_alert_passwordvalidation_col_text'
                                                                                    )
                                                                                ]
                                                                            ),
                                                                            id = 'com_hom_alert_passwordvalidation',
                                                                            is_open = False,
                                                                            color = 'warning',
                                                                            class_name = label_m,
                                                                            dismissable = True,
                                                                            #fade = True,
                                                                        )
                                                                    ]
                                                                )
                                                            ],
                                                            id = 'com_hom_row_passwordvalidation',
                                                            class_name = 'mt-0 mb-0'
                                                        ),
                                                        dbc.Row(
                                                            dbc.Col(
                                                                [
                                                                    dbc.Input(
                                                                        type = 'text',
                                                                        placeholder = 'Username',
                                                                        id = 'com_hom_input_username'
                                                                    )
                                                                ],
                                                                #class_name = 'mb-3'
                                                            ), class_name = 'mt-3 mb-3'
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        type = 'password',
                                                                        placeholder = 'Password',
                                                                        id = 'com_hom_input_password'
                                                                    )
                                                                )
                                                            ], class_name = 'mt-3 mb-3'
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    dbc.Button(
                                                                        "Log-in",
                                                                        style = {'width' : '100%'},
                                                                        id = 'com_hom_btn_login',
                                                                        type = 'submit'
                                                                        #color = 'secondary'
                                                                    )
                                                                )
                                                            ], class_name = 'mt-3 mb-3'
                                                        )
                                                    ]
                                                ),
                                                html.Hr(),
                                                html.P(
                                                    "Forgot password?",
                                                    className = 'mt-3 mb-0'
                                                )
                                            ]
                                        )
                                    ],
                                    class_name = 'align-self-center col-12 col-md-4'
                                )
                            ]
                        )
                    ],
                    style = {
                        'border-radius' : '0.75rem',
                        #'overflow' : 'hidden',
                        'box-shadow' : '0 0 32px 4px rgba(135, 113, 90, 0.2)'
                    },
                    class_name = 'overflow-hidden'
                )
            ]
        )
    ],
    className = 'mt-2 mb-2 ms-md-5 me-md-5'
)

# Callback for logging in
@app.callback(
    [
        Output('com_hom_alert_passwordvalidation', 'is_open'),
        Output('com_hom_row_passwordvalidation', 'class_name'),
        Output('com_hom_alert_passwordvalidation_col_text', 'children'),
        Output('app_currentuser_id', 'data'),
        Output('app_usertype_id', 'data'),
    ],
    [
        Input('com_hom_btn_login', 'n_clicks'), # Begin login query via button click
        Input('app_sessionlogout', 'modified_timestamp') # Reset session userid to -1 if logged out
    ],
    [
        State('com_hom_input_username', 'value'),
        State('com_hom_input_password', 'value'),
        State('app_sessionlogout', 'data'),
        State('app_currentuser_id', 'data'),
        State('app_usertype_id', 'data'),
        State('url', 'pathname'),
    ],
    prevent_initial_call = True
)

def com_home_loginprocess(btn, sessionlogout_time,
    username, password, sessionlogout, user_id,
    usertype_id, pathname):
    
    ctx = dash.callback_context

    if ctx.triggered:
        alert_open = False
        alert_row_class = 'mt-0 mb-0'
        alert_col_text = None
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else: raise PreventUpdate

    if eventid == 'com_hom_btn_login': # Trigger for login process
        if btn:
            if username and password:
                sql = """SELECT id, usertype_id FROM users.user
                    WHERE username = %s AND password = %s AND is_active;"""
                # We match the encrypted input to the encrypted password in the database
                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
                values = [encrypt_string(username), encrypt_string(password)]
                cols = ['id', 'usertype_id']
                df = db.querydatafromdatabase(sql, values, cols)
                if df.shape[0]: # If the query returns rows
                    user_id = df['id'][0]
                    usertype_id = df['usertype_id'][0]
                else:
                    user_id = -1
                    usertype_id = -1
                    alert_open = True
                    alert_row_class = 'mt-3 mb-3'
                    alert_col_text = [
                        "Diri sakto an nabutang nga password.",
                        html.Br(),
                        html.Small(
                            "(Incorrect password.)",
                            className = 'text-muted'
                        ),
                    ]
            elif not(username) or not(password):
                alert_open = True
                alert_row_class = 'mt-3 mb-3'
                if not(username) and not(password):
                    alert_col_text = [
                        "Alayon pagbutang san imo username ug password.",
                        html.Br(),
                        html.Small(
                            "(Please input your username and password.)",
                            className = 'text-muted'
                        ),
                    ]
                elif not(username) and password:
                    alert_col_text = [
                        "Alayon pagbutang san imo username.",
                        html.Br(),
                        html.Small(
                            "(Please input your username.)",
                            className = 'text-muted'
                        ),
                    ]
                else:
                    alert_col_text = [
                        "Alayon pagbutang san imo password.",
                        html.Br(),
                        html.Small(
                            "(Please input your password.)",
                            className = 'text-muted'
                        ),
                    ]
    elif eventid == 'app_sessionlogout' and pathname == '/logout': # Reset the user_id and usertype_id if logged out
        user_id = -1
        usertype_id = -1
    else:
        raise PreventUpdate
    # Maybe move this inside the if statement to
    # avoid updating app_currentuser_id every time
    # this callback is triggered?
    return [alert_open, alert_row_class, alert_col_text, user_id, usertype_id]

# Callback for routing login
@app.callback(
    [
        Output('url', 'pathname')
    ],
    [
        Input('app_currentuser_id', 'modified_timestamp')
    ],
    [
        State('app_currentuser_id', 'data'),
        State('url', 'pathname')
    ],
    prevent_initial_call = True
)

def com_home_routelogin(logintime, user_id, pathname):
    ctx = dash.callback_context
    if ctx.triggered and (pathname == '/' or pathname == '/home'): # Fix this part
        if user_id > 0: url = '/dashboard'
        else: url = '/'
    else: raise PreventUpdate
    return [url]