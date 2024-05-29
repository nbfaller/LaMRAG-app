# Dash related dependencies
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# App definition
from app import app

error_width = 'auto'
error_justify = 'left'

layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H1(html.I(className = 'bi bi-sign-stop')),
                width = error_width
            ),
            justify = error_justify
        ),
        dbc.Row(
            dbc.Col(
                html.H1("Oops, bawal! 😭"),
                width = error_width
            ),
            justify = error_justify
        ),
        dbc.Row(
            dbc.Col(
                html.P(
                    [
                        "Diri ka awtorisado nga mag-abri sini nga page. Kun pamati mo nga sayop ini, alayon pag-contact san administrator.", html.Br(),
                        html.Small("(You're not authorized to view this page. Please contact the administrator if you think this is a mistake.)", className = 'text-muted')
                    ]
                ),
                width = error_width
            ),
            justify = error_justify
        ),
        dbc.Row(
            dbc.Col(
                dbc.Badge(
                    "ERROR 403: FORBIDDEN",
                    #color = 'danger'
                ),
                width = error_width
            ),
            justify = error_justify
        ),
    ]
)