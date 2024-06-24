# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import hashlib
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# App definition
from app import app
from apps import dbconnect as db
from utilities.utils import MarginSettings, CardStyle, RequiredTag, DropdownDataLoader

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
                                            "View reports",
                                            id = 'rep_vie_h1_header'
                                        ),
                                    ],
                                    class_name = MarginSettings.row,
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Barangay", RequiredTag.tag, #html.Br(),
                                                    #html.Small(" (Event)", className = 'text-muted')
                                                ],
                                                id = 'rep_vie_label_brgy_id',
                                                class_name = MarginSettings.label
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-2'
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id = 'rep_vie_input_brgy_id',
                                                    clearable = True,
                                                    disabled = True,
                                                ),
                                                #dbc.FormText(
                                                #    "Kun opisyal ka san barangay, awtomatiko nga pipilion dinhi an imo barangay. (If you are a barangay official, your barangay will be automatically selected.)",
                                                #    color = 'secondary',
                                                #    class_name = MarginSettings.form_text
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-10'
                                        )
                                    ],
                                    id = 'rep_vie_row_brgy_id',
                                    class_name = MarginSettings.row,
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Filter by:", #html.Br(),
                                                    #html.Small(" (Year)", className = 'text-muted')
                                                ],
                                                id = 'rep_vie_label_filter',
                                                class_name = MarginSettings.label
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-2'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_vie_input_reporttype_id',
                                                multi = True,
                                                #type = 'text',
                                                placeholder = "Report type",
                                                #value = 1
                                            ),
                                            class_name = 'align-self-center mb-0 col-12 col-md-9 col-lg-10'
                                        ),
                                    ],
                                    class_name = MarginSettings.row
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_vie_input_event_id',
                                                multi = True,
                                                #type = 'text',
                                                placeholder = "Event",
                                                #value = 1
                                                disabled = True
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-6 col-lg-4'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_vie_input_reportstatus_id',
                                                multi = True,
                                                #type = 'number',
                                                placeholder = "Status",
                                                #min = 1
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-4'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                id = 'rep_vie_input_purok',
                                                type = 'number',
                                                placeholder = "Purok",
                                                min = 1
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-2'
                                        ),
                                    ],
                                    className = MarginSettings.row + ' justify-content-end'
                                )
                            ],
                            id = 'rep_vie_div_header',
                            className = MarginSettings.header
                        ),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.P(
                                                    [
                                                        "Alayon paghinumdom nga diri pa napuprubaran an mga report nga ",
                                                        html.Span("pula", style = {'color' : '#ff5757'}),
                                                        " an kulor.",
                                                        html.Small(
                                                            [
                                                                " (Please note that reports colored in ",
                                                                html.Span("red", style = {'color' : '#ff5757'}),
                                                                " are not yet verified.)",
                                                            ],
                                                            className = 'text-muted'
                                                        )
                                                    ], className = MarginSettings.paragraph
                                                ),
                                            ]
                                        )
                                    ], class_name = MarginSettings.row
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            id = 'rep_vie_col_results',
                                            #className = MarginSettings.div,
                                            style = {
                                                'max-width' : '100%',
                                                'overflow' : 'scroll'
                                            }
                                        )
                                    ]
                                )
                            ],
                            className = MarginSettings.div
                        ),
                        html.Div(
                            [
                                html.Hr(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4(
                                                    [
                                                        html.I(className = 'bi bi-graph-up me-2'),
                                                        "Kadamo san nasumite nga mga report",
                                                        #html.Br(),
                                                        html.Small(" (Number of reports filed)", className = 'text-muted')
                                                    ]
                                                ),
                                            ]
                                        )
                                    ], class_name = MarginSettings.row
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Graph(
                                                id = 'rep_vie_gra_reportsfiled'
                                            )
                                        )
                                    ],
                                    class_name = MarginSettings.row
                                )
                            ],
                            id = 'rep_vie_div_chart',
                            className = MarginSettings.footer + ' d-block'
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.A(
                                                    [
                                                        html.I(className = 'bi bi-arrow-return-left me-2'),
                                                        "Balik sa dashboard",
                                                        html.Small(" (Return to dashboard)", className = 'text-muted')
                                                    ],
                                                    href = '/dashboard'
                                                )
                                            ],
                                            class_name = 'col-auto'
                                        )
                                    ],
                                    class_name = MarginSettings.row + ' justify-content-end'
                                )
                            ],
                            id = 'rep_vie_div_footer',
                            className = MarginSettings.footer
                        )
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        ),
    ]
)

# Callback for populating basic dropdown menus and descriptions
@app.callback(
    [
        Output('rep_vie_input_brgy_id', 'options'),
        Output('rep_vie_input_brgy_id', 'value'),
        Output('rep_vie_input_brgy_id', 'disabled'),
        Output('rep_vie_input_reporttype_id', 'options'),
        Output('rep_vie_input_reportstatus_id', 'options')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data')
    ]
)

