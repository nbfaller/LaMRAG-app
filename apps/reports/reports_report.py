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
        dcc.Store(id = 'rep_rep_report_id', storage_type = 'memory'),
        dcc.Store(id = 'rep_rep_reporttype_id', storage_type = 'memory'),
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
                                            "REPORT",
                                            #color = 'danger'
                                        ),
                                        width = 'auto'
                                    ),
                                    class_name = row_m,
                                ),
                                dbc.Row(
                                    [
                                        html.H1(
                                            "Report",
                                            id = 'rep_rep_h1_header'
                                        )
                                    ],
                                    class_name = row_m,
                                )
                            ],
                            id = 'rep_rep_div_header',
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
                                                        id = 'rep_rep_col_basicinfo',
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
                            id = 'rep_rep_div_basicinfo',
                            className = div_m
                        ),
                        #html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H4(
                                            [
                                                html.I(className = 'bi bi-file-earmark-diff-fill me-2'),
                                                "Mga bersiyon",
                                                #html.Br(),
                                                html.Small(" (Versions)", className = 'text-muted')
                                            ]
                                        ),
                                    ], class_name = row_m
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader(
                                                            dbc.Tabs(
                                                                id = 'rep_rep_crd_tbs_reportversions'
                                                            )
                                                        ),
                                                        dbc.CardBody(
                                                            [
                                                                "Alayon pag-pili san bersiyon nga imo karuyag basahon dida sa mga tab sa igbaw.",
                                                                html.Br(),
                                                                html.Small("Please select the version that you want to read among the tabs above.", className = 'text-muted')
                                                            ],
                                                            id = 'rep_rep_crd_bdy_reportversions',
                                                            class_name = 'card-text',
                                                            style = {
                                                                'max-width' : '100%',
                                                                'overflow' : 'scroll'
                                                            }
                                                        ),
                                                        dbc.CardFooter(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.Small(
                                                                                    [
                                                                                        "Submitted by ",
                                                                                        html.Span(id = 'rep_rep_spa_creator_name'),
                                                                                        " on ",
                                                                                        html.Span(id = 'rep_rep_spa_creation_datetime'),
                                                                                        html.Br(),
                                                                                        "Status: ",
                                                                                        dbc.Badge("Status", id = 'rep_rep_bdg_status_label', class_name = 'align-content-center align-text-top'),
                                                                                        " . Updated on ",
                                                                                        html.Span(id = 'rep_rep_spa_status_datetime'),
                                                                                    ],
                                                                                    className = 'align-self-center card-text text-muted'
                                                                                ),
                                                                            ],
                                                                            class_name = 'col-12 col-xl-auto my-2'
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            dbc.Button(
                                                                                                [
                                                                                                    html.I(className = 'bi bi-pencil-square me-2'),
                                                                                                    "Edit"
                                                                                                ],
                                                                                                id = 'rep_rep_btn_validate',
                                                                                                style = {'width': ' 100%'},
                                                                                                color = 'primary',
                                                                                                outline = True
                                                                                                #type = 'submit'
                                                                                            ),
                                                                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-6 col-xl-auto'
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            dbc.Button(
                                                                                                [
                                                                                                    html.I(className = 'bi bi-check-circle-fill me-2'),
                                                                                                    "Validate"
                                                                                                ],
                                                                                                id = 'rep_rep_btn_edit',
                                                                                                style = {'width': ' 100%'},
                                                                                                #type = 'submit'
                                                                                            ),
                                                                                            class_name = 'align-self-center mt-2 mt-md-0 col-12 col-md-6 col-xl-auto'
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ],
                                                                            class_name = 'align-self-center col-12 col-xl-auto my-2'
                                                                        ),
                                                                    ],
                                                                    class_name = 'justify-content-between'
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    style = card_style
                                                ),
                                                dbc.Tabs(
                                                    id = 'rep_rep_tbs_reportversions'
                                                ),
                                            ]
                                        ),
                                    ], class_name = row_m
                                ),
                            ],
                            id = 'rep_rep_div_data',
                            className = div_m
                        ),
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)

rep_rep_url_pathname = '/reports/report'

