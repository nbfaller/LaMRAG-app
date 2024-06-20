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
import hashlib
from datetime import datetime
import pytz
# App definition
from app import app
from apps import dbconnect as db
from utilities.utils import MarginSettings, CardStyle

layout = html.Div(
    [
        dcc.Store(id = 'rep_rep_sto_report_id', storage_type = 'memory'),
        dcc.Store(id = 'rep_rep_sto_reportversion_id', storage_type = 'memory'),
        dcc.Store(id = 'rep_rep_sto_reporttype_id', storage_type = 'memory'),
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
                                            [
                                                "REPORT SERIAL NO. ",
                                                html.Span("-", id = 'rep_rep_span_reportid')
                                            ]
                                            #color = 'danger'
                                        ),
                                        width = 'auto'
                                    ),
                                    class_name = MarginSettings().row,
                                ),
                                dbc.Row(
                                    [
                                        html.H1(
                                            "Report",
                                            id = 'rep_rep_h1_header'
                                        )
                                    ],
                                    class_name = MarginSettings().row,
                                )
                            ],
                            id = 'rep_rep_div_header',
                            className = MarginSettings().header
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
                                                ], class_name = MarginSettings().row
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
                                                ], #class_name = MarginSettings().row
                                            )
                                        #]
                                    #),
                                    #style = CardStyle.get_style()
                                #)
                            ],
                            id = 'rep_rep_div_basicinfo',
                            className = MarginSettings().div
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
                                    ], class_name = MarginSettings().row
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader(
                                                            dbc.Tabs(
                                                                id = 'rep_rep_crd_tbs_reportversions',
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
                                                                                        "Status: ",
                                                                                        dbc.Badge("Status", id = 'rep_rep_bdg_status_label', class_name = 'align-content-center align-text-top'),
                                                                                        html.Br(),
                                                                                        "Created by ",
                                                                                        html.Span("-", id = 'rep_rep_spa_creator_name'),
                                                                                        " on ",
                                                                                        html.Span("-", id = 'rep_rep_spa_creation_datetime'),
                                                                                        html.Br(),
                                                                                        html.Div(
                                                                                            [
                                                                                                "Validated by ", html.Span("-", id = 'rep_rep_spa_status_updater'),
                                                                                                " on ",
                                                                                                html.Span("-", id = 'rep_rep_spa_status_datetime')
                                                                                            ],
                                                                                            id = 'rep_rep_div_validation',
                                                                                            className = 'd-none'
                                                                                        ),
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
                                                                                                    "Edit/update"
                                                                                                ],
                                                                                                id = 'rep_rep_btn_edit',
                                                                                                style = {'width': ' 100%'},
                                                                                                color = 'primary',
                                                                                                outline = True,
                                                                                                external_link = True
                                                                                                #type = 'submit'
                                                                                            ),
                                                                                            class_name = 'd-inline align-self-center mb-2 mb-md-0 col-12 col-md-6 col-xl-auto'
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            dbc.Button(
                                                                                                [
                                                                                                    html.I(className = 'bi bi-check-circle-fill me-2'),
                                                                                                    "Validate"
                                                                                                ],
                                                                                                id = 'rep_rep_btn_validate',
                                                                                                style = {'width': ' 100%'},
                                                                                                #type = 'submit'
                                                                                            ),
                                                                                            class_name = 'd-inline align-self-center mt-2 mt-md-0 col-12 col-md-6 col-xl-auto',
                                                                                            id = 'rep_rep_col_validate'
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
                                                    style = CardStyle.get_style()
                                                ),
                                                dbc.Tabs(
                                                    id = 'rep_rep_tbs_reportversions'
                                                ),
                                            ]
                                        ),
                                    ], class_name = MarginSettings().row
                                ),
                            ],
                            id = 'rep_rep_div_data',
                            className = MarginSettings().div
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
                                                        "Balik sa mga report",
                                                        html.Small(" (Return to reports)", className = 'text-muted')
                                                    ],
                                                    href = '/reports'
                                                )
                                            ],
                                            class_name = 'col-auto'
                                        )
                                    ],
                                    class_name = MarginSettings().row + ' justify-content-end'
                                )
                            ],
                            id = 'rep_rep_div_footer',
                            className = MarginSettings().footer
                        )
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        ),
        dbc.Modal(
            [
                dbc.Form(
                    [
                        dbc.ModalBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4("Confirm report validation"),
                                                html.P(
                                                    [
                                                        """Alayon pagbutang san imo password para makumpirma an validation sini nga report.
                                                        Alayon liwat pagseguro nga sakto an ngatanan nga nakabutang nga impormasyon.""",
                                                        html.Br(),
                                                        html.Small(
                                                            """(Please enter your password to confirm the validation of this event.
                                                            Also, please ensure that all information submitted is correct.)
                                                            """,
                                                            className = 'text-muted'
                                                        )
                                                    ], className = MarginSettings().paragraph
                                                ),
                                            ]
                                        )
                                    ], class_name = 'mb-3'
                                ),
                                #html.Hr(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Alert(
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                html.I(className = 'bi bi-exclamation-circle-fill me-2'),
                                                                width = 'auto',
                                                                class_name = MarginSettings().alert_icon
                                                            ),
                                                            dbc.Col(
                                                                id = 'rep_rep_alert_passwordvalidation_col_text'
                                                            )
                                                        ]
                                                    ),
                                                    id = 'rep_rep_alert_passwordvalidation',
                                                    is_open = False,
                                                    color = 'warning',
                                                    class_name = MarginSettings().label,
                                                    dismissable = True,
                                                    #fade = True,
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type = 'password',
                                                    id = 'rep_rep_input_password',
                                                    placeholder = ['Enter password'],
                                                    invalid = False
                                                ),
                                            ]
                                        )
                                    ],
                                    id = 'rep_rep_row_password',
                                    class_name = MarginSettings().row + ' d-block'
                                ),
                            ],
                            id = 'rep_rep_modal_confirm_body'
                        ),
                        dbc.ModalFooter(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(className = 'bi bi-arrow-clockwise me-2'),
                                                    "Basaha utro an report (Review report)"
                                                ],
                                                id = 'rep_rep_btn_review',
                                                style = {'width': ' 100%'},
                                                external_link = True
                                            ),
                                            id = 'rep_rep_col_review',
                                            class_name = 'd-none align-self-center col-12 p-0'
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(className = 'bi bi-folder me-2'),
                                                    "Balik sa reports (Return to reports)"
                                                ],
                                                id = 'rep_rep_btn_return',
                                                style = {'width': ' 100%'},
                                                href = '/reports',
                                                external_link = True
                                            ),
                                            id = 'rep_rep_col_return',
                                            class_name = 'd-none align-self-center col-12 p-0'
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(className = 'bi bi-arrow-return-left me-2'),
                                                    "Balik sa dashboard (Return to dashboard)"
                                                ],
                                                id = 'rep_rep_btn_tohome',
                                                style = {'width': ' 100%'},
                                                href = '/dashboard',
                                                external_link = True
                                            ),
                                            id = 'rep_rep_col_tohome',
                                            class_name = 'd-none align-self-center col-12 p-0'
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(className = 'bi bi-check-circle-fill me-2'),
                                                    "I-kumpirma (Confirm)"
                                                ],
                                                id = 'rep_rep_btn_confirm',
                                                style = {'width': ' 100%'},
                                                type = 'submit'
                                            ),
                                            id = 'rep_rep_col_confirm',
                                            class_name = 'd-inline align-self-center col-12 col-md-auto'
                                        )
                                    ],
                                    class_name = 'justify-content-end'
                                )
                            ],
                            id = 'rep_rep_modal_confirm_footer'
                        )
                    ]
                )
            ],
            id = 'rep_rep_modal_confirm',
            is_open = False,
            centered = True,
            scrollable = True,
            backdrop = True,
            #size = 'lg',
        ),
    ]
)

