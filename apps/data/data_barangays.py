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
        dcc.Store(id = 'dat_bar_sto_brgycurrentpop'),
        dcc.Store(id = 'dat_bar_sto_brgypctchange'),
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
                                ),
                                dbc.Row(
                                    [

                                        dbc.Col(
                                            dbc.Label(
                                                [
                                                    "Barangay",
                                                    #html.Br(), html.Small(" (User type)", className = 'text-muted')
                                                ],
                                                id = 'dat_bar_label_brgy_id',
                                                class_name = row_m
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-2'
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'dat_bar_input_brgy_id',
                                                clearable = True,
                                                #value = 1
                                               ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12 col-md-10'
                                        ),
                                    ], className = 'mb-1 mb-md-0',
                                    id = 'dat_bar_row_selectbrgy'
                                ),
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
                                                                                        html.B("-", id = 'dat_bar_spa_currentpop_war'),
                                                                                        " ka-tawo an naukoy dinhi yana sumala san datos san Philippine Statistics Authority.",
                                                                                        html.Small(
                                                                                            [
                                                                                                " (",
                                                                                                html.B("-", id = 'dat_bar_spa_currentpop_en'),
                                                                                                " people live here according to the Philippine Statistics Authority.)"
                                                                                            ],
                                                                                            className = 'text-muted'
                                                                                        )
                                                                                    ],
                                                                                    style = {
                                                                                        'margin-left' : '1em',
                                                                                        'text-indent' : '-1em'
                                                                                    }
                                                                                ),
                                                                                html.Li(
                                                                                    [
                                                                                        html.B("-", id = 'dat_bar_spa_pctchange_war'),
                                                                                        " kada tuig an pagdako san populasyon dinhi base sa historical data.",
                                                                                        html.Small(
                                                                                            [
                                                                                                " (The population here increases by ",
                                                                                                html.B("-", id = 'dat_bar_spa_pctchange_en'),
                                                                                                " every year according to historical data.)"
                                                                                            ],
                                                                                            className = 'text-muted'
                                                                                        )
                                                                                    ],
                                                                                    style = {
                                                                                        'margin-left' : '1em',
                                                                                        'text-indent' : '-1em'
                                                                                    }
                                                                                ),
                                                                                html.Li(
                                                                                    [
                                                                                        "Posible umabot sa ",
                                                                                        html.B("-", id = 'dat_bar_spa_possibpop_war'),
                                                                                        " ka-tawo an populasyon dinhi pag-abot san sunod nga tuig.",
                                                                                        html.Small(
                                                                                            [
                                                                                                " (The population may hit ",
                                                                                                html.B("-", id = 'dat_bar_spa_possibpop_en'),
                                                                                                " by next year.)"
                                                                                            ],
                                                                                            className = 'text-muted'
                                                                                        )
                                                                                    ],
                                                                                    style = {
                                                                                        'margin-left' : '1em',
                                                                                        'text-indent' : '-1em'
                                                                                    }
                                                                                )
                                                                            ]
                                                                        )
                                                                    ], class_name = row_m
                                                                ),
                                                                html.Hr(),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.H5(
                                                                                    [
                                                                                        html.I(className = 'bi bi-calculator me-2'),
                                                                                        "Population calculator",
                                                                                        #html.Br(),
                                                                                        #html.Small(" (Population)", className = 'text-muted')
                                                                                    ]
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ], class_name = row_m
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            dbc.Label(
                                                                                [
                                                                                    "Tuig", #html.Br(),
                                                                                    html.Small(" (Year)", className = 'text-muted')
                                                                                ],
                                                                                id = 'dat_bar_label_calcyear',
                                                                                class_name = label_m
                                                                            ),
                                                                            class_name = 'align-self-center mb-2 mb-lg-0 col-5 col-md-3'
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                type = 'number',
                                                                                id = 'dat_bar_input_calcyear',
                                                                                #min = 2021,
                                                                                #placeholder = 'Example: Mr., Mrs., Ms., Dr.'
                                                                            ),
                                                                            class_name = 'align-self-center mb-2 mb-lg-0 col-7 col-md-9'
                                                                        ),
                                                                    ], class_name = row_m
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            dbc.Label(
                                                                                [
                                                                                    "Populasyon", #html.Br(),
                                                                                    html.Small(" (Population)", className = 'text-muted')
                                                                                ],
                                                                                id = 'dat_bar_label_calcpop',
                                                                                class_name = label_m
                                                                            ),
                                                                            class_name = 'align-self-center mb-2 mb-lg-0 col-5 col-md-3'
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                type = 'number',
                                                                                id = 'dat_bar_input_calcpop',
                                                                                disabled = True,
                                                                                #placeholder = 'Example: Mr., Mrs., Ms., Dr.'
                                                                            ),
                                                                            class_name = 'align-self-center mb-2 mb-lg-0 col-7 col-md-9'
                                                                        ),
                                                                    ], class_name = row_m
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.Small(
                                                                                    [
                                                                                        """Gamita ini nga population calculator para matigo nimo an posible nga kadamo san tawo nga
                                                                                        maukoy sini nga barangay sa tiarabot nga mga tuig. Alayon paghinumdom nga angay la ini
                                                                                        gamiton komo tigo, ug diri ini pwede sumaliwan sa mga sakto nga ihap nga hatag san
                                                                                        Philippine Statistics Authority (PSA) o City Planning and Development Office (CPDO).""",
                                                                                        html.Br(),
                                                                                        html.Small(
                                                                                            """(Feel free to use this population calculator to predict the population of this
                                                                                            barangay in the coming years. Please note that the population generated here is only
                                                                                            speculative, and is not meant to replace any authoritative data provided by
                                                                                            the Philippine Statistics Authority (PSA) or City Planning and Development Office
                                                                                            (CPDO).)""",
                                                                                            className = 'text-muted'
                                                                                        )
                                                                                    ], className = p_m
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ], class_name = row_m
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    id = 'dat_bar_car_popgraph',
                                                    style = card_style,
                                                    class_name = 'w-md-100'
                                                )
                                            ],
                                            class_name = 'mb-3 mb-lg-0 col-12 col-lg-7'
                                        ),
                                        dbc.Col(
                                            [
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
                                                                                                        html.I(className = 'bi bi-exclamation-diamond-fill me-2'),
                                                                                                        "Mga hazard",
                                                                                                        #html.Br(),
                                                                                                        html.Small(" (Hazards)", className = 'text-muted')
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
                                                                                                html.H1(
                                                                                                    [
                                                                                                        html.I(className = 'fa fa-house-flood-water me-2'),
                                                                                                        html.Span("-", id = 'dat_bar_spa_vul_flood')
                                                                                                    ],
                                                                                                    id = 'dat_bar_h1_vul_flood',
                                                                                                    style = {'color' : 'gray'}
                                                                                                ),
                                                                                            ],
                                                                                            class_name = 'd-flex justify-content-center'
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            [
                                                                                                html.H1(
                                                                                                    [
                                                                                                        html.I(className = 'fa fa-hill-rockslide me-2'),
                                                                                                        html.Span("-", id = 'dat_bar_spa_vul_landslide')
                                                                                                    ],
                                                                                                    id = 'dat_bar_h1_vul_landslide',
                                                                                                    style = {'color' : 'gray'}
                                                                                                ),
                                                                                            ],
                                                                                            class_name = 'd-flex justify-content-center'
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            [
                                                                                                html.H1(
                                                                                                    [
                                                                                                        html.I(className = 'fa fa-house-tsunami me-2'),
                                                                                                        html.Span("-", id = 'dat_bar_spa_vul_stormsurge')
                                                                                                    ],
                                                                                                    id = 'dat_bar_h1_vul_stormsurge',
                                                                                                    style = {'color' : 'gray'}
                                                                                                ),
                                                                                            ],
                                                                                            class_name = 'd-flex justify-content-center'
                                                                                        ),
                                                                                    ], class_name = row_m
                                                                                ),
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                                html.P(
                                                                                                    [
                                                                                                        "Sumala san datos san ",
                                                                                                        html.B(html.A("UP National Operational Assessment of Hazards", href = 'https://noah.up.edu.ph/', style = hyperlink_style)),
                                                                                                        #":",
                                                                                                        #html.Br(),
                                                                                                        html.Small(
                                                                                                            [
                                                                                                                " (According to data from the ",
                                                                                                                html.B(html.A("UP National Operational Assessment of Hazards", href = 'https://noah.up.edu.ph/', style = hyperlink_style)),
                                                                                                                "):",
                                                                                                            ],
                                                                                                            className = 'text-muted'
                                                                                                        )
                                                                                                    ],
                                                                                                    className = 'mb-0'
                                                                                                ),
                                                                                                html.Li(
                                                                                                    [
                                                                                                        html.B(id = 'dat_bar_spa_vul_flood_label_war'),
                                                                                                        " an posibilidad nga matabo an pagbaha dinhi.",
                                                                                                        #html.Br(),
                                                                                                        html.Small(
                                                                                                            [
                                                                                                                " (The likelihood of flooding to occur here is ",
                                                                                                                html.B(id = 'dat_bar_spa_vul_flood_label_en'),
                                                                                                                ".)"
                                                                                                            ],
                                                                                                            className = 'text-muted'
                                                                                                        )
                                                                                                    ],
                                                                                                    style = {
                                                                                                        'margin-left' : '1em',
                                                                                                        'text-indent' : '-1em'
                                                                                                    }
                                                                                                ),
                                                                                                html.Li(
                                                                                                    [
                                                                                                        html.B(id = 'dat_bar_spa_vul_landslide_label_war'),
                                                                                                        " an posibilidad nga matabo an pagtimpag san tuna dinhi.",
                                                                                                        #html.Br(),
                                                                                                        html.Small(
                                                                                                            [
                                                                                                                " (The likelihood of landslides occuring here is ",
                                                                                                                html.B(id = 'dat_bar_spa_vul_landslide_label_en'),
                                                                                                                ".)"
                                                                                                            ],
                                                                                                            className = 'text-muted'
                                                                                                        )
                                                                                                    ],
                                                                                                    style = {
                                                                                                        'margin-left' : '1em',
                                                                                                        'text-indent' : '-1em'
                                                                                                    }
                                                                                                ),
                                                                                                html.Li(
                                                                                                    [
                                                                                                        html.B(id = 'dat_bar_spa_vul_stormsurge_label_war'),
                                                                                                        " an posibilidad nga matabo an daluyong san bagyo dinhi.",
                                                                                                        #html.Br(),
                                                                                                        html.Small(
                                                                                                            [
                                                                                                                " (The likelihood of storm surges occuring here is ",
                                                                                                                html.B(id = 'dat_bar_spa_vul_stormsurge_label_en'),
                                                                                                                ".)"
                                                                                                            ],
                                                                                                            className = 'text-muted'
                                                                                                        )
                                                                                                    ],
                                                                                                    style = {
                                                                                                        'margin-left' : '1em',
                                                                                                        'text-indent' : '-1em'
                                                                                                    }
                                                                                                ),
                                                                                            ]
                                                                                        )
                                                                                    ], class_name = row_m
                                                                                ),
                                                                                #html.Hr(),
                                                                                #dbc.Row(
                                                                                #    [
                                                                                #        dbc.Col(
                                                                                #            [
                                                                                #                html.Small(
                                                                                #                    [
                                                                                #                        """An UP National Operational Assessment of Hazards (UP NOAH) in usa nga plataporma
                                                                                #                        san University of the Philippines Resilience Institute (UPRI). Ungay sa mga ginsukol
                                                                                #                        nga mga hazard an: 100 ka-tuig nga rain return para baha; hababaw ug "structurally-controlled"
                                                                                #                        nga pagtimpag san tuna; ug 5 ka-metros para sa mga storm surge.
                                                                                #                        
                                                                                #                        Alayon paghinumdom nga ada pa sa beta release an UP NOAH. Karuyag signgon sini, diri magkakamay-ada
                                                                                #                        sala an UP NOAH Center para sa mga posible nga rubat o pagkawara nga matatabo tungod sa pagbase
                                                                                #                        sini nga mga datos.""",
                                                                                #                        html.Br(),
                                                                                #                        html.Small(
                                                                                #                            """(The UP National Operational Assessment of Hazards (UP NOAH) is a platform of the
                                                                                #                            University of the Philippines Resilience Institute (UPRI). Included in the
                                                                                #                            measurement of these hazards are: 100-year rain return for floods; shallow and
                                                                                #                            structurally-controlled landslides; and 5-meters for storm surges.
                                                                                #                            
                                                                                #                            Please note that UP NOAH is still in beta release. In other words, the UP NOAH Center will
                                                                                #                            not be held liable for any damage or loss resulting from the use of the data above.)""",
                                                                                #                            className = 'text-muted'
                                                                                #                        )
                                                                                #                    ], className = p_m
                                                                                #                ),
                                                                                #            ]
                                                                                #        )
                                                                                #    ], class_name = row_m
                                                                                #)
                                                                            ]
                                                                        )
                                                                    ],
                                                                    id = 'dat_bar_car_hazardscores',
                                                                    style = card_style,
                                                                    class_name = 'w-md-100'
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    class_name = 'mb-3'
                                                ),
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
                                                                                                    #src = 'https://www.openstreetmap.org/export/embed.html?bbox=124.57210779190065%2C12.192325526584924%2C124.59013223648073%2C12.210047691115944&amp;layer=cyclosm',
                                                                                                    #src = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d562.5407776071039!2d124.61192079862425!3d12.06236092006715!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3309db8c252d21d1%3A0xaf1f98f12b16d98f!2sCalbayogCdrrmo!5e1!3m2!1sen!2sph!4v1709188668855!5m2!1sen!2sph',
                                                                                                    id = 'dat_bar_ifr_brgymap',
                                                                                                    width = '100%',
                                                                                                    height = '300em',
                                                                                                    style = {'border' : '0'},
                                                                                                    #allowfullscreen ="",
                                                                                                    loading_state = 'lazy',
                                                                                                    referrerPolicy = 'no-referrer-when-downgrade'
                                                                                                )
                                                                                            ]
                                                                                        )
                                                                                    ], class_name = row_m
                                                                                ),
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                                html.Small(
                                                                                                    [
                                                                                                        """Posible nga diri sakto an ginpapakita nga mga border o boundary sini nga mapa. Para
                                                                                                        sa sakto nga guhit sini nga barangay, alayon pag-aro sa City Planning and Development
                                                                                                        Office (CPDO).""",
                                                                                                        html.Br(),
                                                                                                        html.Small(
                                                                                                            """(The boundaries shown in this map may be incorrect. For an accurate sketch,
                                                                                                            please reach out to the City Planning and Development Office or CPDO.)""",
                                                                                                            className = 'text-muted'
                                                                                                        )
                                                                                                    ], className = p_m
                                                                                                ),
                                                                                            ]
                                                                                        )
                                                                                    ], class_name = row_m
                                                                                )
                                                                            ]
                                                                        )
                                                                    ],
                                                                    id = 'dat_bar_car_spotmap',
                                                                    style = card_style,
                                                                    class_name = 'w-md-100'
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    class_name = 'mb-3'
                                                )
                                            ],
                                            class_name = 'mb-3 mb-lg-0 col-12 col-lg-5'
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

