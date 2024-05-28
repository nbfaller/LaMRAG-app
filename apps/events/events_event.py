# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from urllib.parse import urlparse, parse_qs
# App definition
from app import app
from apps import dbconnect as db

tag_required = html.Sup("*", className = 'text-danger')
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
                                    ),
                                    class_name = row_m,
                                ),
                                dbc.Row(
                                    [
                                        html.H1(
                                            "Event profile",
                                            id = 'eve_eve_h1_header'
                                        ),
                                    ],
                                    class_name = row_m,
                                )
                            ],
                            id = 'eve_eve_div_header',
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
                                                        id = 'eve_eve_col_basicinfo',
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
                            id = 'eve_eve_div_basicinfo',
                            className = div_m
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H4(
                                            [
                                                html.I(className = 'bi bi-body-text me-2'),
                                                "Deskripsiyon",
                                                #html.Br(),
                                                html.Small(" (Description)", className = 'text-muted')
                                            ]
                                        ),
                                    ], class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        html.P(
                                            id = 'eve_eve_htp_description',
                                            className = p_m,
                                            style = {
                                                'white-space' : 'pre-wrap'
                                            }
                                        )
                                    ],
                                    class_name = row_m,
                                )
                            ],
                            id = 'eve_eve_div_description',
                            className = div_m + ' d-block'
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
                                    ],
                                    class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardBody(
                                                        [
                                                            html.H5(
                                                                [
                                                                    html.I(className = 'bi bi-tag me-2'),
                                                                    "Mga nasumite nga kada klase san report",
                                                                    #html.Br(),
                                                                    html.Small(" (Submitted reports per type)", className = 'text-muted')
                                                                ],
                                                                #className = 'm-0'
                                                            ),
                                                            dcc.Graph(
                                                                id = 'eve_eve_gra_reportsfiled'
                                                            )
                                                        ]
                                                    )
                                                ],
                                                style = card_style
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-7 col-lg-8'
                                        ),
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardBody(
                                                        [
                                                            html.H5(
                                                                [
                                                                    html.I(className = 'bi bi-check-circle me-2'),
                                                                    "Proporsiyon san mga naprubaran nga report",
                                                                    html.Br(),
                                                                    html.Small(" (Proportion of verified reports)", className = 'text-muted')
                                                                ],
                                                                #className = 'm-0'
                                                            ),
                                                            dcc.Graph(
                                                                id = 'eve_eve_gra_verifiedpiechart'
                                                            )
                                                        ]
                                                    )
                                                ],
                                                style = card_style
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-5 col-lg-4'
                                        )
                                    ]
                                ),
                            ],
                            id = 'eve_eve_div_data',
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
                                    ], class_name = row_m
                                ),
                            ],
                            id = 'eve_eve_div_reports',
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

eve_eve_url_pathname = '/events/event'

