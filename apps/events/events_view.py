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
                                            "View events",
                                            id = 'eve_vie_h1_header'
                                        ),
                                    ],
                                    class_name = row_m,
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Input(
                                                id = 'eve_vie_input_search',
                                                type = 'text',
                                                placeholder = "Search by name or event type."
                                                #value = 1
                                               ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12'
                                        ),
                                    ], className = 'mb-1 mb-md-0',
                                    id = 'eve_vie_row_search',
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
                                                id = 'eve_vie_label_filter',
                                                class_name = label_m
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-3 col-lg-2'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'eve_vie_input_isactive',
                                                multi = True,
                                                #type = 'text',
                                                placeholder = "Status",
                                                options = [
                                                    {'label' : 'Active', 'value' : True},
                                                    {'label' : 'Inactive', 'value' : False}
                                                ],
                                                value = [True]
                                                #value = 1
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-4 col-lg-3'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'eve_vie_input_eventtype_id',
                                                multi = True,
                                                #type = 'text',
                                                placeholder = "Event type"
                                                #value = 1
                                            ),
                                            class_name = 'align-self-center mb-2 mb-md-0 col-12 col-md-5 col-lg-7'
                                        ),
                                    ], className = 'mb-1 mb-md-0',
                                    id = 'eve_vie_row_filter',
                                    class_name = row_m
                                ),
                            ],
                            id = 'eve_vie_div_header',
                            className = header_m
                        ),
                        html.Div(
                            id = 'eve_vie_div_results',
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

# Callback for populating dropdowns and checklists
@app.callback(
    [
        Output('eve_vie_input_eventtype_id', 'options'),
    ],
    [
        Input('url', 'pathname')
    ]
)

def eve_vie_populatedropdowns(pathname):
    eve_vie_url_pathname = [
        pathname == '/events',
        pathname == '/events/view'
    ]
    if any(eve_vie_url_pathname):
        dropdowns = []

        # Event types
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.eventtype;
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        eventtypes = df.to_dict('records')
        dropdowns.append(eventtypes)

        return dropdowns
    else: raise PreventUpdate

# Callback for searching events
@app.callback(
    [
        Output('eve_vie_div_results', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('eve_vie_input_search', 'value'),
        Input('eve_vie_input_eventtype_id', 'value'),
        Input('eve_vie_input_isactive', 'value'),
    ]
)

def eve_vie_loadsearchresults(pathname, search, type, isactive):
    eve_vie_url_pathname = [
        pathname == '/events',
        pathname == '/events/view'
    ]
    if any(eve_vie_url_pathname):
        # Retrieve users as dataframe
        sql = """SELECT
        e.id AS id,
        e.name AS name,
        CONCAT(et.symbol, ' ', et.label_war, ' (', et.label_en, ')') AS eventtype,
        TO_CHAR(e.startdate, 'Month dd, yyyy') AS startdate,
        TO_CHAR(e.enddate, 'Month dd, yyyy') AS enddate
        FROM events.event AS e
        LEFT JOIN utilities.eventtype AS et ON e.type_id = et.id
        """
        values = []
        cols = ['ID No.', 'Name', 'Event type', 'Start date', 'End date']

        if isactive:
            #print(isactive)
            c = 1
            sql += """ WHERE ("""
            for i in isactive:
                sql += """ e.is_active = %s"""
                if c < len(isactive): sql += """ OR"""
                values += [i]
                c += 1
            sql += """)"""

        if search:
            sql += """ AND e.name ILIKE %s"""
            values += [f"%{search}%"]
        
        if type:
            c = 1
            sql += """ AND ("""
            for i in type:
                sql += """ e.type_id = %s"""
                if c < len(type): sql += """ OR"""
                values += [i]
                c += 1
            sql += """)"""

        sql += """ ORDER BY e.startdate ASC;"""
        df = db.querydatafromdatabase(sql, values, cols)

        for i in df.index:
            # Names as hyperlinks
            df.loc[i, 'Name'] = html.A(
                df['Name'][i],
                href = '/events/event?id=%s' % df['ID No.'][i],
            )

        df = df[['Name', 'Event type', 'Start date', 'End date']]

        table = dbc.Table.from_dataframe(
            df,
            striped = False,
            bordered = False,
            hover = True,
            size = 'sm'
        )

        return [table]
    else: raise PreventUpdate