# Callback for populating dropdowns
@app.callback(
    [
        # Selected barangay
        Output('dat_bar_input_brgy_id', 'options'),
        Output('dat_bar_input_brgy_id', 'value'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgy_id', 'data'),
    ]
)

def dat_bar_populatedropdowns(pathname, region, province, citymun, brgy):
    if pathname == '/data/barangays':
        dropdowns = []

        # Barangays
        sql = """SELECT name AS label, id AS value
        FROM utilities.addressbrgy WHERE region_id = %s AND province_id = %s AND citymun_id = %s;
        """
        values = [region, province, citymun]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        brgys = df.to_dict('records')
        dropdowns.append(brgys)
        dropdowns.append(brgy)

        return dropdowns
    else: raise PreventUpdate

# Callback for showing barangay-specific information
@app.callback(
    [
        # Header
        Output('dat_bar_h1_header', 'children'),
        # Map
        Output('dat_bar_ifr_brgymap', 'src'),
        # Flood vulnerability
        Output('dat_bar_spa_vul_flood', 'children'),
        Output('dat_bar_h1_vul_flood', 'style'),
        Output('dat_bar_spa_vul_flood_label_war', 'children'),
        Output('dat_bar_spa_vul_flood_label_war', 'style'),
        Output('dat_bar_spa_vul_flood_label_en', 'children'),
        # Landslide vulnerability
        Output('dat_bar_spa_vul_landslide', 'children'),
        Output('dat_bar_h1_vul_landslide', 'style'),
        Output('dat_bar_spa_vul_landslide_label_war', 'children'),
        Output('dat_bar_spa_vul_landslide_label_war', 'style'),
        Output('dat_bar_spa_vul_landslide_label_en', 'children'),
        # Storm surge vulnerability
        Output('dat_bar_spa_vul_stormsurge', 'children'),
        Output('dat_bar_h1_vul_stormsurge', 'style'),
        Output('dat_bar_spa_vul_stormsurge_label_war', 'children'),
        Output('dat_bar_spa_vul_stormsurge_label_war', 'style'),
        Output('dat_bar_spa_vul_stormsurge_label_en', 'children'),
        # Minimum population calculator year
        Output('dat_bar_input_calcyear', 'min'),
        Output('dat_bar_input_calcyear', 'value'),
        # Figures and other data
        Output('dat_bar_gra_brgypop', 'figure'),
        Output('dat_bar_spa_currentpop_war', 'children'),
        Output('dat_bar_spa_currentpop_en', 'children'),
        Output('dat_bar_sto_brgycurrentpop', 'data'),
        Output('dat_bar_spa_pctchange_war', 'children'),
        Output('dat_bar_spa_pctchange_en', 'children'),
        Output('dat_bar_sto_brgypctchange', 'data'),
        Output('dat_bar_spa_possibpop_war', 'children'),
        Output('dat_bar_spa_possibpop_en', 'children')
    ],
    [
        #Input('url', 'pathname'),
        Input('dat_bar_input_brgy_id', 'value')
    ],
    [
        State('app_region_id', 'data'),
        State('app_province_id', 'data'),
        State('app_citymun_id', 'data'),
        State('app_brgyinfo_cols', 'data'),
        State('app_latestcensusyear', 'data')
    ]
)

def dat_bar_setbrgyinfo(brgy, region, province, citymun, info_cols, censusyear):
    if brgy:
        toreturn = []

        # Header
        header = None
        sql = """SELECT addressbrgy.name, addressbrgy.pop_2000, addressbrgy.pop_2007, addressbrgy.pop_2010, addressbrgy.pop_2015, addressbrgy.pop_2020,
            addressbrgy.vul_flood, addressbrgy.vul_landslide, addressbrgy.vul_stormsurge,
            vultype_flood.label_war, vultype_landslide.label_war, vultype_stormsurge.label_war,
            vultype_flood.label_en, vultype_landslide.label_en, vultype_stormsurge.label_en,
            vultype_flood.color, vultype_landslide.color, vultype_stormsurge.color,
            vultype_flood.score, vultype_landslide.score, vultype_stormsurge.score,
            addressbrgy.map_src
            FROM utilities.addressbrgy
            LEFT JOIN utilities.vultype AS vultype_flood ON addressbrgy.vul_flood = vultype_flood.id
            LEFT JOIN utilities.vultype AS vultype_landslide ON addressbrgy.vul_landslide = vultype_landslide.id
            LEFT JOIN utilities.vultype AS vultype_stormsurge ON addressbrgy.vul_stormsurge = vultype_stormsurge.id
            WHERE addressbrgy.region_id = %s AND addressbrgy.province_id = %s AND addressbrgy.citymun_id = %s AND addressbrgy.id = %s;"""
        values = [region, province, citymun, brgy]
        cols = info_cols + [
            'vul_flood', 'vul_landslide', 'vul_stormsurge',
            'label_war_flood', 'label_war_landslide', 'label_war_stormsurge',
            'label_en_flood', 'label_en_landslide', 'label_en_stormsurge',
            'color_flood', 'color_landslide', 'color_stormsurge',
            'score_flood', 'score_landslide', 'score_stormsurge',
            'map_src'
            ]
        df = db.querydatafromdatabase(sql, values, cols)
        header = df['name'][0]
        toreturn.append(header)

        # Map
        toreturn.append(df['map_src'][0])
            
        # Flood vulnerability
        toreturn.append(df['vul_flood'][0])
        toreturn.append({'color' : df['color_flood'][0]})
        toreturn.append(df['label_war_flood'][0])
        toreturn.append({'color' : df['color_flood'][0]})
        toreturn.append(df['label_en_flood'][0])
        # Landslide vulnerability
        toreturn.append(df['vul_landslide'][0])
        toreturn.append({'color' : df['color_landslide'][0]})
        toreturn.append(df['label_war_landslide'][0])
        toreturn.append({'color' : df['color_landslide'][0]})
        toreturn.append(df['label_en_landslide'][0])
        # Storm surge vulnerability
        toreturn.append(df['vul_stormsurge'][0])
        toreturn.append({'color' : df['color_stormsurge'][0]})
        toreturn.append(df['label_war_stormsurge'][0])
        toreturn.append({'color' : df['color_stormsurge'][0]})
        toreturn.append(df['label_en_stormsurge'][0])

        # Minimum population calculator year
        toreturn.append(censusyear + 1)
        toreturn.append(None)

        # Graph
        pop_df = df[info_cols]
        pop_df = pop_df.set_index('name').T
        fig = px.scatter(
            pop_df,
            x = pop_df.index,
            y = pop_df.columns,
            #markers = True,
            template = 'plotly_white',
            trendline = 'ols',
            height = 400
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
            yaxis_title = None,
            yaxis_range=[0, 10000]
        )
        #fig.update_yaxes(
        #    autorangeoptions_minallowed = 0
        #)
        toreturn.append(fig)

        # Current pop
        currentpop = int(pop_df.tail(1).values[0])
        pctchange = pop_df.pct_change().mean().values[0]
        possibpop = currentpop * (1 + pctchange)
        toreturn.append(currentpop)
        toreturn.append(currentpop)
        toreturn.append(currentpop)
        # Percent change
        toreturn.append(str(round(pctchange * 100, 2)) + "%")
        toreturn.append(str(round(pctchange * 100, 2)) + "%")
        toreturn.append(pctchange)
        # Possible population
        toreturn.append(round(possibpop, 0))
        toreturn.append(round(possibpop, 0))

        return toreturn
    else: raise PreventUpdate

# Callback for calculating projected population
@app.callback(
    [
        Output('dat_bar_input_calcpop', 'value')
    ],
    [
        Input('dat_bar_input_calcyear', 'value')
    ],
    [
        State('app_latestcensusyear', 'data'),
        State('dat_bar_sto_brgycurrentpop', 'data'),
        State('dat_bar_sto_brgypctchange', 'data')
    ]
)

def dat_bar_calcyear(year, censusyear, currentpop, pctchange):
    projpop = None
    if year and year > censusyear:
        projpop = round(currentpop * (1 + pctchange)**(year - censusyear), 0)
    return [projpop]