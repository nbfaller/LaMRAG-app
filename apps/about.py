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
hyperlink_style = {
    'text-decoration' : 'none',
    'color' : 'inherit'
}
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
        dcc.Store(id = 'com_abt_sto_brgycurrentpop'),
        dcc.Store(id = 'com_abt_sto_brgypctchange'),
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
                                            [
                                                "Hiúnong san LáMRAG",
                                                #html.Br(),
                                                html.Small(" (About LáMRAG)", className = 'text-muted')
                                            ],
                                            id = 'com_abt_h1_header'
                                        ),
                                    ],
                                    class_name = row_m,
                                ),
                                dbc.Row(
                                    [
                                        html.Img(
                                            src = app.get_asset_url('lamrag-wordmark-dmsans-dark.png'),
                                            style = {
                                                'width' : '256px',
                                            }
                                        )
                                    ],
                                    className = 'mt-2 mb-3 py-3 justify-content-center'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H5(
                                                [
                                                    """An LáMRAG in """,
                                                    html.B("Local Management Platform for Risk Analytics and Governance"),
                                                    """ san Siyudad san Calbayog. Usa ini nga web-based information system nga tuyo
                                                    an pag-standardize ug pag-digitize san mga proseso hiúnong san incident reporting,
                                                    data banking, ug data analysis san City Disaster Risk Reduction & Management
                                                    Office (CDRRMO) san Calbayog. Ginhimo ini gamit an Python ug Dash, ug produkto ini
                                                    san halaba nga proseso san systems engineering ug requirements analysis.
                                                    """
                                                ],
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Small(
                                                [
                                                    """LáMRAG is the """,
                                                    html.B("Local Management Platform for Risk Analytics and Governance"),
                                                    """ of the City of Calbayog. It is a web-based information system that aims to
                                                    standardize the incident reporting, data banking, and data analysis processes
                                                    of Calbayog's City Disaster Risk Reduction & Management Office (CDRRMO). LáMRAG
                                                    was developed using Python and Dash and is the result of a lengthy process of
                                                    systems engineering and requirements analysis.
                                                    """
                                                ],
                                                className = 'text-muted'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                ),
                            ],
                            id = 'com_abt_div_header',
                            className = header_m
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.P(
                                                [
                                                    """LáMRAG is the output of a capstone project in IE 194 and 195 (Industrial Engineering
                                                    Capstone Project I & II) by BS Industrial Engineering students at the 
                                                    """,
                                                    html.A(
                                                        html.B("Industrial Engineering and Operations Research Department (IEORD)"),
                                                        href = 'https://ieor.engg.upd.edu.ph',
                                                        style = hyperlink_style
                                                    ),
                                                    """ of the University of the Philippines College of Engineering in Diliman, Quezon City.
                                                    The project team is composed of:"""
                                                ],
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                ),
                            ],
                            id = 'com_abt_div_team',
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