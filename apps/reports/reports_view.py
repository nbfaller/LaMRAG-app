# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import hashlib
from datetime import datetime, timedelta
# App definition
from app import app
from apps import dbconnect as db

tag_required = html.Sup("*", className = 'text-danger')

hyperlink_style = {
    'text-decoration' : 'none',
    'color' : 'inherit'
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
                                            "View reports",
                                            id = 'rep_vie_h1_header'
                                        ),
                                    ],
                                    class_name = row_m,
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Barangay", tag_required, #html.Br(),
                                                    #html.Small(" (Event)", className = 'text-muted')
                                                ],
                                                id = 'rep_vie_label_brgy_id',
                                                class_name = label_m
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
                                                #    class_name = ftext_m
                                                #),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-10'
                                        )
                                    ],
                                    id = 'rep_vie_row_brgy_id',
                                    class_name = row_m,
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Search", tag_required, #html.Br(),
                                                    #html.Small(" (Event)", className = 'text-muted')
                                                ],
                                                id = 'rep_vie_label_brgy_id',
                                                class_name = label_m
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-2'
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                id = 'rep_vie_input_search',
                                                type = 'text',
                                                placeholder = "Search by name or event type."
                                                #value = 1
                                               ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-9 col-lg-10'
                                        ),
                                    ], className = 'mb-1 mb-md-0',
                                    id = 'rep_vie_row_search',
                                    class_name = row_m
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
                                                class_name = label_m
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
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-6 col-lg-7'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'rep_vie_input_event_id',
                                                multi = True,
                                                #type = 'text',
                                                placeholder = "Event"
                                                #value = 1
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-3'
                                        ),
                                    ], className = 'mb-1 mb-md-0',
                                    id = 'rep_vie_row_filter',
                                    class_name = row_m
                                ),
                            ],
                            id = 'rep_vie_div_header',
                            className = header_m
                        ),
                        html.Div(
                            id = 'rep_vie_div_results',
                            className = div_m,
                            style = {
                                'max-width' : '100%',
                                'overflow' : 'scroll'
                            }
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
        Output('rep_vie_input_reporttype_id', 'options'),
        Output('rep_vie_input_event_id', 'options')
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
        
        # Barangays
        sql = """SELECT name AS label, id AS value
        FROM utilities.addressbrgy
        WHERE region_id = %s AND province_id = %s AND citymun_id = %s;
        """
        values = [region, province, citymun]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        brgys = df.to_dict('records')
        dropdowns.append(brgys)
        dropdowns.append(brgy)
        
        # Report types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.reporttype;
        """
        values = []
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        reporttypes = df.to_dict('records')
        dropdowns.append(reporttypes)
        
        # Events
        sql = """SELECT e.name AS label, e.id AS value
        FROM events.event AS e
        LEFT JOIN events.eventbrgy AS eb ON e.id = eb.event_id
        WHERE eb.region_id = %s AND eb.province_id = %s AND eb.citymun_id = %s
        AND eb.brgy_id = %s;
        """
        values = [region, province, citymun, brgy]
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        events = df.to_dict('records')
        dropdowns.append(events)

        return dropdowns
    else: raise PreventUpdate

# Callback for searching reports
@app.callback(
    [
        Output('rep_vie_div_results', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('rep_vie_input_search', 'value'),
        Input('rep_vie_input_reporttype_id', 'value'),
        Input('rep_vie_input_event_id', 'value'),
    ]
)

def rep_vie_loadsearchresults(pathname, search, type, eventtype):
    conditions = [
        pathname == '/reports',
        pathname == '/reports/view'
    ]
    if any(conditions):
        # Retrieve users as dataframe
        sql = """SELECT
        r.id AS report_id,
        rv.id AS version_id,
        CONCAT(rt.label_war, ' (', rt.label_en, ')') as reporttype_id,
        r.purok,
        rv.occurrence_date,
        rv.occurrence_time,
        CONCAT(u.lname, ', ', COALESCE(u.livedname, u.fname), ' ', LEFT(u.mname, 1)) AS creator_name,
        TO_CHAR(rv.create_time, 'Month dd, yyyy • HH:MI:SS AM') AS create_time,
        CONCAT(rs.label_war, ' (', rs.label_en, ')') as reportstatus_id
        FROM reports.reportversion AS rv
        LEFT JOIN reports.report AS r ON rv.report_id = r.id
        LEFT JOIN users.user AS u ON rv.creator_id = u.id
        LEFT JOIN utilities.reporttype AS rt ON r.type_id = rt.id
        LEFT JOIN utilities.reportstatus AS rs ON rv.status_id = rs.id
        """
        values = []
        cols = ['Report ID', 'Version No.', 'Type', 'Purok', 'Occurrence date', 'Occurrence time', 'Creator', 'Creation time', 'Status']

        sql += """ ORDER BY rv.create_time DESC;"""
        df = db.querydatafromdatabase(sql, values, cols)

        #df = df[['Name', 'Event type', 'Start date', 'End date']]

        table = dbc.Table.from_dataframe(
            df,
            striped = False,
            bordered = False,
            hover = True,
            size = 'sm'
        )

        return [table]
    else: raise PreventUpdate