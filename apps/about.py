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
from utilities.utils import MarginSettings, CardStyle



layout = html.Div(
    [
        dcc.Store(id = 'com_abt_sto_brgycurrentpop'),
        dcc.Store(id = 'com_abt_sto_brgypctchange'),
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
                                            [
                                                "Hiúnong san LáMRAG",
                                                #html.Br(),
                                                html.Small(" (About LáMRAG)", className = 'text-muted')
                                            ],
                                            id = 'com_abt_h1_header'
                                        ),
                                    ],
                                    class_name = MarginSettings.row,
                                ),
                                dbc.Row(
                                    [
                                        html.Img(
                                            src = app.get_asset_url('lamrag-wordmark-dmsans-dark.png'),
                                            style = {
                                                'width' : '256px',
                                            }
                                        )
                                    ],
                                    className = 'mt-2 mb-3 py-3 justify-content-center'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H5(
                                                [
                                                    """LáMRAG an ngaran san """,
                                                    html.B("Local Management Platform for Risk Analytics and Governance"),
                                                    """ san Siyudad san Calbayog. Usa ini nga web-based information system nga tuyo
                                                    an pag-standardize ug pag-digitize san mga proseso hiúnong san incident reporting,
                                                    data banking, ug data analysis san City Disaster Risk Reduction & Management
                                                    Office (CDRRMO) san Calbayog. Ginhimo ini gamit an Python ug Dash, ug produkto ini
                                                    san usa ka-tuig nga proseso san systems engineering ug requirements analysis.
                                                    """
                                                ],
                                                className = 'lh-sm'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Small(
                                                [
                                                    """LáMRAG is the """,
                                                    html.B("Local Management Platform for Risk Analytics and Governance"),
                                                    """ of the City of Calbayog. It is a web-based information system that aims to
                                                    standardize the incident reporting, data banking, and data analysis processes
                                                    of Calbayog's City Disaster Risk Reduction & Management Office (CDRRMO). LáMRAG
                                                    was developed using Python and Dash and is the result of a year-long process of
                                                    systems engineering and requirements analysis.
                                                    """
                                                ],
                                                className = 'text-muted'
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                ),
                            ],
                            id = 'com_abt_div_header',
                            className = MarginSettings.header
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H3(
                                                [
                                                    """The Project Team"""
                                                ],
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                    class_name = MarginSettings.row
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.P(
                                                [
                                                    """LáMRAG is the output of a capstone project in IE 194 and 195 (Industrial Engineering
                                                    Capstone Project I & II) by BS Industrial Engineering students at the 
                                                    """,
                                                    html.A(
                                                        html.B("Industrial Engineering and Operations Research Department (IEORD)"),
                                                        href = 'https://ieor.engg.upd.edu.ph'
                                                    ),
                                                    """ of the """,
                                                    html.A(
                                                        html.B("University of the Philippines College of Engineering"),
                                                        href = 'https://coe.upd.edu.ph'
                                                    ),
                                                    """ in Diliman, Quezon City.
                                                    The project team, guided under the supervision of """,
                                                    html.A(html.B("Assistant Professor Benette Custodio"), href = 'https://ieor.engg.upd.edu.ph/people/faculty/assistant-professor/benette-p-custodio/'),
                                                    """, is composed of:"""
                                                ],
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dbc.CardImg(
                                                                            src = "/static/team/nics.png",
                                                                            style = {
                                                                                'width': '100%',  # Ensure the image can scale in width
                                                                                'height': '100%',  # Ensure the image can scale in height
                                                                                'object-fit' : 'cover',
                                                                                'border-radius' : '0rem'
                                                                            },
                                                                            class_name = 'img-fluid'
                                                                        ),
                                                                    ],
                                                                    class_name = 'col-12 col-sm-6 col-md-5 col-lg-4'
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.CardBody(
                                                                            [
                                                                                html.H4(
                                                                                    [
                                                                                        "Nicolas Bracamonte Faller, Jr. • ",
                                                                                        html.A(
                                                                                            html.I(className = 'bi bi-linkedin'),
                                                                                            href = 'https://www.linkedin.com/in/nbfaller',
                                                                                            className = 'align-self-center',
                                                                                            target = '_blank'
                                                                                        ),
                                                                                        html.A(
                                                                                            html.I(className = 'bi bi-github ms-2'),
                                                                                            href = 'https://github.com/nbfaller',
                                                                                            className = 'align-self-center',
                                                                                            target = '_blank'
                                                                                        ),
                                                                                    ],
                                                                                    className = 'card-title align-self-center'
                                                                                ),
                                                                                html.P(
                                                                                    """
                                                                                        Nics is the team leader for this project. A native of Calbayog City, he is deeply passionate about
                                                                                        regional development and equal access to economic opportunity. He has an acute
                                                                                        addiction for UP Diliman kwek-kwek, Area 2 sisig, and white chocolate mocha frappucinos.
                                                                                    """,
                                                                                ),
                                                                                html.H5(
                                                                                    [
                                                                                        html.I(className = 'bi bi-music-note-beamed me-2'),
                                                                                        "My capstone era LSS:",
                                                                                    ],
                                                                                    className = 'mb-3'
                                                                                ),
                                                                                html.Iframe(
                                                                                    #src = 'https://open.spotify.com/embed/track/6f6IdBXL1sAHMVgwlcawDf?utm_source=generator',
                                                                                    #src = 'https://open.spotify.com/embed/track/3ZztcZYTUG2o8jViQMHmRn?utm_source=generator',
                                                                                    src = 'https://open.spotify.com/embed/track/6zELuTXrMMOk4fFIf3OErT?utm_source=generator',
                                                                                    width = '100%',
                                                                                    height = '152px',
                                                                                    style = {
                                                                                        'border-radius' : '12px',
                                                                                        #'margin' : '-2em'
                                                                                    },
                                                                                    allow = 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture',
                                                                                    loading_state = 'lazy',
                                                                                    className = 'mb-0'
                                                                                )
                                                                            ]
                                                                        ),
                                                                    ],
                                                                    class_name = 'align-self-center'
                                                                )
                                                            ],
                                                            className = 'g-1',
                                                        ),
                                                    ],
                                                    #body = True,
                                                    style = CardStyle.get_style(),
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                    class_name = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dbc.CardImg(
                                                                            src = "/static/team/leiz.png",
                                                                            style = {
                                                                                'width': '100%',  # Ensure the image can scale in width
                                                                                'height': '100%',  # Ensure the image can scale in height
                                                                                'object-fit': 'cover',
                                                                                'border-radius' : '0rem'
                                                                            },
                                                                            class_name = 'img-fluid'
                                                                        ),
                                                                    ],
                                                                    class_name = 'col-12 col-sm-6 col-md-5 col-lg-4'
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.CardBody(
                                                                            [
                                                                                html.H4(
                                                                                    [
                                                                                        "Leiz Isobelle Castor • ",
                                                                                        html.A(
                                                                                            html.I(className = 'bi bi-linkedin'),
                                                                                            #href = 'https://www.linkedin.com/in/nbfaller',
                                                                                            className = 'align-self-center',
                                                                                            target = '_blank'
                                                                                        ),
                                                                                    ],
                                                                                    className = 'card-title align-self-center'
                                                                                ),
                                                                                html.P(
                                                                                    """
                                                                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam quis dui sit amet libero fringilla pellentesque. Fusce vitae ipsum convallis nisi condimentum vulputate. Aliquam erat volutpat. Nam ac nibh tempor, hendrerit lacus a, rhoncus velit. Donec tempus non nisi ac dignissim. Vestibulum viverra, leo nec.
                                                                                    """,
                                                                                ),
                                                                                html.H5(
                                                                                    [
                                                                                        html.I(className = 'bi bi-music-note-beamed me-2'),
                                                                                        "My capstone era LSS:",
                                                                                    ],
                                                                                    className = 'mb-3'
                                                                                ),
                                                                                html.Iframe(
                                                                                    #src = 'https://open.spotify.com/embed/track/6f6IdBXL1sAHMVgwlcawDf?utm_source=generator',
                                                                                    width = '100%',
                                                                                    height = '152px',
                                                                                    style = {
                                                                                        'border-radius' : '12px',
                                                                                        #'margin' : '-2em'
                                                                                    },
                                                                                    allow = 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture',
                                                                                    loading_state = 'lazy',
                                                                                    className = 'mb-0'
                                                                                )
                                                                            ]
                                                                        ),
                                                                    ],
                                                                    class_name = 'align-self-center'
                                                                )
                                                            ],
                                                            className = 'g-1',
                                                        ),
                                                    ],
                                                    #body = True,
                                                    style = CardStyle.get_style(),
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                    class_name = 'mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dbc.CardImg(
                                                                            src = "/static/team/maerix.png",
                                                                            style = {
                                                                                'width': '100%',  # Ensure the image can scale in width
                                                                                'height': '100%',  # Ensure the image can scale in height
                                                                                'object-fit': 'cover',
                                                                                'border-radius' : '0rem'
                                                                            },
                                                                            class_name = 'img-fluid'
                                                                        ),
                                                                    ],
                                                                    class_name = 'col-12 col-sm-6 col-md-5 col-lg-4'
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.CardBody(
                                                                            [
                                                                                html.H4(
                                                                                    [
                                                                                        "Hannah Maerix Catalan • ",
                                                                                        html.A(
                                                                                            html.I(className = 'bi bi-linkedin'),
                                                                                            #href = 'https://www.linkedin.com/in/nbfaller',
                                                                                            className = 'align-self-center',
                                                                                            target = '_blank'
                                                                                        ),
                                                                                    ],
                                                                                    className = 'card-title align-self-center'
                                                                                ),
                                                                                html.P(
                                                                                    """
                                                                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam quis dui sit amet libero fringilla pellentesque. Fusce vitae ipsum convallis nisi condimentum vulputate. Aliquam erat volutpat. Nam ac nibh tempor, hendrerit lacus a, rhoncus velit. Donec tempus non nisi ac dignissim. Vestibulum viverra, leo nec.
                                                                                    """,
                                                                                ),
                                                                                html.H5(
                                                                                    [
                                                                                        html.I(className = 'bi bi-music-note-beamed me-2'),
                                                                                        "My capstone era LSS:",
                                                                                    ],
                                                                                    className = 'mb-3'
                                                                                ),
                                                                                html.Iframe(
                                                                                    #src = 'https://open.spotify.com/embed/track/6f6IdBXL1sAHMVgwlcawDf?utm_source=generator',
                                                                                    width = '100%',
                                                                                    height = '152px',
                                                                                    style = {
                                                                                        'border-radius' : '12px',
                                                                                        #'margin' : '-2em'
                                                                                    },
                                                                                    allow = 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture',
                                                                                    loading_state = 'lazy',
                                                                                    className = 'mb-0'
                                                                                )
                                                                            ]
                                                                        ),
                                                                    ],
                                                                    class_name = 'align-self-center'
                                                                )
                                                            ],
                                                            className = 'g-1',
                                                        ),
                                                    ],
                                                    #body = True,
                                                    style = CardStyle.get_style(),
                                                ),
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                    class_name = 'mb-3'
                                ),
                            ],
                            id = 'com_abt_div_team',
                            className = MarginSettings.div
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H3(
                                                [
                                                    """Acknowledgements"""
                                                ],
                                            ),
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                    class_name = MarginSettings.row
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.P(
                                                    [
                                                        """The development of LáMRAG would not have been possible without the
                                                        support and accommodation of the """,
                                                        html.B("City Disaster Risk Reduction & Management Office (CDRRMO) of Calbayog"),
                                                        """. The project team extends its gratitude, first and foremost, to City DRRM Officer """,
                                                        html.B(
                                                            "Sandro C. Daguman, DMD"
                                                        ),
                                                        """ for his interest in and eventual support of this project. The team also thanks the
                                                        CDRRMO's section heads—""",
                                                        html.B(
                                                            "Ma. Fatima Shaira Adona"
                                                        ),
                                                        " (Administration & Training), ",
                                                        html.B(
                                                            "Basilio Tongonon Jr."
                                                        ),
                                                        " (Research & Planning), and ",
                                                        html.B(
                                                            "Joseph Von Catorce"
                                                        ),
                                                        """ (Operation & Warning)—for their assistance. The following officials
                                                        of the CDRRMO are also hereby acknowledged for their support:""",
                                                        html.Li(
                                                            [
                                                                html.B("Jamaica Ultra"),
                                                                ", Data Banking Officer;"
                                                            ],
                                                            className = 'ms-3'
                                                        ),
                                                        html.Li(
                                                            [
                                                                html.B("Rodolfo Gonzaga, Jr."),
                                                                ", Barangay Assessment Team Officer (Community Project Coordinator for the Calbayog District);"
                                                            ],
                                                            className = 'ms-3'
                                                        ),
                                                        html.Li(
                                                            [
                                                                html.B("Hazelle Charis Hugo"),
                                                                ", Barangay Assessment Team Officer (Community Project Coordinator for the Tinambacan District);"
                                                            ],
                                                            className = 'ms-3'
                                                        ),
                                                        html.Li(
                                                            [
                                                                html.B("Milagros Abrito"),
                                                                ", Barangay Assessment Team Officer (Community Project Coordinator for the Oquendo District); and"
                                                            ],
                                                            className = 'ms-3'
                                                        ),
                                                        html.Li(
                                                            [
                                                                html.B("Prescila Daguman"),
                                                                ", Administrative Section Officer."
                                                            ],
                                                            className = 'ms-3'
                                                        ),
                                                        """ The project team also extends its gratitude to the rest of the CDRRMO's staff, its responders,
                                                        and the barangay officials who accommodated the project team in their implementation of the project's
                                                        user experience survey for their cooperation, support, and generosity.""",                                             
                                                    ],
                                                ),
                                                html.P(
                                                    [
                                                        """As for support coming from the """,
                                                        html.A(html.B("UPD Industrial Engineering and Operations Research Department"), href = 'https://ieor.engg.upd.edu.ph'),
                                                        """, the project team would first like to extend its wholehearted gratitude to """,
                                                        html.A(html.B("Asst. Prof. Benette Custodio"), href = 'https://ieor.engg.upd.edu.ph/people/faculty/assistant-professor/benette-p-custodio/'),
                                                        """ for her mentorship and guidance as the project team's adviser. The team would also like to thank """,
                                                        html.A(html.B("Asst. Prof. Raymond Freth Lagria"), href = 'https://ieor.engg.upd.edu.ph/people/faculty/assistant-professor/raymond-freth-a-lagria/'),
                                                        """ for his support as the department's chairperson and """,
                                                        html.A(html.B("Asst. Prof. Carlo Angelo Sonday"), href = 'https://ieor.engg.upd.edu.ph/people/faculty/assistant-professor/carlo-angelo-a-sonday/'),
                                                        """ for his technical guidance in information systems development, database engineering, and web application deployment.""",
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        """Ultimately, the project team would like to thank the City Government of Calbayog, led by """,
                                                        html.A(html.B("Mayor Raymund C. Uy"), href = 'https://www.facebook.com/people/Raymund-Monmon-C-Uy/100086298882034/'),
                                                        """, """,
                                                        html.A(html.B("Vice Mayor Rex M. Daguman"), href = 'https://www.facebook.com/RexMDaguman'),
                                                        """, and the members of the """,
                                                        html.A(html.B("Sangguniang Panlungsod"), href = 'https://www.facebook.com/calbayogsp/'),
                                                        """ for their accommodation of and support for this project.""",
                                                    ]
                                                )
                                            ],
                                            class_name = 'align-self-center mb-2 mb-lg-0 col-12'
                                        ),
                                    ],
                                    class_name = MarginSettings.row
                                ),
                            ],
                            id = 'com_abt_div_acknowledgements',
                            className = MarginSettings.div
                        )
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)