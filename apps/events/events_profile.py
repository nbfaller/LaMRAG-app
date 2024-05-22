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
                                    ],
                                    #class_name = row_m,
                                )
                            ],
                            id = 'eve_pro_div_header',
                            #className = div_m
                        ),
                        # Basic information
                        html.Div(
                            [
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
                                    ], class_name = row_m
                                ),
                            ],
                            id = 'eve_pro_div_basicinfo',
                            #className = div_m
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
        Output('eve_pro_col_basicinfo', 'children')
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
                e.startdate, e.enddate,
                e.description,
                u.username AS creator,
                e.create_time,
                e.is_active AS status,
                e.is_active_time AS status_time
                FROM events.event AS e
                LEFT JOIN utilities.eventtype AS et ON e.type_id = et.id
                LEFT JOIN users.user AS u ON e.creator_id = u.id
                WHERE e.id = %s;
                """
                values = [event_id]
                cols = [
                    'Name', 'Type', 'Start date', 'End date',
                    'Description', 'Creator', 'Creation time',
                    'Status', 'Status time'
                ]
                df = db.querydatafromdatabase(sql, values, cols)
                print(df)

                # Header
                to_return.append(df['Name'][0])

                # Basic information table
                table_df = df[['Type', 'Start date', 'End date', 'Description', 'Creator', 'Creation time', 'Status', 'Status time']].transpose()
                table_df.insert(0, "Information", [html.B('Type'), html.B('Start date'), html.B('End date'), html.B('Description'), html.B('Creator'), html.B('Creation time'), html.B('Status'), html.B('Status time')], True)
                table_df = table_df.rename(columns={'Information' : '', 0 : ''})
                table = dbc.Table.from_dataframe(
                    table_df,
                    striped = False,
                    bordered = False,
                    hover = False,
                    size = 'sm'
                )
                to_return.append(table)
            else: raise PreventUpdate
        else: raise PreventUpdate
        return to_return
    else: raise PreventUpdate