# Callback for displaying event details
@app.callback(
    [
        Output('eve_eve_h1_header', 'children'),
        Output('eve_eve_htp_description', 'children'),
        Output('eve_eve_div_description', 'className'),
        Output('eve_eve_col_basicinfo', 'children'),
        Output('eve_eve_gra_reportsfiled', 'figure'),
        Output('eve_eve_gra_verifiedpiechart', 'figure'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search'),
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data')
    ]
)

def eve_eve_setevent(pathname, search, region, province, citymun, brgy):
    if pathname == eve_eve_url_pathname:
        to_return = []
        event_header = "Event profile"
        description_class = 'd-none'
        parsed = urlparse(search)
        if parse_qs(parsed.query):
            event_id = parse_qs(parsed.query)['id'][0]
            if event_id:
                sql = """SELECT e.name,
                CONCAT(et.symbol, ' ', et.label_war, ' (', et.label_en, ')'),
                TO_CHAR(e.startdate, 'Month dd, yyyy'), TO_CHAR(e.enddate, 'Month dd, yyyy'),
                e.description,
                CONCAT(u.lname, ', ', COALESCE(u.livedname, u.fname), ' ', LEFT(u.mname, 1), ' (', u.username, ')') AS creator,
                TO_CHAR(e.create_time::timestamp AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Manila', 'Month dd, yyyy • HH:MI:SS AM'),
                CAST(e.is_active AS TEXT) AS status,
                TO_CHAR(e.is_active_time::timestamp AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Manila', 'Month dd, yyyy • HH:MI:SS AM') AS status_time
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
                if df['Deskripsiyon (Description)'][0]:
                    description_class = div_m + ' d-block'
                to_return.append(description_class)

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

                # Stacked area chart of reports filed
                sql = """SELECT rv.status_time,
                CONCAT(rt.symbol, ' ', rt.label_war, ' (', rt.label_en, ')') AS report_type
                FROM reports.reportversion AS rv
                LEFT JOIN reports.report AS r ON rv.report_id = r.id
                LEFT JOIN events.event AS e ON r.event_id = e.id
                LEFT JOIN utilities.reporttype AS rt ON r.type_id = rt.id
                WHERE e.is_active
                AND (r.region_id = %s AND r.province_id = %s
                AND r.citymun_id = %s)
                AND e.id = %s
                AND rv.status_id = 2;
                """
                values = [region, province, citymun, event_id]
                cols = ['Validation time', 'Report type']
                df = db.querydatafromdatabase(sql, values, cols)
                #print(df)
                df['Validation time'] = pd.to_datetime(df['Validation time'])
                df = df.groupby([df['Validation time'], 'Report type']).size().unstack(fill_value = 0).cumsum().reset_index()
                df.columns.name = None
                #print(df)

                traces = []
                for event in df.columns[1:]:
                    traces.append(
                        go.Scatter(
                            x = df['Validation time'],
                            y = df[event],
                            mode = 'lines',
                            name = event,
                            stackgroup = 'one',  # This parameter makes it a stacked area chart
                            #line = {'shape': 'spline', 'smoothing': 1.3}
                        )
                    )

                layout = go.Layout(
                    {
                        'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor' : 'rgba(0, 0, 0, 0)'
                    },
                    #title = 'Cumulative reports filed over time',
                    xaxis = {
                        'title': 'Petsa (Date)'
                    },
                    yaxis = {
                        'title': 'Mga ginhimo nga report (Reports filed)'
                    },
                    font_family = "DM Sans",
                    showlegend = True,
                    legend = {
                        'orientation' : 'h',
                        'xanchor' : 'left',
                        'yanchor' : 'top',
                        'x' : 0.00,
                        'y' : -0.25
                    },
                    template = 'plotly_white',
                    margin = {
                        't' : 0,
                        'b' : 0,
                        'l' : 0,
                        'r' : 0,
                        'pad' : 0
                    }
                )

                to_return.append({'data': traces, 'layout': layout})

                # Pie chart of reports validation
                sql = """SELECT CONCAT(rs.label_war, ' (', rs.label_en, ')') AS status,
                COUNT(*) as count
                FROM reports.reportversion AS rv
                LEFT JOIN reports.report AS r ON rv.report_id = r.id
                LEFT JOIN events.event AS e ON r.event_id = e.id
                LEFT JOIN utilities.reportstatus AS rs ON rv.status_id = rs.id
                WHERE e.is_active
                AND (r.region_id = %s AND r.province_id = %s
                AND r.citymun_id = %s)
                AND e.id = %s
                GROUP BY status;
                """
                values = [region, province, citymun, event_id]
                cols = ['Validation status', 'Reports']
                df = db.querydatafromdatabase(sql, values, cols)
                #print(df)

                slices = [
                    go.Pie(
                        labels = df['Validation status'],
                        values = df['Reports'],
                        hole = .3
                    )
                ]

                layout = go.Layout(
                    {
                        'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor' : 'rgba(0, 0, 0, 0)'
                    },
                    #title = 'Distribution of reports by status',
                    font_family = "DM Sans",
                    showlegend = True,
                    legend = {
                        'orientation' : 'h',
                        'xanchor' : 'left',
                        'yanchor' : 'top',
                        'x' : 0.00,
                        'y' : 0.00
                    },
                    template = 'plotly_white',
                    margin = {
                        't' : 0,
                        'b' : 0,
                        'l' : 0,
                        'r' : 0,
                        'pad' : 0
                    }
                )

                to_return.append({'data': slices, 'layout': layout})

            else: raise PreventUpdate
        else: raise PreventUpdate
        return to_return
    else: raise PreventUpdate