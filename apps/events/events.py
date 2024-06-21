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
from utilities.utils import MarginSettings, CardStyle, ReturnLinkCallback, DropdownDataLoader

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
                                    class_name = MarginSettings().row,
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
                                    class_name = MarginSettings().row
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
                                                class_name = MarginSettings().label
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
                                    class_name = MarginSettings().row
                                ),
                            ],
                            id = 'eve_vie_div_header',
                            className = MarginSettings().header
                        ),
                        html.Div(
                            id = 'eve_vie_div_results',
                            className = MarginSettings().div,
                            style = {
                                'max-width' : '100%',
                                'overflow' : 'scroll'
                            }
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
                                                        html.Span(
                                                            "Balik sa home",
                                                            id = 'eve_vie_spa_returnlink_war'
                                                        ),
                                                        html.Small(
                                                            " (Return to home)",
                                                            id = 'eve_vie_sma_returnlink_en',
                                                            className = 'text-muted'
                                                        )
                                                    ],
                                                    id = 'eve_vie_hta_returnlink',
                                                    href = '/'
                                                )
                                            ],
                                            class_name = 'col-auto'
                                        )
                                    ],
                                    class_name = MarginSettings().row + ' justify-content-end'
                                )
                            ],
                            id = 'eve_vie_div_footer',
                            className = MarginSettings().footer
                        )
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        ),
    ]
)

# Common callback for changing return link depending
# on user login status
return_link_callback_instance = ReturnLinkCallback(app, 'eve_vie')

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
        ddl = DropdownDataLoader(db)

        # Event types
        types = ddl.load_event_types()
        dropdowns.append(types)

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
        # Retrieve events as dataframe
        sql = """SELECT
        e.id AS id,
        e.name AS name,
        CONCAT(et.symbol, ' ', et.label_war, ' (', et.label_en, ')') AS eventtype,
        TO_CHAR(e.startdate, 'Month dd, yyyy') AS startdate,
        TO_CHAR(e.enddate, 'Month dd, yyyy') AS enddate,
        e.is_active
        FROM events.event AS e
        LEFT JOIN utilities.eventtype AS et ON e.type_id = et.id
        """
        values = []
        cols = ['ID No.', 'Name', 'Event type', 'Start date', 'End date', 'Active?']

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

        df = df[['Name', 'Event type', 'Start date', 'End date', 'Active?']]

        table = dbc.Table.from_dataframe(
            df,
            striped = False,
            bordered = False,
            hover = True,
            size = 'sm'
        )

        return [table]
    else: raise PreventUpdate