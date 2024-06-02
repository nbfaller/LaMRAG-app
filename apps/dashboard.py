# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
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
                                    [
                                        html.H1(
                                            "User dashboard",
                                            id = 'com_das_h1_header'
                                        ),
                                        html.P(
                                            "User information",
                                            id = 'com_das_htp_userdetails',
                                            className = p_m
                                        )
                                    ],
                                    class_name = row_m,
                                ),
                            ],
                            id = 'com_das_div_header',
                            className = header_m
                        ),
                        html.Hr(),
                        # Cards
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.A(
                                                                                    html.H4(
                                                                                        [
                                                                                            html.I(className = 'bi bi-file-earmark-bar-graph-fill me-2'),
                                                                                            "Mga ginsumite nga report",
                                                                                            html.Small(" (Reports filed)", className = 'text-muted')
                                                                                        ]
                                                                                    ),
                                                                                    href = '/reports'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ], class_name = row_m
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                dcc.Graph(
                                                                                    id = 'com_das_gra_reportsfiled'
                                                                                ),
                                                                                html.H4(
                                                                                    [
                                                                                        html.I(className = 'bi bi-search me-2'),
                                                                                        html.Br(),
                                                                                        "Waray pa nasusumite nga report ini nga barangay.",
                                                                                        html.Br(),
                                                                                        html.Small("(This barangay is yet to submit reports.)")
                                                                                    ],
                                                                                    id = 'com_das_h3_grapherror',
                                                                                    className = 'd-none mb-0 text-center text-muted'
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    style = card_style
                                                )
                                            ],
                                            class_name = 'mb-2 mb-lg-0 col-12 col-lg-7'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.A(
                                                                                    html.H4(
                                                                                        [
                                                                                            html.I(className = 'bi bi-calendar-event-fill me-2'),
                                                                                            "Mga aktibo nga panhitabó",
                                                                                            html.Small(" (Active events)", className = 'text-muted'),
                                                                                        ]
                                                                                    ),
                                                                                    href = '/events'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ], class_name = row_m
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            id = 'com_das_col_eventstable'
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    style = card_style
                                                )
                                            ],
                                            class_name = 'mb-2 mb-lg-0 col-12 col-lg-5'
                                        ),
                                    ],
                                    class_name = row_m,
                                )
                            ],
                            id = 'com_das_div_cards',
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

com_das_pathname = '/dashboard'

@app.callback(
    [
        Output('com_das_htp_userdetails', 'children'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('app_currentuser_id', 'data'),
        #State('app_usertype_id', 'data')
    ]
)

def com_das_setpagedetails(
    pathname, user_id, #type_id
):
    if pathname == com_das_pathname:
        details = "User information"
        sql = """SELECT u.lname, u.fname, u.mname, u.livedname,
            ut.label
            FROM users.user AS u
            LEFT JOIN utilities.usertype AS ut ON u.usertype_id = ut.id
            WHERE u.id = %s;
            """
        values = [user_id]
        cols = ['lname', 'fname', 'mname', 'livedname', 'usertype']
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0]:
            lname = df['lname'][0]
            mname = df['mname'][0][0] + "." if df['mname'][0] else None
            fname = df['livedname'][0] if df['livedname'][0] else df['fname'][0]
            usertype = df['usertype'][0]
            
            details = "%s %s %s • %s" % (fname, mname, lname, usertype)
        
        return [details]
    else: raise PreventUpdate

# Callback for generating reports graph and events table
@app.callback(
    [
        Output('com_das_gra_reportsfiled', 'figure'),
        Output('com_das_gra_reportsfiled', 'style'),
        Output('com_das_h3_grapherror', 'className'),
        Output('com_das_col_eventstable', 'children')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data'),
    ]
)

def com_das_generatereportsgraph(pathname, region, province, citymun, brgy):
    fig = None
    class_name = 'd-none'
    style = {'display' : 'none'}
    table = html.H4(
        [
            html.I(className = 'bi bi-search me-2'),
            html.Br(),
            "Waray aktibo nga panhitabó ini nga barangay.",
            html.Br(),
            html.Small("(This barangay has no active events.)")
        ],
        #id = 'com_das_h3_grapherror',
        className = 'd-block m-3 text-center text-muted'
    )

    if pathname == com_das_pathname:
        # Stacked area chart of reports filed
        sql = """SELECT rv.create_time,
        e.name AS event
        FROM reports.reportversion AS rv
        LEFT JOIN reports.report AS r ON rv.report_id = r.id
        LEFT JOIN events.event AS e ON r.event_id = e.id
        WHERE e.is_active
        AND (r.region_id = %s AND r.province_id = %s
        AND r.citymun_id = %s
        """
        values = [region, province, citymun]
        cols = ['Creation time', 'Event']

        if int(brgy) > 0:
            sql += " AND r.brgy_id = %s"
            values += [brgy]

        sql += ");"
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape[0]:
            style = {'display' : 'block'}
            df['Creation time'] = pd.to_datetime(df['Creation time'])
            df = df.groupby([df['Creation time'], 'Event']).size().unstack(fill_value = 0).cumsum().reset_index()
            df.columns.name = None

            traces = []
            for event in df.columns[1:]:
                traces.append(
                    go.Scatter(
                        x = df['Creation time'],
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
                legend = {
                    'orientation' : 'h',
                    'xanchor' : 'left',
                    'yanchor' : 'top',
                    'x' : 0.00,
                    'y' : -0.25
                },
                showlegend = True,
                template = 'plotly_white',
                margin = {
                    't' : 0,
                    'b' : 0,
                    'l' : 0,
                    'r' : 0,
                    'pad' : 0
                }
            )
            fig = {'data': traces, 'layout': layout}
        else: 
            class_name = 'd-block m-3 text-center text-muted'
        
        # Events table
        sql = """SELECT DISTINCT ON (e.id)
        e.id AS id,
        e.name AS name
        FROM events.event AS e
        LEFT JOIN utilities.eventtype AS et ON e.type_id = et.id
        LEFT JOIN events.eventbrgy AS eb ON e.id = eb.event_id
        WHERE e.is_active AND (eb.region_id = %s AND eb.province_id = %s
        AND eb.citymun_id = %s
        """
        values = [region, province, citymun]

        if int(brgy) > 0:
            sql += " AND eb.brgy_id = %s"
            values += [brgy]
            
        sql += ") ORDER BY e.id ASC;"
        cols = ['ID No.', 'Name',]
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0]:
            for i in df.index:
            # Names as hyperlinks
                df.loc[i, 'Name'] = html.A(
                    df['Name'][i],
                    href = '/events/event?id=%s' % df['ID No.'][i],
                )
            df = df[['Name']]
            table = dbc.Table.from_dataframe(
                df,
                striped = False,
                bordered = False,
                hover = True,
                size = 'sm'
            )
        
    return [
        fig,
        style,
        class_name,
        table
    ]