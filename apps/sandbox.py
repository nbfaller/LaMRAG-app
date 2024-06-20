# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# Sandbox imports
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# App definition
from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dcc.Store(id = 'sandbox_event_id', data = 1),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Spinner(
                            spinner_style = {
                                'color' : '#2a3385',
                                'width' : '3rem',
                                'height' : '3rem'
                            }
                        ),
                        html.H3(
                            [
                                "Kadali la.",
                                html.Br(),
                                html.Small("(Please wait.)", className = 'text-muted')
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

sandbox_url = '/sandbox'