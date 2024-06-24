# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import pytz
# App definition
from app import app
from apps import dbconnect as db
from utilities.utils import MarginSettings, CardStyle, DropdownDataLoader

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
                                            className = MarginSettings.paragraph
                                        )
                                    ],
                                    class_name = MarginSettings.row,
                                ),
                            ],
                            id = 'com_das_div_header',
                            className = MarginSettings.header
                        ),
                        html.Hr(),
                        # Cards
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.A(
                                                    dbc.Card(
                                                        [
                                                            html.H1(html.I(className = 'bi bi-pencil-square')),
                                                            html.H4("Maghimo report", className = 'mb-3'),
                                                            html.Hr(className = 'my-1'),
                                                            html.P(
                                                                [
                                                                    "Himo kit bag-o nga report didi.",
                                                                    html.Small(
                                                                        " (Let's file new reports here.)",
                                                                        className = 'text-muted'
                                                                    )
                                                                ],
                                                                className = MarginSettings.paragraph # + ' text-muted'
                                                            )
                                                        ],
                                                        body = True,
                                                        style = CardStyle.get_style(),
                                                        class_name = 'hover-enlarge'
                                                    ),
                                                    href = '/reports/create?mode=new'
                                                )
                                            ],
                                            class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                html.A(
                                                    dbc.Card(
                                                        [
                                                            html.H1(html.I(className = 'bi bi-calendar-event')),
                                                            html.H4("Mga panhitabó", className = 'mb-3'),
                                                            html.Hr(className = 'my-1'),
                                                            html.P(
                                                                [
                                                                    "An lista san mga panhitabó.",
                                                                    html.Small(
                                                                        " (The list of events.)",
                                                                        className = 'text-muted'
                                                                    )
                                                                ],
                                                                className = MarginSettings.paragraph # + ' text-muted'
                                                            )
                                                        ],
                                                        body = True,
                                                        style = CardStyle.get_style(),
                                                        class_name = 'hover-enlarge'
                                                    ),
                                                    href = '/events'
                                                )
                                            ],
                                            class_name = 'mb-3 mb-lg-0 col-12 col-sm-6 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                html.A(
                                                    dbc.Card(
                                                        [
                                                            html.H1(html.I(className = 'bi bi-houses')),
                                                            html.H4("Aton barangay", className = 'mb-3'),
                                                            html.Hr(className = 'my-1'),
                                                            html.P(
                                                                [
                                                                    "Populasyon ug mga hazard.",
                                                                    html.Small(
                                                                        " (Population and hazards.)",
                                                                        className = 'text-muted'
                                                                    )
                                                                ],
                                                                className = MarginSettings.paragraph # + ' text-muted'
                                                            )
                                                        ],
                                                        body = True,
                                                        style = CardStyle.get_style(),
                                                        class_name = 'hover-enlarge'
                                                    ),
                                                    href = '/data/barangays'
                                                )
                                            ],
                                            class_name = 'mb-3 mb-md-0 col-12 col-sm-6 col-lg-3'
                                        ),
                                        dbc.Col(
                                            [
                                                html.A(
                                                    dbc.Card(
                                                        [
                                                            html.H1(html.I(className = 'bi bi-house-add')),
                                                            html.H4("Mag-profile balay", className = 'mb-3'),
                                                            html.Hr(className = 'my-1'),
                                                            html.P(
                                                                [
                                                                    "Para community profiling.",
                                                                    html.Small(
                                                                        " (For community profiling.)",
                                                                        className = 'text-muted'
                                                                    )
                                                                ],
                                                                className = MarginSettings.paragraph # + ' text-muted'
                                                            )
                                                        ],
                                                        body = True,
                                                        style = CardStyle.get_style(),
                                                        class_name = 'hover-enlarge'
                                                    ),
                                                    href = '/data/household/upload'
                                                )
                                            ],
                                            class_name = 'col-12 col-sm-6 col-lg-3'
                                        ),
                                    ],
                                    class_name = 'mb-3'
                                ),
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
                                                                    ], class_name = MarginSettings.row
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
                                                    style = CardStyle.get_style(),
                                                    #class_name = 'hover-enlarge'
                                                )
                                            ],
                                            class_name = 'mb-2 mb-lg-0 col-12 col-lg-7'
                                        ),
                                        dbc.Col(
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
                                                                                                            html.I(className = 'bi bi-calendar-event-fill me-2'),
                                                                                                            "Mga aktibo nga panhitabó",
                                                                                                            html.Small(" (Active events)", className = 'text-muted'),
                                                                                                        ]
                                                                                                    ),
                                                                                                    href = '/events'
                                                                                                )
                                                                                            ]
                                                                                        )
                                                                                    ], class_name = MarginSettings.row
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
                                                                    style = CardStyle.get_style(),
                                                                    #class_name = 'hover-enlarge'
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    class_name = 'mb-3'
                                                ),
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
                                                                                                            html.I(className = 'bi bi-exclamation-diamond-fill me-2'),
                                                                                                            "Mga hazard sa mga barangay",
                                                                                                            html.Small(" (Barangay hazards)", className = 'text-muted'),
                                                                                                        ]
                                                                                                    ),
                                                                                                    href = '/data/barangays'
                                                                                                )
                                                                                            ]
                                                                                        )
                                                                                    ], class_name = MarginSettings.row
                                                                                ),
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            dcc.Dropdown(
                                                                                                id = 'com_das_input_brgy_id',
                                                                                                clearable = True,
                                                                                                value = 1,
                                                                                                placeholder = "Barangay"
                                                                                            ),
                                                                                            #class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-10'
                                                                                        ),
                                                                                    ], className = 'mb-3',
                                                                                    id = 'com_das_row_selectbrgy'
                                                                                ),
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                                html.H1(
                                                                                                    [
                                                                                                        html.I(className = 'fa fa-house-flood-water me-2'),
                                                                                                        html.Span("-", id = 'com_das_spa_vul_flood')
                                                                                                    ],
                                                                                                    id = 'com_das_h1_vul_flood',
                                                                                                    style = {'color' : 'gray'}
                                                                                                ),
                                                                                            ],
                                                                                            class_name = 'd-flex justify-content-center'
                                                                                        ),
                                                                                        dbc.Tooltip(
                                                                                            "Posibilidad san pagbaha (possibility of flooding).",
                                                                                            target = 'com_das_h1_vul_flood',
                                                                                            #body = True,
                                                                                            #trigger = 'focus',
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            [
                                                                                                html.H1(
                                                                                                    [
                                                                                                        html.I(className = 'fa fa-hill-rockslide me-2'),
                                                                                                        html.Span("-", id = 'com_das_spa_vul_landslide')
                                                                                                    ],
                                                                                                    id = 'com_das_h1_vul_landslide',
                                                                                                    style = {'color' : 'gray'}
                                                                                                ),
                                                                                            ],
                                                                                            class_name = 'd-flex justify-content-center'
                                                                                        ),
                                                                                        dbc.Tooltip(
                                                                                            "Posibilidad san pagtimpag san tuna (possibility of landslides).",
                                                                                            target = 'com_das_h1_vul_landslide',
                                                                                            #body = True,
                                                                                            #trigger = 'focus',
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            [
                                                                                                html.H1(
                                                                                                    [
                                                                                                        html.I(className = 'fa fa-house-tsunami me-2'),
                                                                                                        html.Span("-", id = 'com_das_spa_vul_stormsurge')
                                                                                                    ],
                                                                                                    id = 'com_das_h1_vul_stormsurge',
                                                                                                    style = {'color' : 'gray'}
                                                                                                ),
                                                                                            ],
                                                                                            class_name = 'd-flex justify-content-center'
                                                                                        ),
                                                                                        dbc.Tooltip(
                                                                                            "Posibilidad san storm surge (possibility of storm surge).",
                                                                                            target = 'com_das_h1_vul_stormsurge',
                                                                                            #body = True,
                                                                                            #trigger = 'focus',
                                                                                        ),
                                                                                    ], class_name = MarginSettings.row
                                                                                ),
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                                """Tikang ini nga datos sa National Operational
                                                                                                Assessment of Hazards (NOAH) san University of the Philippines
                                                                                                Resilience Institute (UPRI)."""
                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ]
                                                                        )
                                                                    ],
                                                                    style = CardStyle.get_style(),
                                                                    #class_name = 'hover-enlarge'
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    class_name = 'h-auto'
                                                )
                                            ],
                                            class_name = 'mb-2 mb-lg-0 col-12 col-lg-5'
                                        ),
                                    ],
                                    class_name = MarginSettings.row,
                                )
                            ],
                            id = 'com_das_div_cards',
                            className = MarginSettings.div
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

        sql += ") ORDER BY rv.create_time ASC;"
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
                    'title' : 'Petsa (Date)',
                    #'range' : [df['Creation time'][0], datetime.now()],
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