rep_rep_url_pathname = '/reports/report'

# Callback for displaying report details
@app.callback(
    [
        Output('rep_rep_h1_header', 'children'),
        Output('rep_rep_btn_review', 'href'),
        Output('rep_rep_btn_edit', 'href'),
        Output('rep_rep_sto_report_id', 'data'),
        Output('rep_rep_span_reportid', 'children'),
        Output('rep_rep_sto_reporttype_id', 'data'),
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
                # Return button href
                review_href = '/reports/report?id=%s' % df['No.'][0]
                to_return.append(review_href)
                # Edit button href
                edit_href = '/reports/create?mode=update&id=%s' % df['No.'][0]
                to_return.append(edit_href)
                # Report ID
                to_return.append(df['No.'][0])
                # Report serial number
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
                    style = {'margin' : '0px'},
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
        Input('rep_rep_sto_report_id', 'data'),
    ],
    [
        State('rep_rep_sto_reporttype_id', 'data'),
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
                    label = 'R. No. %s-%s' % (report_id, latest_version + 1),
                    id = 'rep_rep_tbs_tab_%s' % (latest_version + 1),
                    active_label_style = {'font-weight' : '700'}
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
        Output('rep_rep_spa_status_updater', 'children'),
        Output('rep_rep_spa_status_datetime', 'children'),
        Output('rep_rep_col_validate', 'class_name'),
        Output('rep_rep_div_validation', 'className')
    ],
    [
        Input('rep_rep_crd_tbs_reportversions', 'active_tab'),
    ],
    [
        State('rep_rep_sto_report_id', 'data'),
        State('rep_rep_sto_reporttype_id', 'data'),
        State('app_currentuser_id', 'data'),
    ]
)