def rep_vie_populatedropdowns(pathname, region, province, citymun, brgy):
    conditions = [
        pathname == '/reports',
        pathname == '/reports/view'
    ]
    if any(conditions):
        dropdowns = []
        ddl = DropdownDataLoader(db)
        
        # Barangays
        brgys = ddl.load_barangays(region, province, citymun)
        dropdowns.append(brgys)

        brgy_value, brgy_disabled = ddl.lock_brgy(brgy)
        dropdowns.extend([brgy_value, brgy_disabled])
        
        # Report types
        reporttypes = ddl.load_report_types()
        dropdowns.append(reporttypes)

        # Report statuses
        reportstatuses = ddl.load_report_statuses()
        dropdowns.append(reportstatuses)

        return dropdowns
    else: raise PreventUpdate

# Callback for searching reports
@app.callback(
    [
        Output('rep_vie_col_results', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('rep_vie_input_brgy_id', 'value'),
        Input('rep_vie_input_reporttype_id', 'value'),
        Input('rep_vie_input_event_id', 'value'),
        Input('rep_vie_input_purok', 'value')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
    ]
)

def rep_vie_loadsearchresults(pathname, brgy, type, event, purok, region, province, citymun):
    conditions = [
        pathname == '/reports',
        pathname == '/reports/view'
    ]
    if any(conditions):
        # Retrieve reports as dataframe
        sql = """SELECT
        r.id AS report_id,
		e.name AS event_name,
        CONCAT(rt.symbol, ' ', rt.label_war, ' (', rt.label_en, ')') as reporttype_id,
        ab.name AS brgy,
        r.purok,
        rv.status_id
        FROM reports.report AS r
        LEFT JOIN utilities.reporttype AS rt ON r.type_id = rt.id
		LEFT JOIN events.event AS e ON r.event_id = e.id
        LEFT JOIN utilities.addressbrgy AS ab ON (r.region_id = ab.region_id AND r.province_id = ab.province_id AND r.citymun_id = ab.citymun_id AND r.brgy_id = ab.id)
        LEFT JOIN (
            SELECT rv1.report_id, rv1.status_id
            FROM reports.reportversion AS rv1
            INNER JOIN (
                SELECT report_id, MAX(id) AS version_id
                FROM reports.reportversion
                GROUP BY report_id
            ) AS rv2 ON rv1.report_id = rv2.report_id AND rv1.id = rv2.version_id
        ) AS rv ON r.id = rv.report_id
        WHERE (r.region_id = %s AND r.province_id = %s AND r.citymun_id = %s
        """
        values = [region, province, citymun]
        cols = ['No.', 'Event', 'Report type', 'Barangay', 'Purok', 'Status']

        if brgy and int(brgy) > 0:
            sql += """ AND brgy_id = %s"""
            values += [int(brgy)]
        sql += ")"
            
        if type:
            c = 1
            sql += """ AND ("""
            for i in type:
                sql += """ r.type_id = %s"""
                if c < len(type): sql += """ OR"""
                values += [i]
                c += 1
            sql += """)"""
            
        if event:
            c = 1
            sql += """ AND ("""
            for i in event:
                sql += """ r.event_id = %s"""
                if c < len(event): sql += """ OR"""
                values += [i]
                c += 1
            sql += """)"""
        
        if purok and purok > 0:
            sql += """ AND (r.purok = %s)"""
            values += [purok]
        
        sql += """ ORDER BY r.id DESC;"""
        df = db.querydatafromdatabase(sql, values, cols)

        results = dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3(
                            [
                                html.I(className = 'bi bi-search me-2'),
                                html.Br(),
                                "Waray report para sini nga barangay, purok, klase san report, o panhitabó.",
                                html.Br(),
                                html.Small("(There's no report for this barangay, purok, report type, or event.)")
                            ],
                            className = 'mb-0 text-center text-muted'
                        ),
                    ]
                )
            ],
            #class_name = MarginSettings.row
        ),

        if df.shape[0]:
            for i in df.index:
                # Names as hyperlinks
                row = html.A(
                    df['Report type'][i],
                    href = '/reports/report?id=%s' % df['No.'][i]
                )

                df.at[i, 'Report type'] = html.Span(row, style = {'color' : '#ff5757'}) if df.at[i, 'Status'] == 1 else row

            results = dbc.Table.from_dataframe(
                df[['No.', 'Event', 'Report type', 'Barangay', 'Purok']],
                striped = False,
                bordered = False,
                hover = True,
                size = 'sm'
            )

        return [results]
    else: raise PreventUpdate

# Callback for generating reports graph
@app.callback(
    [
        Output('rep_vie_gra_reportsfiled', 'figure'),
        Output('rep_vie_div_chart', 'className')
    ],
    [
        Input('url', 'pathname'),
        Input('rep_vie_input_brgy_id', 'value')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
    ]
)

def rep_vie_generatereportsgraph(pathname, brgy, region, province, citymun):
    fig = None
    class_name = MarginSettings.footer + ' d-block'
    conditions = [
        pathname == '/reports',
        pathname == '/reports/view'
    ]
    if any(conditions):
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

        if brgy:
            sql += " AND r.brgy_id = %s"
            values += [brgy]

        sql += ");"
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape[0]:
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
            class_name = 'd-none'
    return [fig, class_name]