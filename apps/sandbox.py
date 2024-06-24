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
from utilities.utils import MarginSettings, CardStyle, RequiredTag, DropdownDataLoader, FormFieldConstructor

input_brgy_id = FormFieldConstructor(
    id_prefix = 'sbox',
    id_actual = 'brgy_id',
    input_type = dcc.Dropdown,
    label_war = "Barangay",
    label_en = "Barangay",
    required = True,
    form_text_war = "Kun opisyal ka san barangay, awtomatiko nga pipilion dinhi an imo barangay.",
    form_text_en = "If you are a barangay official, your barangay will be automatically selected."
)

input_docu = FormFieldConstructor(
    id_prefix = 'sbox',
    id_actual = 'docu',
    input_type = dcc.Upload,
)

layout = html.Div(
    [
        dcc.Store(id = 'sandbox_event_id', data = 1),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Form(
                            [
                                # Common information
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H1(
                                                    "File a report",
                                                    id = 'sbox_h1_header'
                                                ),
                                                html.P(
                                                    [
                                                        "Kinihanglan pun-on an mga patlang nga may pula nga asterisk ", RequiredTag.tag, ".",
                                                        html.Br(),
                                                        html.Small(
                                                            ["(Fields with red asterisks ", RequiredTag.tag, " are required.)"],
                                                            className = 'text-muted'
                                                        )
                                                    ], className = MarginSettings.paragraph
                                                )
                                            ],
                                            id = 'sbox_row_header',
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [

                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ]
                                )
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