# Callback for populating dropdowns
@app.callback(
    [
        # Selected barangay
        Output('com_das_input_brgy_id', 'options'),
        Output('com_das_input_brgy_id', 'value'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data'),
        State('com_das_input_brgy_id', 'value'),
    ]
)

def com_das_populatedropdowns(pathname, region, province, citymun, brgy, selectedbrgy):
    if pathname == '/dashboard':
        dropdowns = []
        ddl = DropdownDataLoader(db)

        # Barangays
        brgys = ddl.load_barangays(region, province, citymun)
        dropdowns.append(brgys)

        if brgy > 0: dropdowns.append(brgy)
        else: dropdowns.append(selectedbrgy)

        return dropdowns
    else: raise PreventUpdate


# Callback for showing barangay-specific information
@app.callback(
    [
        # Flood vulnerability
        Output('com_das_spa_vul_flood', 'children'),
        Output('com_das_h1_vul_flood', 'style'),
        # Landslide vulnerability
        Output('com_das_spa_vul_landslide', 'children'),
        Output('com_das_h1_vul_landslide', 'style'),
        # Storm surge vulnerability
        Output('com_das_spa_vul_stormsurge', 'children'),
        Output('com_das_h1_vul_stormsurge', 'style'),
    ],
    [
        #Input('url', 'pathname'),
        Input('com_das_input_brgy_id', 'value')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgyinfo_cols', 'data'),
        State('app_latestcensusyear', 'data')
    ]
)

def com_das_setbrgyinfo(brgy, region, province, citymun, info_cols, censusyear):
    if brgy:
        toreturn = []

        # Header
        header = None
        sql = """SELECT addressbrgy.name, addressbrgy.pop_2000, addressbrgy.pop_2007, addressbrgy.pop_2010, addressbrgy.pop_2015, addressbrgy.pop_2020,
            addressbrgy.vul_flood, addressbrgy.vul_landslide, addressbrgy.vul_stormsurge,
            vultype_flood.label_war, vultype_landslide.label_war, vultype_stormsurge.label_war,
            vultype_flood.label_en, vultype_landslide.label_en, vultype_stormsurge.label_en,
            vultype_flood.color, vultype_landslide.color, vultype_stormsurge.color,
            vultype_flood.score, vultype_landslide.score, vultype_stormsurge.score,
            addressbrgy.map_src
            FROM utilities.addressbrgy
            LEFT JOIN utilities.vultype AS vultype_flood ON addressbrgy.vul_flood = vultype_flood.id
            LEFT JOIN utilities.vultype AS vultype_landslide ON addressbrgy.vul_landslide = vultype_landslide.id
            LEFT JOIN utilities.vultype AS vultype_stormsurge ON addressbrgy.vul_stormsurge = vultype_stormsurge.id
            WHERE addressbrgy.region_id = %s AND addressbrgy.province_id = %s AND addressbrgy.citymun_id = %s AND addressbrgy.id = %s;"""
        values = [region, province, citymun, brgy]
        cols = info_cols + [
            'vul_flood', 'vul_landslide', 'vul_stormsurge',
            'label_war_flood', 'label_war_landslide', 'label_war_stormsurge',
            'label_en_flood', 'label_en_landslide', 'label_en_stormsurge',
            'color_flood', 'color_landslide', 'color_stormsurge',
            'score_flood', 'score_landslide', 'score_stormsurge',
            'map_src'
            ]
        df = db.querydatafromdatabase(sql, values, cols)
            
        # Flood vulnerability
        toreturn.append(df['vul_flood'][0])
        toreturn.append({'color' : df['color_flood'][0]})
        # Landslide vulnerability
        toreturn.append(df['vul_landslide'][0])
        toreturn.append({'color' : df['color_landslide'][0]})
        # Storm surge vulnerability
        toreturn.append(df['vul_stormsurge'][0])
        toreturn.append({'color' : df['color_stormsurge'][0]})

        return toreturn
    else: raise PreventUpdate