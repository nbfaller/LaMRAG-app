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
                                                    html.H4("Local Management Platform for Risk Analytics & Governance"),
                                                    class_name = 'mb-3'
                                                ),
                                                dbc.Form(
                                                    [
                                                        dbc.Row(
                                                            dbc.Col(
                                                                [
                                                                    dbc.Input(
                                                                        type = 'text',
                                                                        placeholder = 'Username',
                                                                        id = 'com_hom_input_username'
                                                                    )
                                                                ],
                                                                class_name = 'mb-3'
                                                            )
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
                                                            ], class_name = 'mb-3'
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    dbc.Button(
                                                                        "Log-in",
                                                                        style = {'width' : '100%'},
                                                                        id = 'com_hom_btn_login'
                                                                        #color = 'secondary'
                                                                    )
                                                                )
                                                            ], class_name = 'mb-0'
                                                        )
                                                    ]
                                                ),
                                            ]
                                        )
                                    ],
                                    class_name = 'col-12 col-md-4'
                                )
                            ]
                        )
                    ],
                    style = {
                        'border-radius' : '0.75rem',
                        'overflow' : 'hidden',
                        'box-shadow' : '0 0 32px 4px rgba(135, 113, 90, 0.2)'
                    }
                )
            ]
        )
    ],
    className = 'mt-2 mb-2 ms-md-5 me-md-5'
)