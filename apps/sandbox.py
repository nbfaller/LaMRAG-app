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

tag_required = html.Sup("*", className = 'text-danger')


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