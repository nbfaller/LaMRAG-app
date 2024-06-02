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
from datetime import datetime
import pytz
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
        dcc.Store(id = 'eve_eve_sto_eventid', data = -1, storage_type = 'memory'),
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
                                                ], class_name = row_m
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Button(
                                                            [
                                                                html.I(className = 'bi bi-toggle-off me-2'),
                                                                "Deactivate this event"
                                                            ],
                                                            id = 'eve_eve_btn_activate',
                                                            style = {'width': ' 100%'},
                                                            color = 'primary',
                                                            #outline = True,
                                                            external_link = True
                                                            #type = 'submit'
                                                        ),
                                                        class_name = 'd-inline align-self-center mb-2 mb-md-0 col-12 col-md-6 col-xl-auto'
                                                    ),
                                                ],
                                                class_name = 'justify-content-end'
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
                                    ],
                                    class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    id = 'eve_eve_div_sumreports'
                                                ),
                                            ]
                                        )
                                    ], class_name = row_m
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
                                                "Mga consolidated report",
                                                #html.Br(),
                                                html.Small(" (Generated consolidated reports)", className = 'text-muted')
                                            ]
                                        ),
                                    ], class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    id = 'eve_eve_div_consreports'
                                                ),
                                            ]
                                        )
                                    ], class_name = row_m
                                ),
                            ],
                            className = div_m
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
                                                        "Balik sa mga panhitabó",
                                                        html.Small(" (Return to events)", className = 'text-muted')
                                                    ],
                                                    href = '/events'
                                                )
                                            ],
                                            class_name = 'col-auto'
                                        )
                                    ],
                                    class_name = row_m + ' justify-content-end'
                                )
                            ],
                            id = 'eve_eve_div_footer',
                            className = footer_m
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
        Output('eve_eve_sto_eventid', 'data'),
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
                to_return.append(event_id)
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

                df.loc[0, 'Kamutangan (Status)'] = 'Active' if df.loc[0, 'Kamutangan (Status)'] == 'true' else 'Deactivated'

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
                sql = """SELECT rv.occurrence_date,
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
                cols = ['Occurrence date', 'Report type']
                df = db.querydatafromdatabase(sql, values, cols)
                #print(df)
                #df['Occurrence date'] = pd.to_datetime(df['Validation time'])
                df = df.groupby([df['Occurrence date'], 'Report type']).size().unstack(fill_value = 0).cumsum().reset_index()
                df.columns.name = None
                #print(df)

                traces = []
                for event in df.columns[1:]:
                    traces.append(
                        go.Scatter(
                            x = df['Occurrence date'],
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

# Callback for generating consolidated reports
@app.callback(
    [
        Output('eve_eve_div_consreports', 'children')
    ],
    [
        Input('eve_eve_sto_eventid', 'modified_timestamp')
    ],
    [
        State('eve_eve_sto_eventid', 'data'),
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
    ],
    prevent_initial_call = True
)

def eve_eve_generateconsreports(
    modified_timestamp, event_id,
    region, province, citymun
):
    accordion = []
    sql = """SELECT id, CONCAT(symbol, ' ', label_war, ' (', label_en, ')'), table_nm
        FROM utilities.reporttype
        ORDER BY id ASC;"""
    values = []
    cols = ['id', 'label', 'table']
    types = db.querydatafromdatabase(sql, values, cols)
    
    for type_id in range(1, len(types) + 1):
        sql = """WITH latest_version AS (
                SELECT DISTINCT ON (r.id)
                    r.id AS report_id,
                    ab.name AS brgy,
                    rv.id AS version_id,
                    r.purok AS purok,
                    rv.remarks AS remarks
                FROM reports.report AS r
                INNER JOIN reports.reportversion AS rv
                    ON r.id = rv.report_id
                INNER JOIN utilities.addressbrgy AS ab
                    ON (r.region_id = ab.region_id AND r.province_id = ab.province_id AND r.citymun_id = ab.citymun_id AND r.brgy_id = ab.id)
                WHERE r.event_id = %s AND r.type_id = %s
                ORDER BY r.id, rv.id DESC)
            SELECT /*lv.report_id AS id,
                lv.version_id AS version,*/
                lv.brgy AS brgy,
                lv.purok AS purok,
                lv.remarks AS remarks
            """
        values = [int(event_id), int(type_id)]
        cols = [
            #'ID',
            #'Version',
            'Barangay',
            'Purok',
            'Remarks']
        sql_join = ""
        #print(i)
        # Report type 1: Related incident
        if type_id == 1:
            #continue
            sql += """,
                CONCAT(rv_relinc_type.symbol, ' ', rv_relinc_type.label_war, ' (', rv_relinc_type.label_en, ')') AS relinc_type,
                rv_relinc.qty AS relinc_qty,
                rv_relinc.description AS relinc_desc,
                rv_relinc.actions_taken AS relinc_actions,
                CONCAT(rv_relinc_status.label_war, ' (', rv_relinc_status.label_en, ')') AS relinc_status
                """
            cols += [
                'Type',
                'Quantity',
                'Description',
                'Actions taken',
                'Status'
            ]
            sql_join = """ INNER JOIN reports.relinc AS rv_relinc
                    ON (lv.report_id = rv_relinc.report_id
                    AND lv.version_id = rv_relinc.version_id)
                INNER JOIN utilities.relinctype AS rv_relinc_type
                    ON rv_relinc.type_id = rv_relinc_type.id
                INNER JOIN utilities.relincstatus AS rv_relinc_status
                    ON (rv_relinc.status_id = rv_relinc_status.id AND rv_relinc.type_id = rv_relinc_status.relinctype_id);"""
        # Report type 2: Casualty
        elif type_id == 2:
            #continue
            sql += """,
                CONCAT(rv_casualty_type.symbol, ' ', rv_casualty_type.label_war, ' (', rv_casualty_type.label_en, ')') AS casualty_type,
                CONCAT(rv_casualty.lname, ', ', rv_casualty.fname, ' ', rv_casualty.mname) AS casualty_name,
                rv_casualty.age AS casualty_age,
                CONCAT(rv_casualty_assignedsex.symbol, ' ', rv_casualty_assignedsex.label_war, ' (', rv_casualty_assignedsex.label_en, ')') AS casualty_assignedsex,
                rv_casualty.cause AS casualty_cause,
                rv_casualty.infosource AS casualty_infosource,
                CONCAT(rv_casualty_status.label_war, ' (', rv_casualty_status.label_en, ')') AS casualty_status
                """
            cols += [
                'Type',
                'Name',
                'Age',
                'Assigned sex at birth',
                'Cause',
                'Source of information',
                'Status'
            ]
            sql_join = """ INNER JOIN reports.casualty AS rv_casualty
                    ON (lv.report_id = rv_casualty.report_id
                    AND lv.version_id = rv_casualty.version_id)
                INNER JOIN utilities.casualtytype AS rv_casualty_type
                    ON rv_casualty.type_id = rv_casualty_type.id
                INNER JOIN utilities.assignedsex AS rv_casualty_assignedsex
                    ON rv_casualty.assignedsex_id = rv_casualty_assignedsex.id
                INNER JOIN utilities.casualtystatus AS rv_casualty_status
                    ON rv_casualty.status_id = rv_casualty_status.id;"""
        # Report type 3: Public utility status
        elif type_id == 3:
            #continue
            sql += """,
                rv_pubutilint_pubutil.name AS pubutilint_pubutil,
                CONCAT(rv_pubutilint_pubutiltype.symbol, ' ', rv_pubutilint_pubutiltype.label_war, ' (', rv_pubutilint_pubutiltype.label_en, ')') AS pubutilint_pubutiltype,
                CONCAT(rv_pubutilint_pubutilinttype.symbol, ' ', rv_pubutilint_pubutilinttype.label_war, ' (', rv_pubutilint_pubutilinttype.label_en, ')') AS pubutilint_type,
                rv_pubutilint.int_date AS pubutilint_intdate,
                rv_pubutilint.int_time AS pubutilint_inttime,
                rv_pubutilint.res_date AS pubutilint_resdate,
                rv_pubutilint.res_time AS pubutilint_restime
                """
            cols += [
                'Public utility',
                'Utility type',
                'Interruption type',
                'Interruption date',
                'Interruption time',
                'Restoration date',
                'Restoration time'
            ]
            sql_join = """ INNER JOIN reports.pubutilint AS rv_pubutilint
                    ON (lv.report_id = rv_pubutilint.report_id
                    AND lv.version_id = rv_pubutilint.version_id)
                INNER JOIN utilities.pubutil AS rv_pubutilint_pubutil
                    ON rv_pubutilint.pubutil_id = rv_pubutilint_pubutil.id
                INNER JOIN utilities.pubutiltype AS rv_pubutilint_pubutiltype
                    ON rv_pubutilint_pubutil.type_id = rv_pubutilint_pubutiltype.id
                INNER JOIN utilities.pubutilinttype AS rv_pubutilint_pubutilinttype
                    ON rv_pubutilint.inttype_id = rv_pubutilint_pubutilinttype.id;"""
        # Report type 4: Damaged house
        elif type_id == 4:
            #continue
            sql += """,
                CONCAT(rv_dmgdhouse_type.symbol, ' ', rv_dmgdhouse_type.label_war, ' (', rv_dmgdhouse_type.label_en, ')') AS dmgdhouse_type,
                CONCAT(rv_dmgdhouse.lname, ', ', rv_dmgdhouse.fname, ' ', rv_dmgdhouse.mname) AS dmgdhouse_name,
                rv_dmgdhouse.age AS dmgdhouse_age,
                CONCAT(rv_dmgdhouse_assignedsex.symbol, ' ', rv_dmgdhouse_assignedsex.label_war, ' (', rv_dmgdhouse_assignedsex.label_en, ')') AS dmgdhouse_assignedsex,
                rv_dmgdhouse.loc_text AS dmgdhouse_loctext,
                rv_dmgdhouse.loc_gps AS dmgdhouse_locgps
                """
            cols += [
                'Damage type',
                'Name of homeowner',
                'Age',
                'Assigned sex at birth',
                'Location',
                'GPS coordinates'
            ]
            sql_join = """ INNER JOIN reports.dmgdhouse AS rv_dmgdhouse
                    ON (lv.report_id = rv_dmgdhouse.report_id
                    AND lv.version_id = rv_dmgdhouse.version_id)
                INNER JOIN utilities.dmgdinfratype AS rv_dmgdhouse_type
                    ON rv_dmgdhouse.type_id = rv_dmgdhouse_type.id
                INNER JOIN utilities.assignedsex AS rv_dmgdhouse_assignedsex
                    ON rv_dmgdhouse.assignedsex_id = rv_dmgdhouse_assignedsex.id;"""
        # Report type 5: Public infrastructure status
        elif type_id == 5:
            #continue
            sql += """,
                CONCAT(rv_dmgdinfra_type.symbol, ' ', rv_dmgdinfra_type.label_war, ' (', rv_dmgdinfra_type.label_en, ')') AS dmgdinfra_type,
                CONCAT(rv_dmgdinfra_class.label_war, ' (', rv_dmgdinfra_class.label_en, ')') AS dmgdinfra_class,
                rv_dmgdinfra.infraname AS dmgdinfra_name,
                CONCAT(rv_dmgdinfra.qty, ' ', rv_dmgdinfra_qtyunit.label_war, ' (', rv_dmgdinfra_qtyunit.label_en, ')') AS dmgdinfra_qty,
                CONCAT(rv_dmgdinfra_dmgtype.symbol, ' ', rv_dmgdinfra_dmgtype.label_war, ' (', rv_dmgdinfra_dmgtype.label_en, ')') AS dmgdinfra_dmgtype,
                rv_dmgdinfra.loc_text AS dmgdinfra_loctext,
                rv_dmgdinfra.loc_gps AS dmgdinfra_locgps,
                CONCAT('₱', rv_dmgdinfra.infracost) AS dmgdinfra_infracost
                """
            cols += [
                'Type',
                'Class',
                'Name/description',
                'Quantity',
                'Damage type',
                'Location',
                'GPS coordinates',
                'Cost'
            ]
            sql_join = """ INNER JOIN reports.dmgdinfra AS rv_dmgdinfra
                    ON (lv.report_id = rv_dmgdinfra.report_id
                    AND lv.version_id = rv_dmgdinfra.version_id)
                INNER JOIN utilities.infratype AS rv_dmgdinfra_type
                    ON rv_dmgdinfra.infratype_id = rv_dmgdinfra_type.id
                INNER JOIN utilities.infraclass AS rv_dmgdinfra_class
                    ON rv_dmgdinfra.infraclass_id = rv_dmgdinfra_class.id
                INNER JOIN utilities.qtyunit AS rv_dmgdinfra_qtyunit
                    ON rv_dmgdinfra.qtyunit_id = rv_dmgdinfra_qtyunit.id
                INNER JOIN utilities.dmgdinfratype AS rv_dmgdinfra_dmgtype
                    ON rv_dmgdinfra.dmgtype_id = rv_dmgdinfra_dmgtype.id;"""
        
        sql += """ FROM latest_version lv %s""" % sql_join
        
        #values = [int(event_id), int(type_id)]
        #print(sql, values, cols)
        table_df = db.querydatafromdatabase(sql, values, cols)

        table = None
        if table_df.shape[0]:
            table = dbc.Table.from_dataframe(
                table_df,
                striped = False,
                bordered = False,
                hover = True,
                size = 'sm',
            )
        else:
            table = html.H3(
                [
                    html.I(className = 'bi bi-search me-2'),
                    html.Br(),
                    "Waray report sini nga klase an ginhimo.",
                    html.Br(),
                    html.Small("(No reports of this type were made.)")
                ],
                className = 'mb-0 text-center text-muted'
            ),

        accordion.append(
            dbc.AccordionItem(
                html.Div(
                    table,
                    style = {
                        'max-width' : '100%',
                        'overflow' : 'scroll'
                    }
                ),
                title = types['label'][type_id - 1],
            )
        )
    
    content = [
        dbc.Accordion( 
            accordion,
            start_collapsed = True,
            class_name = 'mb-1'
        ),
        html.Small(
            [
                """Ungod ug sakto ini nga consolidated report yana nga %s.
                Diri api sini nga mga ihap an mga report nga puprubaran pa.""" % (datetime.now(pytz.timezone('Asia/Manila')).strftime("%Y-%m-%d, %H:%M:%S")),
                html.Small(
                    [
                        """ (This consolidated report is true and correct as of %s.
                        Unverified reports are not included in these tallies.)"""  % (datetime.now(pytz.timezone('Asia/Manila')).strftime("%Y-%m-%d at %H:%M:%S"))
                    ]
                )
            ],
            className = 'text-muted'
        )
    ]

    return [content]

# Callback for generating consolidated reports
@app.callback(
    [
        Output('eve_eve_div_sumreports', 'children')
    ],
    [
        Input('eve_eve_sto_eventid', 'modified_timestamp')
    ],
    [
        State('eve_eve_sto_eventid', 'data'),
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
    ],
    prevent_initial_call = True
)

def eve_eve_generatesumreports(
    modified_timestamp, event_id,
    region, province, citymun
):
    content = []
    accordion = []
    sql = """SELECT id, CONCAT(symbol, ' ', label_war, ' (', label_en, ')'), table_nm
        FROM utilities.reporttype
        ORDER BY id ASC;"""
    values = []
    cols = ['id', 'label', 'table']
    types = db.querydatafromdatabase(sql, values, cols)
    
    for type_id in range(1, len(types) + 1):
        sql = """
            WITH latest_version AS (
                SELECT DISTINCT ON (r.id)
                    r.id AS report_id,
                    rv.id AS version_id,
                    ab.name AS brgy,
                    r.purok AS purok,
                    rv.remarks AS remarks
                FROM reports.report AS r
                INNER JOIN reports.reportversion AS rv
                    ON r.id = rv.report_id
                LEFT JOIN utilities.addressbrgy AS ab
                    ON (r.region_id = ab.region_id AND r.province_id = ab.province_id AND r.citymun_id = ab.citymun_id AND r.brgy_id = ab.id)
                WHERE r.event_id = %s AND r.type_id = %s
                ORDER BY r.id, rv.id DESC
            )
            SELECT /*lv.report_id AS id,
                lv.version_id AS version,*/
                lv.brgy AS brgy
        """
        values = [int(event_id), int(type_id)]
        cols = ['Barangay']
        sql_join = ""
        
        # Report type 1: Related incident
        if type_id == 1:
            sql2 = """SELECT id, CONCAT(symbol, ' ',  label_en) FROM utilities.relinctype
                ORDER BY id ASC;"""
            values2 = []
            cols2 = ['id', 'label']
            df2 = db.querydatafromdatabase(sql2, values2, cols2)

            for i in range(0, len(df2)):
                sql += """,
                    COUNT (CASE WHEN rv_relinc.type_id = %s THEN 1 END) AS 
                    """
                #if i < len(df2): sql += ""","""
                sql += "col_" + str(df2['id'][i])
                values += [int(df2['id'][i])]
                cols += [df2['label'][i]]

            sql_join = """ INNER JOIN reports.relinc AS rv_relinc
                    ON (lv.report_id = rv_relinc.report_id
                    AND lv.version_id = rv_relinc.version_id)"""
        # Report type 2: Casualty
        elif type_id == 2:
            sql2 = """SELECT ucs.id, ucs.label_en, uct.id, uct.label_en
            FROM utilities.casualtytype AS uct
            CROSS JOIN utilities.casualtystatus AS ucs
            ORDER BY ucs.id, uct.id;"""
            values2 = []
            cols2 = ['status_id', 'status', 'type_id', 'type']
            df2 = db.querydatafromdatabase(sql2, values2, cols2)

            for i in range(0, len(df2)):
                sql += """,
                    COUNT (CASE WHEN rv_casualty.status_id = %s AND rv_casualty.type_id = %s THEN 1 END) AS 
                    """
                #if i < len(df2): sql += ""","""
                sql += "col_" + str(df2['status_id'][i]) + "_" + str(df2['type_id'][i])
                values += [int(df2['status_id'][i]), int(df2['type_id'][i])]
                cols += [df2['status'][i] + ' - ' + df2['type'][i]]

            sql_join = """ INNER JOIN reports.casualty AS rv_casualty
                    ON (lv.report_id = rv_casualty.report_id
                    AND lv.version_id = rv_casualty.version_id)"""
        # Report type 3: Public utility status
        elif type_id == 3:
            sql2 = """SELECT pit.id, pit.label_en, put.id, put.symbol, put.label_en
                FROM utilities.pubutiltype AS put
            CROSS JOIN utilities.pubutilinttype AS pit
            ORDER BY put.id, pit.id;"""
            values2 = []
            cols2 = ['int_id', 'status', 'type_id', 'symbol', 'type']
            df2 = db.querydatafromdatabase(sql2, values2, cols2)

            for i in range(0, len(df2)):
                if df2['int_id'][i] == 1:
                    sql += """, COUNT (CASE WHEN (rv_pubutilint.inttype_id = %s"""
                    values += [int(df2['int_id'][i])]
                elif df2['int_id'][i] == 2:
                    sql += """ OR rv_pubutilint.inttype_id = %s"""
                    values += [int(df2['int_id'][i])]
                elif df2['int_id'][i] == 3:
                    sql += """ OR rv_pubutilint.inttype_id = %s) AND rv_pubutilint_pubutil.type_id = %s THEN 1 END) AS """
                    sql += "col_123" + "_" + str(df2['type_id'][i])
                    values += [int(df2['int_id'][i]), int(df2['type_id'][i])]
                    cols += [df2['symbol'][i] + "❌ Interruption" + ' - ' + df2['type'][i]]
                else:
                    sql += """,
                        COUNT (CASE WHEN rv_pubutilint.inttype_id = %s AND rv_pubutilint_pubutil.type_id = %s THEN 1 END) AS 
                        """
                    sql += "col_4" + "_" + str(df2['type_id'][i])
                    values += [int(df2['int_id'][i]), int(df2['type_id'][i])]
                    cols += [df2['symbol'][i] + "✅ Restored" + ' - ' + df2['type'][i]]

                
                #if i < len(df2): sql += ""","""

            sql_join = """ INNER JOIN reports.pubutilint AS rv_pubutilint
                    ON (lv.report_id = rv_pubutilint.report_id
                    AND lv.version_id = rv_pubutilint.version_id)
                INNER JOIN utilities.pubutil AS rv_pubutilint_pubutil
                    ON rv_pubutilint.pubutil_id = rv_pubutilint_pubutil.id"""
        # Report type 4: Damaged house
        elif type_id == 4:
            sql2 = """SELECT id, symbol, label_en
                FROM utilities.dmgdinfratype AS put
                ORDER BY id;"""
            values2 = []
            cols2 = ['id', 'symbol', 'label']
            df2 = db.querydatafromdatabase(sql2, values2, cols2)

            for i in range(0, len(df2)):
                sql += """,
                    COUNT (CASE WHEN rv_dmgdhouse.type_id = %s THEN 1 END) AS 
                    """
                
                #if i < len(df2): sql += ""","""
                sql += "col_" + str(df2['id'][i])
                values += [int(df2['id'][i])]
                cols += [df2['symbol'][i] + ' ' + df2['label'][i]]
            
            sql += """,
                COUNT (CASE WHEN rv_dmgdhouse.type_id = 1 OR rv_dmgdhouse.type_id = 2 THEN 1 END) AS col_3
                """
            cols += ["🏘️ Total"]

            sql_join = """ INNER JOIN reports.dmgdhouse AS rv_dmgdhouse
                    ON (lv.report_id = rv_dmgdhouse.report_id
                    AND lv.version_id = rv_dmgdhouse.version_id)"""
        elif type_id == 5:
            sql += """,
                COUNT (rv_dmgdinfra.version_id) AS qty,
                SUM (rv_dmgdinfra.infracost) AS cost
                """
            #values += [int(df2['status_id'][i]), int(df2['type_id'][i])]
            cols += ['🔢 Number of damaged infrastructure', '💸 Cost of damage (₱)']

            sql_join = """ INNER JOIN reports.dmgdinfra AS rv_dmgdinfra
                    ON (lv.report_id = rv_dmgdinfra.report_id
                    AND lv.version_id = rv_dmgdinfra.version_id)"""
            
        sql += """ FROM latest_version AS lv %s
            GROUP BY lv.brgy ORDER BY lv.brgy;
        """ % sql_join
        table_df = db.querydatafromdatabase(sql, values, cols)

        table = None
        if table_df.shape[0]:
            table = dbc.Table.from_dataframe(
                table_df,
                striped = False,
                bordered = False,
                hover = True,
                size = 'sm',
            )
        else:
            table = html.H3(
                [
                    html.I(className = 'bi bi-search me-2'),
                    html.Br(),
                    "Waray report sini nga klase an ginhimo.",
                    html.Br(),
                    html.Small("(No reports of this type were made.)")
                ],
                className = 'mb-0 text-center text-muted'
            ),

        accordion.append(
            dbc.AccordionItem(
                html.Div(
                    table,
                    style = {
                        'max-width' : '100%',
                        'overflow' : 'scroll'
                    }
                ),
                title = types['label'][type_id - 1],
            )
        )
    
    content = [
        dbc.Accordion( 
            accordion,
            start_collapsed = True,
            class_name = 'mb-1'
        ),
        html.Small(
            [
                """Ungod ug sakto ini nga consolidated report yana nga %s.
                Diri api sini nga mga ihap an mga report nga puprubaran pa.""" % (datetime.now(pytz.timezone('Asia/Manila')).strftime("%Y-%m-%d, %H:%M:%S")),
                html.Small(
                    [
                        """ (This consolidated report is true and correct as of %s.
                        Unverified reports are not included in these tallies.)"""  % (datetime.now(pytz.timezone('Asia/Manila')).strftime("%Y-%m-%d at %H:%M:%S"))
                    ]
                )
            ],
            className = 'text-muted'
        )
    ]
    
    return [content]