# Callback for displaying report details
@app.callback(
    [
        Output('rep_rep_h1_header', 'children'),
        Output('rep_rep_report_id', 'data'),
        Output('rep_rep_reporttype_id', 'data'),
        Output('rep_rep_col_basicinfo', 'children'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search'),
    ]
)

def rep_rep_setreport(pathname, search):
    if pathname == rep_rep_url_pathname:
        to_return = []
        parsed = urlparse(search)
        if parse_qs(parsed.query):
            report_id = parse_qs(parsed.query)['id'][0]
            if report_id:
                sql = """SELECT
                r.id,
                r.type_id,
                e.name AS event,
                CONCAT(et.symbol, ' ', et.label_war, ' (', et.label_en, ')') AS event_type,
                CONCAT(rt.symbol, ' ', rt.label_war, ' (', rt.label_en, ')') AS report_type,
                ab.name AS brgy_name,
                r.purok AS purok
                FROM reports.report AS r
                LEFT JOIN events.event AS e on r.event_id = e.id
                LEFT JOIN utilities.eventtype AS et ON e.type_id = et.id
                LEFT JOIN utilities.addressbrgy AS ab ON (r.region_id = ab.region_id AND r.province_id = ab.province_id AND r.citymun_id = ab.citymun_id AND r.brgy_id = ab.id)
                LEFT JOIN utilities.reporttype AS rt ON r.type_id = rt.id
                WHERE r.id = %s;
                """
                values = [report_id]
                cols = [
                    'No.',
                    'Type ID',
                    'Panhitabó (Event)',
                    'Klase san panhitabó (Event type)',
                    'Klase san report (Report type)',
                    'Barangay',
                    'Purok'
                ]
                df = db.querydatafromdatabase(sql, values, cols)

                # Header
                to_return.append(df['Klase san report (Report type)'][0])
                # Report ID
                to_return.append(df['No.'][0])
                # Report type
                to_return.append(df['Type ID'][0])

                # Basic information table
                table_df = df[['Panhitabó (Event)', 'Klase san panhitabó (Event type)', 'Barangay', 'Purok']].transpose()
                table_df.insert(
                    0,
                    "Information",
                    [
                        html.Span(
                            [
                                html.I(className = 'bi bi-journal-bookmark me-2'),
                                html.B("Panhitabó"),
                                html.Small(" (Event)", className = 'text-muted')
                            ]
                        ),
                        html.Span(
                            [
                                html.I(className = 'bi bi-tag me-2'),
                                html.B("Klase san panhitabó"),
                                html.Small(" (Event type)", className = 'text-muted')
                            ]
                        ),
                        html.Span(
                            [
                                html.I(className = 'bi bi-geo-alt me-2'),
                                html.B("Barangay"),
                                #html.Small(" (End date)", className = 'text-muted')
                            ]
                        ),
                        html.Span(
                            [
                                html.I(className = 'bi bi-houses me-2'),
                                html.B("Purok"),
                                #html.Small(" (Creator)", className = 'text-muted')
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

# Callback for generating tabs for report versions
@app.callback(
    [
        Output('rep_rep_crd_tbs_reportversions', 'children'),
        Output('rep_rep_crd_tbs_reportversions', 'active_tab'),
    ],
    [
        Input('rep_rep_report_id', 'data'),
    ],
    [
        State('rep_rep_reporttype_id', 'data'),
    ]
)

def rep_rep_populatereports(report_id, type):
    tabs = []
    if report_id:
        sql = """SELECT id
        FROM reports.reportversion
        WHERE report_id = %s;
        """
        values = [report_id]
        cols = ['ID']
        df = db.querydatafromdatabase(sql, values, cols)

        latest_version = 0

        while latest_version < len(df.index):
            tabs.append(
                dbc.Tab(
                    label = 'v. %s' % (latest_version + 1),
                    id = 'rep_rep_tbs_tab_%s' % (latest_version + 1)
                )
            )
            latest_version += 1
    else: raise PreventUpdate
    return [tabs, 'tab-%s' % (latest_version - 1)]

# Callback for populating page with report versions
@app.callback(
    [
        Output('rep_rep_crd_bdy_reportversions', 'children'),
        Output('rep_rep_spa_creator_name', 'children'),
        Output('rep_rep_spa_creation_datetime', 'children'),
        Output('rep_rep_bdg_status_label', 'children'),
        Output('rep_rep_bdg_status_label', 'color'),
        Output('rep_rep_spa_status_datetime', 'children')
    ],
    [
        Input('rep_rep_crd_tbs_reportversions', 'active_tab'),
    ],
    [
        State('rep_rep_report_id', 'data'),
        State('rep_rep_reporttype_id', 'data'),
    ]
)

def rep_rep_populatereports(version, report_id, type):
    content = []
    creator_name = "-"
    creation_datetime = "-"
    status_label = "-"
    status_datetime = "-"
    status_color = None
    if version:
        version_id = int((str(version).split("-")[1])) + 1
        sql = """SELECT rv.id,
        TO_CHAR(rv.occurrence_date, 'Month dd, yyyy'),
        rv.occurrence_time::time,
        """
        values = [report_id, version_id]
        cols = [
            'No.',
            'Petsa san panhitabó (Date of occurrence)',
            'Oras san panhitabó (Time of ocurrence)',
        ]

        # Additional type-specific rows
        if type == 1:
            sql += """ CONCAT(rv_relinc_type.symbol, ' ', rv_relinc_type.label_war, ' (', rv_relinc_type.label_en, ')'),
            rv_relinc.qty,
            rv_relinc.description,
            rv_relinc.actions_taken,
            CONCAT(rv_relinc_status.label_war, ' (', rv_relinc_status.label_en, ')'),
            """
            cols += [
                'Klase san insidente (Type of incident)',
                'Kantidad san insidente (Quantity of incident)',
                'Deskripsiyon (Description)',
                'Mga ginhimo pagkatapos (Actions taken)',
                'Kamutangan san insidente (Status)',
            ]
        if type == 2:
            sql += """ rv_casualty.type_id,
            CONCAT(rv_casualty.lname, ', ', rv_casualty.fname, ' ', rv_casualty.mname),
            rv_casualty.age,
            rv_casualty.assignedsex_id,
            rv_casualty.region_id,
            rv_casualty.province_id,
            rv_casualty.citymun_id,
            rv_casualty.brgy_id,
            rv_casualty.street,
            rv_casualty.cause,
            rv_casualty.infosource,
            rv_casualty.status_id,
            """
            cols += [
                'Klase san disgrasiya (Casualty type)',
                'Ngaran san nadisgrasiya',
                'Edad (Age)',
                'Natawo nga babayi/lalaki (Sex assigned at birth)',
                'Rehiyon nga gin-iistaran (Region of residence)',
                'Probinsya nga gin-iistaran (Probinsya of residence)',
                'Siyudad/bungto nga gin-iistaran (City/municipality of residence)',
                'Barangay nga gin-iistaran (Barangay of residence)',
                'Kalsada nga gin-iistaran (Street address)',
                'Rason san pagkadisgrasiya (Cause of casualty)',
                'Ginkuhaan san impormasyon (Source of information)',
                'Kamutangan san pagprubar (Validation status)',
            ]
        
        # Other common version information (auxiliary)
        sql += """ rv.remarks,
        CONCAT(rs.label_war, ' (', rs.label_en, ')') AS status,
        TO_CHAR(rv.status_time, 'Month dd, yyyy at HH:MI:SS AM'),
        rs.color,
        CONCAT(u.lname, ', ', COALESCE(u.livedname, u.fname), ' ', LEFT(u.mname, 1), ' (', u.username, ')') AS creator,
        TO_CHAR(rv.create_time, 'Month dd, yyyy at HH:MI:SS AM')
        FROM reports.reportversion AS rv
        LEFT JOIN users.user AS u ON rv.creator_id = u.id
        LEFT JOIN utilities.reportstatus AS rs ON rv.status_id = rs.id
        """
        cols += [
            'Iba pa nga komento (remarks)',
            'Kamutangan san report (Report status)',
            'Oras san pagbag-o san kamutangan (Time of report status)',
            'Status color',
            'Nag-report (Reported by)',
            'Oras san pagreport (Report time)',
        ]

        # Type-specific left join
        if type == 1:
            sql += """ LEFT JOIN reports.relinc AS rv_relinc ON (
                    rv.report_id = rv_relinc.report_id AND
                    rv.id = rv_relinc.version_id)
                LEFT JOIN utilities.relinctype AS rv_relinc_type ON (
                    rv_relinc.type_id = rv_relinc_type.id)
                LEFT JOIN utilities.relincstatus AS rv_relinc_status ON (
                    rv_relinc.status_id = rv_relinc_status.id AND
                    rv_relinc.type_id = rv_relinc_status.relinctype_id)
            """
        if type == 2:
            sql += """ LEFT JOIN reports.casualty AS rv_casualty ON (
                rv.report_id = rv_casualty.report_id AND
                rv.id = rv_casualty.version_id)
            """
        
        sql += """ WHERE rv.report_id = %s AND rv.id = %s;"""
        df = db.querydatafromdatabase(sql, values, cols)

        # Set report creator name
        creator_name = df['Nag-report (Reported by)'][0]
        creation_datetime = df['Oras san pagreport (Report time)'][0]
        status_label = df['Kamutangan san report (Report status)'][0]
        status_datetime = df['Oras san pagbag-o san kamutangan (Time of report status)'][0]
        status_color = df['Status color'][0]

        # Remove last two columns
        df = df.iloc[:, :-5]
        cols = cols[:-5]

        label_rows = []
        for i in cols[1:]:
            secondary_label = None
            if len(i.split(' (')) > 1: secondary_label = html.Small([" (", str(i.split(' (')[1])[:-1], ")"], className = 'text-muted')
            label_rows += [
                html.Span(
                    [
                        html.B(i.split(' (')[0]),
                        secondary_label
                    ]
                )
            ]

        # Table
        version_df = df[df['No.'] == version_id].transpose()
        version_df = version_df.iloc[1:]
        #print(version_df.to_string())

        version_df.insert(
            0,
            "Information",
            label_rows,
            True
        )
        version_df = version_df.rename(columns={'Information' : '', 0 : ''})
        table = dbc.Table.from_dataframe(
            version_df,
            striped = False,
            bordered = False,
            hover = False,
            size = 'sm',
            borderless = True,
            style = {'margin' : '0px'}
        )

        content.append(table)
    else: raise PreventUpdate
    return [content, creator_name, creation_datetime, status_label, status_color, status_datetime]