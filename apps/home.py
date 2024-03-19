# Dash related dependencies
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# App definition
from app import app

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    "Dashboard",
                    md = 9,
                    #class_name = 'col-md-8 col-sm-6 col-xs-12'
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Log-in"),
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Input(
                                                    type = 'text',
                                                    placeholder = 'Username',
                                                    id = 'login_username'
                                                )
                                            )
                                        ], class_name = 'mb-3'
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Input(
                                                    type = 'password',
                                                    placeholder = 'Password',
                                                    id = 'login_password'
                                                )
                                            )
                                        ], class_name = 'mb-3'
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Button(
                                                    "Log-in",
                                                    style = {'width' : '100%'},
                                                    id = 'login_btn'
                                                    #color = 'secondary'
                                                )
                                            )
                                        ], class_name = 'mb-0'
                                    )
                                ]
                            )
                        ]
                    ),
                    md = 3,
                    #class_name = 'col-md-4 col-sm-6 col-xs-12'
                )
            ]
        )
    ]
)