# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# Sandbox imports
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
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
        dcc.Store(id = 'sandbox_event_id', data = 1),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = 'sandbox_graph_1',
                                            animate = True,
                                            #style = {'max-height' : '15em'}
                                        )
                                    ]
                                )
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = 'sandbox_graph_2',
                                            animate = True,
                                            #style = {'max-height' : '15em'}
                                        )
                                    ]
                                )
                            ],
                        ),
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)

sandbox_url = '/sandbox'

@app.callback(
    [
        Output('sandbox_graph_1', 'figure'),
        Output('sandbox_graph_2', 'figure')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('sandbox_event_id', 'data'),
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data')
    ]
)

def sandbox_generatehistogram(pathname, data, region, province, citymun, brgy):
    fig = None
    if pathname == sandbox_url:
        sql = """SELECT rv.create_time,
        e.name AS event
        FROM reports.reportversion AS rv
        LEFT JOIN reports.report AS r ON rv.report_id = r.id
        LEFT JOIN events.event AS e ON r.event_id = e.id
        WHERE e.is_active
        AND (r.region_id = %s AND r.province_id = %s
        AND r.citymun_id = %s AND r.brgy_id = %s);
        """
        values = [region, province, citymun, brgy]
        cols = ['Creation time', 'Event']
        df = db.querydatafromdatabase(sql, values, cols)
        #print(df)
        df['Creation time'] = pd.to_datetime(df['Creation time'])
        df = df.groupby([df['Creation time'], 'Event']).size().unstack(fill_value = 0).cumsum().reset_index()
        df.columns.name = None
        #print(df)

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
            title = 'Cumulative reports filed over time',
            xaxis = {
                'title': 'Petsa (Date)'
            },
            yaxis = {
                'title': 'Mga ginhimo nga report (Reports filed)'
            },
            font_family = "DM Sans",
            showlegend = True,
            template = 'plotly_white',
        )

        fig1 = {'data': traces, 'layout': layout}

        sql = """SELECT al.login_time
        FROM logs.accesslog AS al;
        """
        values = []
        cols = ['Login time']
        df = db.querydatafromdatabase(sql, values, cols)
        #print(df)
        df['Login time'] = pd.to_datetime(df['Login time'])
        #df = df.groupby([df['Creation time'].dt.date, 'Event']).size().unstack(fill_value=0).cumsum().reset_index()
        df.columns.name = None
        #print(df)

        traces = []
        traces.append(
            go.Scatter(
                x = df['Login time'],
                #y = df[event],
                mode = 'lines',
                #name = 'Cumulative log-ins',
                #stackgroup ='one'  # This parameter makes it a stacked area chart
            )
        )

        layout = go.Layout(
            {
                'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                'paper_bgcolor' : 'rgba(0, 0, 0, 0)'
            },
            title = 'Cumulative user logins',
            xaxis = {
                'title': 'Petsa (Date)'
            },
            yaxis = {
                'title': 'Log-ins'
            },
            font_family = "DM Sans",
            showlegend = False,
            template = 'plotly_white',
        )

        fig2 = {'data': traces, 'layout': layout}
        return [fig1, fig2]
    else: raise PreventUpdate