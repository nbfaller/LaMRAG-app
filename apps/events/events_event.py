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
                                        dbc.Col(
                                            [
                                                dbc.Accordion(
                                                    id = 'eve_eve_acc_reports'
                                                ),
                                                html.Small(
                                                    [
                                                        """Ungod ug sakto ini nga consolidated report yana nga """,
                                                        html.Span(id = 'eve_eve_spa_reporttimestamp_war'),
                                                        """. Diri api sini nga mga ihap an mga report nga puprubaran pa.""",
                                                        html.Small(
                                                            [
                                                                """ (This consolidated report is true and correct as of """,
                                                                html.Span(id = 'eve_eve_spa_reporttimestamp_en'),
                                                                """. Unverified reports are not included in these tallies.)"""
                                                            ]
                                                        )
                                                    ],
                                                    className = 'text-muted'
                                                )
                                            ]
                                        )
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
        Output('eve_eve_acc_reports', 'children')
    ],
    [
        Input('eve_eve_sto_eventid', 'modified_timestamp')
    ],
    [
        State('eve_eve_sto_eventid', 'data')
    ],
    prevent_initial_call = True
)

def eve_eve_generatereports(modified_timestamp, event_id):
    accordion = []
    sql = """SELECT id, CONCAT(symbol, ' ', label_war, ' (', label_en, ')'), table_nm
        FROM utilities.reporttype
        ORDER BY id ASC;"""
    values = []
    cols = ['id', 'label', 'table']
    types = db.querydatafromdatabase(sql, values, cols)
    
    for type_id in range(1, len(types) + 1):
        sql = """SELECT
        r.id AS report_id,
        rv.id AS version_id,
        r.purok AS purok,
        rv.remarks AS remarks"""
        values = []
        cols = ['ID', 'Version', 'Purok', 'Remarks']
        sql_join = ""
        #print(i)
        # Report type 1: Related incident
        if type_id == 1:
            #continue
            sql += """,
                rv_relinc.type_id AS relinc_type,
                rv_relinc.qty AS reinc_qty,
                rv_relinc.description AS relinc_desc,
                rv_relinc.actions_taken AS relinc_actionstaken
                """
            cols += [
                'Related incident type',
                'Quantity',
                'Description',
                'Actions taken'
            ]
            sql_join = """ INNER JOIN reports.relinc AS rv_relinc
                ON (rv.report_id = rv_relinc.report_id
                AND rv.id = rv_relinc.version_id)"""
        # Report type 2: Casualty
        elif type_id == 2:
            #continue
            sql += """,
                rv_casualty.type_id AS casualty_type,
                CONCAT(rv_casualty.lname, ', ', rv_casualty.fname, ' ', rv_casualty.mname),
                rv_casualty.age AS casualty_age,
                rv_casualty.assignedsex_id AS casualty_assignedsex,
                rv_casualty.region_id AS casualty_region,
                rv_casualty.province_id AS casualty_province,
                rv_casualty.citymun_id AS casualty_citymun,
                rv_casualty.brgy_id AS casualty_brgy,
                rv_casualty.street AS casualty_street,
                rv_casualty.cause AS casualty_cause,
                rv_casualty.infosource AS casualty_infosource,
                rv_casualty.status_id AS casualty_status
                """
            cols += [
                'Casualty type',
                'Name',
                'Age',
                'Assigned sex at birth',
                'Region',
                'Province',
                'City/municipality',
                'Barangay',
                'Street address',
                'Cause',
                'Source of information',
                'Status'
            ]
            sql_join = """ INNER JOIN reports.casualty AS rv_casualty
                ON (rv.report_id = rv_casualty.report_id
                AND rv.id = rv_casualty.version_id)"""
        # Report type 3: Public utility status
        elif type_id == 3:
            #continue
            sql += """,
                rv_pubutilint.pubutil_id AS pubutilint_pubutil,
                rv_pubutilint.inttype_id AS pubutilint_type,
                rv_pubutilint.int_date AS pubutilint_intdate,
                rv_pubutilint.int_time AS pubutilint_inttime,
                rv_pubutilint.res_date AS pubutilint_resdate,
                rv_pubutilint.res_time AS pubutilint_restime
                """
            cols += [
                'Public utility',
                'Interruption type',
                'Interruption date',
                'Interruption time',
                'Restoration date',
                'Restoration time'
            ]
            sql_join = """ INNER JOIN reports.pubutilint AS rv_pubutilint
                ON (rv.report_id = rv_pubutilint.report_id
                AND rv.id = rv_pubutilint.version_id)"""
        # Report type 4: Damaged house
        elif type_id == 4:
            #continue
            sql += """,
                rv_dmgdhouse.type_id AS dmgdhouse_type,
                CONCAT(rv_dmgdhouse.lname, ', ', rv_dmgdhouse.fname, ' ', rv_dmgdhouse.mname) AS dmgdhouse_owner,
                rv_dmgdhouse.age AS dmgdhouse_age,
                rv_dmgdhouse.assignedsex_id AS dmgdhouse_assignedsex,
                rv_dmgdhouse.loc_text AS dmgdhouse_loctext,
                rv_dmgdhouse.loc_gps AS dmgdhouse_locgps
                """
            cols += [
                'Damage type',
                'Homeowner name',
                'Age',
                'Assigned sex at birth',
                'Location',
                'GPS coordinates',
            ]
            sql_join = """ INNER JOIN reports.dmgdhouse AS rv_dmgdhouse
                ON (rv.report_id = rv_dmgdhouse.report_id
                AND rv.id = rv_dmgdhouse.version_id)"""
        # Report type 5: Public infrastructure status
        elif type_id == 5:
            #continue
            sql += """,
                rv_dmgdinfra.infratype_id AS dmgdinfra_type,
                rv_dmgdinfra.infraclass_id AS dmgdinfra_class,
                rv_dmgdinfra.infraname AS dmgdinfra_name,
                rv_dmgdinfra.qty AS dmgdinfra_qty,
                rv_dmgdinfra.qtyunit_id AS dmgdinfra_qtyunit,
                rv_dmgdinfra.dmgtype_id AS dmgdinfra_dmgtype,
                rv_dmgdinfra.loc_text AS dmgdinfra_loctext,
                rv_dmgdinfra.loc_gps AS dmgdinfra_locgps,
                rv_dmgdinfra.infracost AS dmgdinfra_cost
                """
            cols += [
                'Infrastructure type',
                'Infrastructure class',
                'Name/description',
                'Quantity',
                'Units',
                'Damage type',
                'Location',
                'GPS coordinates',
                'Cost',
            ]
            sql_join = """ INNER JOIN reports.dmgdinfra AS rv_dmgdinfra
                ON (rv.report_id = rv_dmgdinfra.report_id
                AND rv.id = rv_dmgdinfra.version_id)"""
        
        sql += """ FROM reports.report AS r
            INNER JOIN reports.reportversion AS rv
            ON rv.id = (
                SELECT id
                FROM reports.reportversion AS rv
                WHERE r.id = rv.report_id
                ORDER BY id DESC LIMIT 1
            )"""
        sql += sql_join
        sql += """ WHERE r.event_id = %s AND r.type_id = %s;"""
        
        values = [int(event_id), int(type_id)]
        #print(sql, values, cols)
        table_df = db.querydatafromdatabase(sql, values, cols)
        table = dbc.Table.from_dataframe(
            table_df,
            striped = False,
            bordered = False,
            hover = True,
            size = 'sm',
        )

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

    return [accordion]