def rep_rep_populatereports(version, report_id, type, currentuser_id):
    content = []
    creator_name = "-"
    creation_datetime = "-"
    status_label = "-"
    status_datetime = "-"
    status_color = None
    status_updater = "-"
    validate_class_name = 'd-inline align-self-center mt-2 mt-md-0 col-12 col-md-6 col-xl-auto'
    validate_div_class = 'd-none'
    if version:
        version_id = int((str(version).split("-")[1])) + 1
        sql = """SELECT rv.id,
        TO_CHAR(rv.occurrence_date, 'Month dd, yyyy'),
        rv.occurrence_time::time AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Manila',
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
        elif type == 2:
            sql += """ CONCAT(rv_casualty_type.symbol, ' ', rv_casualty_type.label_war, ' (', rv_casualty_type.label_en, ')'),
            CONCAT(rv_casualty.lname, ', ', rv_casualty.fname, ' ', rv_casualty.mname),
            rv_casualty.age,
            CONCAT(rv_casualty_assignedsex.symbol, ' ', rv_casualty_assignedsex.label_war, ' (', rv_casualty_assignedsex.label_en, ')'),
            ar.name,
            ap.name,
            acm.name,
            ab.name,
            rv_casualty.street,
            rv_casualty.cause,
            rv_casualty.infosource,
            CONCAT(rv_casualty_status.label_war, ' (', rv_casualty_status.label_en, ')'),
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
        elif type == 3:
            sql += """ CONCAT(rv_pubutil_type.symbol, ' ', rv_pubutil_type.label_war, ' (', rv_pubutil_type.label_en, ')'),
            rv_pubutilint_pubutil.name,
            CONCAT(rv_pubutilint_type.symbol, ' ', rv_pubutilint_type.label_war, ' (', rv_pubutilint_type.label_en, ')'),
            TO_CHAR(rv_pubutilint.int_date, 'Month dd, yyyy'),
            rv_pubutilint.int_time::time AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Manila',
            TO_CHAR(rv_pubutilint.res_date, 'Month dd, yyyy'),
            rv_pubutilint.res_time::time AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Manila',
            """
            cols += [
                'Klase san utilidad, (Type of utility)',
                'Naghahatag san serbisyo (Service provider)',
                'Klase san pag-undang',
                'Petsa san pag-undang',
                'Oras san pag-undang',
                'Petsa san pagbalik',
                'Oras san pagbalik'
            ]
        elif type == 4:
            sql += """ CONCAT(rv_dmgdhouse_type.symbol, ' ', rv_dmgdhouse_type.label_war, ' (', rv_dmgdhouse_type.label_en, ')'),
            CONCAT(rv_dmgdhouse.lname, ', ', rv_dmgdhouse.fname, ' ', rv_dmgdhouse.mname),
            rv_dmgdhouse.age,
            CONCAT(rv_dmgdhouse_assignedsex.symbol, ' ', rv_dmgdhouse_assignedsex.label_war, ' (', rv_dmgdhouse_assignedsex.label_en, ')'),
            rv_dmgdhouse.loc_text,
            rv_dmgdhouse.loc_gps,
            """
            cols += [
                'Klase san pagkarubat (Type of damage)',
                'Ngaran san tag-iya (Name of homeowner)',
                'Edad (Age)',
                'Natawo nga babayi/lalaki (Sex assigned at birth)',
                'Lokasiyon san balay (Location of home)',
                'GPS coordinates'
            ]
        elif type == 5:
            sql += """ CONCAT(rv_infra_type.symbol, ' ', rv_infra_type.label_war, ' (', rv_infra_type.label_en, ')'),
            CONCAT(rv_infra_class.label_war, ' (', rv_infra_class.label_en, ')'),
            rv_dmgdinfra.infraname,
            rv_dmgdinfra.loc_text,
            rv_dmgdinfra.loc_gps,
            CONCAT(rv_dmgdinfra.qty, ' ', rv_dmgdinfra_qtyunit.label_war, ' (', rv_dmgdinfra_qtyunit.label_en, ')'),
            CONCAT('₱', ROUND(CAST(rv_dmgdinfra.infracost AS NUMERIC), 2)),
            CONCAT(rv_dmgdinfra_type.symbol, ' ', rv_dmgdinfra_type.label_war, ' (', rv_dmgdinfra_type.label_en, ')'),
            """
            cols += [
                'Tipo san imprastruktura (Infrastructure type)',
                'Klase (Classification)',
                'Ngaran/deskripsiyon (Name/description)',
                'Lokasiyon',
                'GPS coordinates',
                'Kadamo san narubat (Quantity of damage)',
                'Kantidad san narubat (Cost of damage)',
                'Kamutangan (Status)'
            ]
        
        # Other common version information (auxiliary)
        sql += """ rv.remarks,
        rs.id,
        CONCAT(us.lname, ', ', us.fname, ' ', LEFT(us.mname, 1), ' (', us.username, ')') AS status_updater,
        rv.status_updater_id,
        CONCAT(rs.label_war, ' (', rs.label_en, ')') AS status,
        TO_CHAR(rv.status_time::timestamp AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Manila', 'Month dd, yyyy at HH:MI:SS AM TZ'),
        rs.color,
        CONCAT(u.lname, ', ', COALESCE(u.livedname, u.fname), ' ', LEFT(u.mname, 1), ' (', u.username, ')') AS creator,
        TO_CHAR(rv.create_time::timestamp AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Manila', 'Month dd, yyyy at HH:MI:SS AM TZ')
        FROM reports.reportversion AS rv
        LEFT JOIN users.user AS u ON rv.creator_id = u.id
        LEFT JOIN users.user AS us ON rv.status_updater_id = us.id
        LEFT JOIN utilities.reportstatus AS rs ON rv.status_id = rs.id
        """
        cols += [
            'Iba pa nga komento (Remarks)',
            'status_id',
            'Nag-update (Updated by)',
            'status_updater_id',
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
        elif type == 2:
            sql += """ LEFT JOIN reports.casualty AS rv_casualty ON (
                    rv.report_id = rv_casualty.report_id AND
                    rv.id = rv_casualty.version_id)
                LEFT JOIN utilities.casualtytype AS rv_casualty_type ON (
                    rv_casualty.type_id = rv_casualty_type.id)
                LEFT JOIN utilities.casualtystatus AS rv_casualty_status ON (
                    rv_casualty.status_id = rv_casualty_status.id)
                LEFT JOIN utilities.assignedsex AS rv_casualty_assignedsex ON (
                    rv_casualty.assignedsex_id = rv_casualty_assignedsex.id)
                INNER JOIN utilities.addressregion AS ar ON (
                    rv_casualty.region_id = ar.id)
                INNER JOIN utilities.addressprovince AS ap ON (
                    rv_casualty.region_id = ap.region_id AND rv_casualty.province_id = ap.id)
                INNER JOIN utilities.addresscitymun AS acm ON (
                    rv_casualty.region_id = acm.region_id AND rv_casualty.province_id = acm.province_id AND rv_casualty.citymun_id = acm.id)
                INNER JOIN utilities.addressbrgy AS ab ON (
                    rv_casualty.region_id = ab.region_id AND rv_casualty.province_id = ab.province_id AND rv_casualty.citymun_id = ab.citymun_id AND rv_casualty.brgy_id = ab.id)
            """
        elif type == 3:
            sql += """ LEFT JOIN reports.pubutilint AS rv_pubutilint ON (
                    rv.report_id = rv_pubutilint.report_id AND
                    rv.id = rv_pubutilint.version_id)
                LEFT JOIN utilities.pubutil AS rv_pubutilint_pubutil ON (
                    rv_pubutilint.pubutil_id = rv_pubutilint_pubutil.id)
                LEFT JOIN utilities.pubutiltype AS rv_pubutil_type ON (
                    rv_pubutilint_pubutil.type_id = rv_pubutil_type.id)
                LEFT JOIN utilities.pubutilinttype AS rv_pubutilint_type ON (
                    rv_pubutilint.inttype_id = rv_pubutilint_type.id)
            """
        elif type == 4:
            sql += """ LEFT JOIN reports.dmgdhouse AS rv_dmgdhouse ON (
                    rv.report_id = rv_dmgdhouse.report_id AND
                    rv.id = rv_dmgdhouse.version_id)
                LEFT JOIN utilities.dmgdinfratype AS rv_dmgdhouse_type ON (
                    rv_dmgdhouse.type_id = rv_dmgdhouse_type.id)
                LEFT JOIN utilities.assignedsex AS rv_dmgdhouse_assignedsex ON (
                    rv_dmgdhouse.assignedsex_id = rv_dmgdhouse_assignedsex.id)
            """
        elif type == 5:
            sql += """ LEFT JOIN reports.dmgdinfra AS rv_dmgdinfra ON (
                    rv.report_id = rv_dmgdinfra.report_id AND
                    rv.id = rv_dmgdinfra.version_id)
                LEFT JOIN utilities.infratype AS rv_infra_type ON (
                    rv_dmgdinfra.infratype_id = rv_infra_type.id)
                LEFT JOIN utilities.infraclass AS rv_infra_class ON (
                    rv_dmgdinfra.infraclass_id = rv_infra_class.id)
                LEFT JOIN utilities.qtyunit AS rv_dmgdinfra_qtyunit ON (
                    rv_dmgdinfra.qtyunit_id = rv_dmgdinfra_qtyunit.id)
                LEFT JOIN utilities.dmgdinfratype AS rv_dmgdinfra_type ON (
                    rv_dmgdinfra.dmgtype_id = rv_dmgdinfra_type.id)
            """

        
        sql += """ WHERE rv.report_id = %s AND rv.id = %s;"""
        df = db.querydatafromdatabase(sql, values, cols)

        # Set report creator name
        creator_name = df['Nag-report (Reported by)'][0]
        creation_datetime = df['Oras san pagreport (Report time)'][0]
        status_label = df['Kamutangan san report (Report status)'][0]
        status_datetime = df['Oras san pagbag-o san kamutangan (Time of report status)'][0]
        status_color = df['Status color'][0]
        status_updater = df['Nag-update (Updated by)'][0]

        # Show validation button depending on report status
        status_id = df['status_id'][0]
        status_updater_id = df['status_updater_id'][0]
        if status_id == 2 or status_updater_id == currentuser_id:
            validate_class_name = 'd-none align-self-center mt-2 mt-md-0 col-12 col-md-6 col-xl-auto'
            validate_div_class = 'd-inline'

        # Remove last five columns
        df = df.iloc[:, :-8]
        cols = cols[:-8]

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
    return [content, creator_name, creation_datetime, status_label, status_color, status_updater, status_datetime, validate_class_name, validate_div_class]

# Callback for confirming report validation
@app.callback(
    [
        # Modal
        Output('rep_rep_modal_confirm', 'is_open'),
        # Report version
        Output('rep_rep_sto_reportversion_id', 'data')
    ],
    [
        Input('rep_rep_btn_validate', 'n_clicks')
    ],
    [
        State('rep_rep_crd_tbs_reportversions', 'active_tab'),
    ],
    prevent_initial_call = True
)

def rep_rep_confirmcreation(btn, reportversion):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'rep_rep_btn_validate' and btn:
            # Modal
            modal_open = True
            version = int(str(reportversion).split("-")[1]) + 1
            return [modal_open, version]
        else: raise PreventUpdate
    else: raise PreventUpdate

# Callback for validating report
@app.callback(
    [
        # In-modal alert
        Output('rep_rep_alert_passwordvalidation', 'is_open'),
        Output('rep_rep_alert_passwordvalidation', 'class_name'),
        Output('rep_rep_alert_passwordvalidation', 'color'),
        Output('rep_rep_alert_passwordvalidation_col_text', 'children'),
        # Input validation
        Output('rep_rep_input_password', 'invalid'),
        Output('rep_rep_input_password', 'valid'),
        # Button visibility
        Output('rep_rep_col_review', 'class_name'),
        Output('rep_rep_col_return', 'class_name'),
        Output('rep_rep_col_tohome', 'class_name'),
        Output('rep_rep_col_confirm', 'class_name'),
        # Modal dissmisability
        Output('rep_rep_modal_confirm', 'backdrop'),
        # Password field visibility
        Output('rep_rep_row_password', 'class_name')
    ],
    [
        Input('rep_rep_btn_confirm', 'n_clicks')
    ],
    [
        # User details
        State('app_currentuser_id', 'data'),
        State('rep_rep_input_password', 'value'),
        # Report details
        State('rep_rep_sto_report_id', 'data'),
        State('rep_rep_sto_reportversion_id', 'data')
    ],
    prevent_initial_call = True
)

def rep_rep_submitcreation(
    btn, user_id, password,
    report_id, version_id
):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'rep_rep_btn_confirm' and btn:
            # Alert
            alert_open = False
            alert_class_name = None
            alert_color = None
            alert_col_text = None
            # Password validation
            password_invalid = False
            password_valid = False
            # Button visibility
            vis_none = 'd-none'
            #vis_inline = 'd-inline'
            vis_block = 'd-block'
            common_class = ' align-self-center col-12 p-0'
            class_review = vis_none + common_class
            class_return = vis_none + common_class
            class_tohome = vis_none + common_class
            class_confirm = vis_block + common_class + ' col-md-auto'
            # Modal dissmisability
            modal_backdrop = True
            # Password visibility
            class_password = MarginSettings().row + ' ' + vis_block
            if not(password):
                alert_open = True
                alert_class_name = 'mb-3'
                alert_color = 'warning'
                password_invalid = True
                alert_col_text = [
                    "Alayon pagbutang san imo password.",
                    html.Br(),
                    html.Small(
                        "(Please enter your password.)",
                        className = 'text-muted'
                    ),
                ]
            else:
                sql = """SELECT username FROM users.user
                WHERE id = %s AND password = %s;"""
                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
                values = [user_id, encrypt_string(password)]
                cols = ['username']
                df = db.querydatafromdatabase(sql, values, cols)
                if df.shape[0]:
                    # Actual report validation
                    sql = """UPDATE reports.reportversion
                    SET status_id = 2,
                        status_time = %s,
                        status_updater_id = %s
                    WHERE report_id = %s
                        AND id = %s;
                    """
                    values = [
                        datetime.now(pytz.timezone('Asia/Manila')),
                        user_id,
                        report_id,
                        version_id
                    ]
                    db.modifydatabase(sql, values)
                    
                    # Open alert
                    alert_open = True
                    alert_class_name = 'mb-3'
                    alert_color = 'success'
                    # Change validity
                    password_valid = True
                    # Button visibility
                    class_review = vis_block + common_class + ' mb-2'
                    class_return = vis_block + common_class + ' mb-2 mt-2'
                    class_tohome = vis_block + common_class + ' mt-2'
                    class_confirm = vis_none + common_class
                    # Modal dissmisability
                    modal_backdrop = 'static'
                    # Password visibility
                    class_password = MarginSettings().row + ' ' + vis_none

                    alert_col_text = [
                        "Na-validate na an report.",
                        html.Br(),
                        html.Small(
                            "(Report validated.)",
                            className = 'text-muted'
                        ),
                    ]
                else:
                    alert_open = True
                    alert_class_name = 'mb-3'
                    alert_color = 'warning'
                    password_invalid = True
                    alert_col_text = [
                        "Diri sakto an nabutang nga password.",
                        html.Br(),
                        html.Small(
                            "(Incorrect password.)",
                            className = 'text-muted'
                        ),
                    ]
            return [
                alert_open, alert_class_name, alert_color, alert_col_text,
                password_invalid, password_valid,
                class_review, class_return, class_tohome, class_confirm,
                modal_backdrop,
                class_password
            ]
        else: raise PreventUpdate
    else: raise PreventUpdate