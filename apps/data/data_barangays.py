# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
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
                                            "BARANGAYS",
                                            #color = 'danger'
                                        ),
                                        width = 'auto'
                                    )
                                ),
                                dbc.Row(
                                    [
                                        html.H1(
                                            "View barangays",
                                            id = 'dat_bar_h1_header'
                                        ),
                                    ],
                                    class_name = row_m,
                                )
                            ],
                            id = 'dat_bar_div_header',
                            className = header_m
                        ),
                        # Cards
                        html.Div(
                            [
                                #html.Hr(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.H4(
                                                                                    [
                                                                                        html.I(className = 'bi bi-people-fill me-2'),
                                                                                        "Populasyon",
                                                                                        #html.Br(),
                                                                                        html.Small(" (Population)", className = 'text-muted')
                                                                                    ]
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ], class_name = row_m
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                dcc.Graph(
                                                                                    id = 'dat_bar_gra_brgypop',
                                                                                    animate = True,
                                                                                    #style = {'max-height' : '15em'}
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ], class_name = row_m
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.Li(
                                                                                    [
                                                                                        html.B(id = 'dat_bar_spa_currentpop'),
                                                                                        " ka-tawo an naukoy dinhi yana sumala san datos san Philippine Statistics Authority."
                                                                                    ]
                                                                                ),
                                                                                html.Li(
                                                                                    [
                                                                                        html.B(id = 'dat_bar_spa_pctchange'),
                                                                                        " kada tuig an pagdako san populasyon dinhi base sa historical data."
                                                                                    ]
                                                                                ),
                                                                                html.Li(
                                                                                    [
                                                                                        "Posible umabot sa ",
                                                                                        html.B(id = 'dat_bar_spa_possibpop'),
                                                                                        " ka-tawo an populasyon dinhi pag-abot san sunod nga tuig."
                                                                                    ]
                                                                                )
                                                                            ]
                                                                        )
                                                                    ], class_name = row_m
                                                                ),
                                                            ]
                                                        )
                                                    ],
                                                    id = 'dat_bar_car_popgraph',
                                                    style = card_style
                                                )
                                            ],
                                            class_name = 'align-self-center mb-3 mb-lg-0 col-12 col-lg-7'
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.H4(
                                                                                    [
                                                                                        html.I(className = 'bi bi-map-fill me-2'),
                                                                                        "Mapa",
                                                                                        #html.Br(),
                                                                                        html.Small(" (Map)", className = 'text-muted')
                                                                                    ]
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ], class_name = row_m
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.Iframe(
                                                                                    src = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6865.002317456614!2d124.58614405!3d12.20445395!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3309e1307fe06507%3A0xc9cd798f17ae0427!2sJose%20A.%20Rono%2C%20Calbayog%20City%2C%20Samar!5e1!3m2!1sen!2sph!4v1714120167172!5m2!1sen!2sph',
                                                                                    #src = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d562.5407776071039!2d124.61192079862425!3d12.06236092006715!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3309db8c252d21d1%3A0xaf1f98f12b16d98f!2sCalbayogCdrrmo!5e1!3m2!1sen!2sph!4v1709188668855!5m2!1sen!2sph',
                                                                                    width = '100%',
                                                                                    height = '200em',
                                                                                    style = {'border' : '0'},
                                                                                    #allowfullscreen ="",
                                                                                    loading_state = 'lazy',
                                                                                    referrerPolicy = 'no-referrer-when-downgrade'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ], class_name = row_m
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    id = 'dat_bar_car_spotmap',
                                                    style = card_style
                                                )
                                            ],
                                            class_name = 'align-self-center mb-3 mb-lg-0 col-12 col-lg-5'
                                        )
                                    ],
                                    class_name = row_m
                                )
                            ],
                            id = 'dat_bar_div_cards',
                            className = div_m
                        )
                    ],
                    class_name = 'col-lg-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)

# Callback for showing barangay-specific information
@app.callback(
    [
        Output('dat_bar_h1_header', 'children'),
        Output('dat_bar_gra_brgypop', 'figure'),
        Output('dat_bar_spa_currentpop', 'children'),
        Output('dat_bar_spa_pctchange', 'children'),
        Output('dat_bar_spa_possibpop', 'children')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data'),
        State('app_census_cols', 'data')
    ]
)

def dat_bar_setbrgyinfo(pathname, region, province, citymun, brgy, census_cols):
    if pathname == '/data/barangays':
        if region and province and citymun and brgy:
            header = None

            # Header
            sql = """SELECT name, pop_2000, pop_2007,
                pop_2010, pop_2015, pop_2020 FROM utilities.addressbrgy
                WHERE region_id = %s AND province_id = %s AND citymun_id = %s AND id = %s;"""
            values = [region, province, citymun, brgy]
            cols = census_cols
            df = db.querydatafromdatabase(sql, values, cols)
            header = df['name'][0]

            # Graph
            df = df.set_index('name').T
            fig = px.scatter(
                df,
                x = df.index,
                y = df.columns,
                #markers = True,
                template = 'plotly_white',
                trendline = 'ols',
                height = 200
            )
            fig.update_traces(
                mode = 'lines'
            )
            fig.data[-1].line.dash = 'dot'
            fig.data[-1].line.color = 'lightgray'
            fig.update_layout(
                {
                    'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                    'paper_bgcolor' : 'rgba(0, 0, 0, 0)'
                },
                font_family = "DM Sans",
                showlegend = False,
                margin = dict(l = 0, r = 0, t = 0, b = 0),
                xaxis_title = "Tuig (year)",
                yaxis_title = None
            )

            # Current pop
            currentpop = int(df.tail(1).values[0])
            pctchange = df.pct_change().mean().values[0]
            possibpop = currentpop + (currentpop * pctchange)

            return [header, fig, currentpop, str(round(pctchange * 100, 2)) + '%', round(possibpop, 0)]
        else: raise PreventUpdate
    else: raise PreventUpdate