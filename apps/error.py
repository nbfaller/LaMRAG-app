# Dash related dependencies
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# App definition
from application import app

error_width = 'auto'
error_justify = 'left'

layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H1(html.I(className = 'bi bi-patch-question')),
                width = error_width
            ),
            justify = error_justify
        ),
        dbc.Row(
            dbc.Col(
                html.H1("Hala, waray man?"),
                width = error_width
            ),
            justify = error_justify
        ),
        dbc.Row(
            dbc.Col(
                html.P(
                    [
                        "Rubat o nawawara an imo ginbibiling dinhi. Alayon pag-contact san administrator para mabuligan ka.", html.Br(),
                        html.Small("(The page you are looking for is either broken or does not exist. Please contact the administrator for assistance.)", className = 'text-muted')
                    ]
                ),
                width = error_width
            ),
            justify = error_justify
        ),
        dbc.Row(
            dbc.Col(
                dbc.Badge(
                    "ERROR 404: PAGE NOT FOUND",
                    #color = 'danger'
                ),
                width = error_width
            ),
            justify = error_justify
        ),
    ]
)