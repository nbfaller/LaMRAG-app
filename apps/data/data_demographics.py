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
from utilities.utils import MarginSettings

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [

                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)