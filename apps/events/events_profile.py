# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from urllib.parse import urlparse, parse_qs
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Header
                        html.Div(
                            [
                                dbc.Row(
                                    dbc.Col(
                                        dbc.Badge(
                                            "EVENT",
                                            #color = 'danger'
                                        ),
                                        width = 'auto'
                                    )
                                ),
                                dbc.Row(
                                    [
                                        html.H1(
                                            "Event profile",
                                            id = 'eve_pro_h1_header'
                                        ),
                                        html.P(
                                            id = 'eve_pro_htp_description',
                                            className = p_m
                                        )
                                    ],
                                    class_name = row_m,
                                )
                            ],
                            id = 'eve_pro_div_header',
                            className = header_m
                        ),
                        html.Hr(),
                        # Basic information
                        html.Div(
                            [
                                #dbc.Card(
                                    #dbc.CardBody(
                                        #[
                                            dbc.Row(
                                                [
                                                    html.H4(
                                                        [
                                                            html.I(className = 'bi bi-exclamation-square-fill me-2'),
                                                            "Primero nga impormasyon",
                                                            #html.Br(),
                                                            html.Small(" (Basic information)", className = 'text-muted')
                                                        ]
                                                    ),
                                                ], class_name = row_m
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        id = 'eve_pro_col_basicinfo',
                                                        #class_name = 'table-responsive',
                                                        style = {
                                                            'max-width' : '100%',
                                                            'overflow' : 'scroll'
                                                        }
                                                    )
                                                ], #class_name = row_m
                                            )
                                        #]
                                    #),
                                    #style = card_style
                                #)
                            ],
                            id = 'eve_pro_div_basicinfo',
                            className = div_m
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H4(
                                            [
                                                html.I(className = 'bi bi-graph-up me-2'),
                                                "Data summary",
                                                #html.Br(),
                                                #html.Small(" (Generated consolidated reports)", className = 'text-muted')
                                            ]
                                        ),
                                    ], class_name = row_m
                                ),
                            ],
                            id = 'eve_pro_div_data',
                            className = div_m
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H4(
                                            [
                                                html.I(className = 'bi bi-clipboard-data-fill me-2'),
                                                "Mga ginhimo nga consolidated report",
                                                #html.Br(),
                                                html.Small(" (Generated consolidated reports)", className = 'text-muted')
                                            ]
                                        ),
                                    ], class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            id = 'eve_pro_col_reportsgraph',
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-4'
                                        ),
                                        dbc.Col(
                                            id = 'eve_pro_col_reportsgraph',
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-8'
                                        )
                                    ]
                                ),
                            ],
                            id = 'eve_pro_div_reports',
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

eve_pro_url_pathname = '/events/profile'

# Callback for displaying event details
@app.callback(
    [
        Output('eve_pro_h1_header', 'children'),
        Output('eve_pro_htp_description', 'children'),
        Output('eve_pro_col_basicinfo', 'children'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)

def eve_pro_setevent(pathname, search):
    if pathname == eve_pro_url_pathname:
        to_return = []
        event_header = "Event profile"
        parsed = urlparse(search)
        if parse_qs(parsed.query):
            event_id = parse_qs(parsed.query)['id'][0]
            if event_id:
                sql = """SELECT e.name,
                CONCAT(et.symbol, ' ', et.label_war, ' (', et.label_en, ')'),
                TO_CHAR(e.startdate, 'Month dd, yyyy'), TO_CHAR(e.enddate, 'Month dd, yyyy'),
                e.description,
                CONCAT(u.lname, ', ', COALESCE(u.livedname, u.fname), ' ', LEFT(u.mname, 1), ' (', u.username, ')') AS creator,
                TO_CHAR(e.create_time, 'Month dd, yyyy • HH:MI:SS AM'),
                CAST(e.is_active AS TEXT) AS status,
                TO_CHAR(e.is_active_time, 'Month dd, yyyy • HH:MI:SS AM') AS status_time
                FROM events.event AS e
                LEFT JOIN utilities.eventtype AS et ON e.type_id = et.id
                LEFT JOIN users.user AS u ON e.creator_id = u.id
                WHERE e.id = %s;
                """
                values = [event_id]
                cols = [
                    'Name', 'Klase (Type)', 'Petsa san pagtikang (Start date)', 'Petsa san pagtapos (End date)',
                    'Deskripsiyon (Description)', 'Naghimo (Creator)', 'Oras san paghimo (Creation time)',
                    'Kamutangan (Status)', 'Oras san kamutangan (Status time)'
                ]
                df = db.querydatafromdatabase(sql, values, cols)

                # Header
                to_return.append(df['Name'][0])
                # Description
                to_return.append(df['Deskripsiyon (Description)'][0])

                # Basic information table
                table_df = df[['Klase (Type)', 'Petsa san pagtikang (Start date)', 'Petsa san pagtapos (End date)', 'Naghimo (Creator)', 'Oras san paghimo (Creation time)', 'Kamutangan (Status)', 'Oras san kamutangan (Status time)']].transpose()
                table_df.insert(
                    0,
                    "Information",
                    [
                        html.Span(
                            [
                                html.I(className = 'bi bi-tag me-2'),
                                html.B("Klase"),
                                html.Small(" (Type)", className = 'text-muted')
                            ]
                        ),
                        html.Span(
                            [
                                html.I(className = 'bi bi-calendar-event me-2'),
                                html.B("Petsa san pagtikang"),
                                html.Small(" (Start date)", className = 'text-muted')
                            ]
                        ),
                        html.Span(
                            [
                                html.I(className = 'bi bi-calendar3-range me-2'),
                                html.B("Petsa san pagtapos"),
                                html.Small(" (End date)", className = 'text-muted')
                            ]
                        ),
                        html.Span(
                            [
                                html.I(className = 'bi bi-person me-2'),
                                html.B("Naghimo"),
                                html.Small(" (Creator)", className = 'text-muted')
                            ]
                        ),
                        html.Span(
                            [
                                html.I(className = 'bi bi-clock me-2'),
                                html.B("Oras san paghimo"),
                                html.Small(" (Creation time)", className = 'text-muted')
                            ]
                        ),
                        html.Span(
                            [
                                html.I(className = 'bi bi-patch-question me-2'),
                                html.B("Kamutangan"),
                                html.Small(" (Status)", className = 'text-muted')
                            ]
                        ),
                        html.Span(
                            [
                                html.I(className = 'bi bi-clock-history me-2'),
                                html.B("Oras san kamutangan"),
                                html.Small(" (Status time)", className = 'text-muted')
                            ]
                        ),
                    ],
                    True
                )
                table_df = table_df.rename(columns={'Information' : '', 0 : ''})
                table = dbc.Table.from_dataframe(
                    table_df,
                    striped = False,
                    bordered = False,
                    hover = False,
                    size = 'sm',
                    borderless = True,
                    style = {'margin' : '0px'}
                )
                to_return.append(table)
            else: raise PreventUpdate
        else: raise PreventUpdate
        return to_return
    else: raise PreventUpdate