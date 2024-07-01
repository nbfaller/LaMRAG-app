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
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.H1(
                                            [
                                                "Mga patakaran hiúnong san pribasidad",
                                                #html.Br(),
                                                html.Small(" (Privacy policy)", className = 'text-muted')
                                            ],
                                            id = 'com_abt_h1_header'
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.P(
                                                    [
                                                        html.B("Petsa san pagpatuman"),
                                                        html.Span(" (Date of effectivity)", className = 'text-muted'), ":", html.Br(),
                                                        "Ika-15 san Hulyo 2024", html.Br(),
                                                        html.Span(" (15 July 2024) ", className = 'text-muted'),
                                                    ],
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = 'col-12 col-md-6'
                                        ),
                                        dbc.Col(
                                            [
                                                html.P(
                                                    [
                                                        html.B("Katapusan nga pagbag-o"),
                                                        html.Span(" (Last updated)", className = 'text-muted'), ":", html.Br(),
                                                        "Ika-15 san Hulyo 2024", html.Br(),
                                                        html.Span(" (15 July 2024) ", className = 'text-muted'),
                                                    ],
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = 'col-12 col-md-6'
                                        ),
                                    ],
                                    #class_name = MarginSettings.row,
                                ),
                            ],
                            id = 'com_pri_div_header',
                            className = MarginSettings.header
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H2("Winaray")
                                            ],
                                            id = 'com_pri_div_body_war_header',
                                            class_name = MarginSettings.row
                                        ),
                                        #dbc.Row(
                                        #    [
                                        #        dcc.Link(
                                        #            [
                                        #                html.I(className = 'bi bi-arrow-down me-2'),
                                        #                "Laktaw pakadto sa hubad sini nga mga patakaran sa Ingles.",
                                        #                html.Small(" (Skip to the English version of this policy.)")
                                        #            ],
                                        #            href = '#com_pri_div_body_en_header',
                                        #            className = 'skip-link'
                                        #        )
                                        #    ],
                                        #    class_name = MarginSettings.row
                                        #),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """Maupay nga pag-abot sa """,
                                                        html.B("Local Management Platform for Risk Analytics and Governance"),
                                                        """ o """, html.B("LáMRAG"),
                                                        """. An LáMRAG in usá nga information system nga guinhimo para sa
                                                        City Disaster Risk Reduction and Management Office (CDRRMO) san Siyudad san Calbayog.
                                                        Guinhimo ini nga sistema para magserbi komo mekanismo san pag-report san mga insidente,
                                                        pagtirok san datos, ug pag-analisar sini datos nga may kalabutan san durodilain nga mga
                                                        natural disaster nga naigo o nakakaapekto sa Siyudad san Calbayog. Limitado an paggamit
                                                        san LáMRAG sa mga opisyal san mga barangay ug mga opisyal san pamunuan sini nga siyudad."""
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        """Komo nagamit san LáMRAG, pinaura namon an imo pribasidad ug guintatalinguha namon nga
                                                        mapapanalipdan an imo personal nga datos subay san """,
                                                        html.B("Republic Act No. 10173"),
                                                        """ (nga kilala liwat komo an """,
                                                        html.B("Data Privacy Act of 2012"),
                                                        """). Guinlalatag sini nga mga patakaran hiúnong san pribasidad an
                                                        mga klase san impormasiyon o datos nga amon guintitirok, panano namon ini guingagamit, ug an mga pitad
                                                        nga amon guinbubuhat para maseguro an pagsalipod sini nga datos."""
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_war_intro',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-database-fill me-2'),
                                                        "Nano nga datos an amon guintitirok?"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.H5(
                                                    "Personal nga impormasiyon, sugad san:"
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li("Bug-os nga ngaran (primero, butnga, ug apelyido);", className = 'ms-3'),
                                                html.Li("Petsa san pagkatawo;", className = 'ms-3'),
                                                html.Li("Kun natawo ka nga babayi o lalaki;", className = 'ms-3'),
                                                html.Li("Apirmatibo nga identidad (kun sano man naangay, sugad san lived name, honorific, ug mga pronoun);", className = 'ms-3'),
                                                html.Li("Opisina ug puwesto/katungdanan sa lokal nga pamunuan;", className = 'ms-3'),
                                                html.Li("Numero sa cellphone;", className = 'ms-3'),
                                                html.Li("Email address, kun mayda;", className = 'ms-3'),
                                                html.Li("Ngaran sa Facebook, kun mayda; ug", className = 'ms-3'),
                                                html.Li("Adlaw-adlaw ug permanente nga guin-iistaran.", className = 'ms-3')
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.H5(
                                                    "Sulod san mga incident report, sugad san:"
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li("Mga detalye san insidente, sugad san klase, lokasiyon, petsa, oras, ug iba pa;", className = 'ms-3'),
                                                html.Li("Mga deskripsiyon ug dokumentasiyon, sugad san mga retrato; ug", className = 'ms-3'),
                                                html.Li("Impormasiyon hiunong san naghimo san report.", className = 'ms-3'),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.H5(
                                                    "Datos hiunong san paggamit san LáMRAG, sugad san:"
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li("Oras san mga log-in; ug", className = 'ms-3'),
                                                html.Li("Klase san nagamit nga nalog-in.", className = 'ms-3'),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                    ],
                                    id = 'com_pri_div_body_war_info',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-bank2 me-2'),
                                                        "Legal nga basehan san pagproseso san datos"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """Amon guinpoproseso an imo personal nga impormasiyon sumala san
                                                        mga nasunod nga legal nga basehan:"""
                                                    ],
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li(
                                                    [
                                                        html.B("An imo pagtugot: "),
                                                        """Kun nahatag ka permiso para maproseso namon an imo personal nga impormasiyon;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Legal nga obligasiyon: "),
                                                        """Kun kinihanglan an pagproseso para sumunod sa legal nga obligasiyon; ug"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Interes san publiko: "),
                                                        """Kun kinihanglan an pagproseso para sa paghimo san trabaho nga
                                                        guinhihimo sa interes san publiko o sa pagpapatuman san opisyal nga
                                                        awtoridad."""
                                                    ],
                                                    className = 'ms-3'
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                    ],
                                    id = 'com_pri_div_body_war_basis',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-database-fill-gear me-2'),
                                                        "Panano namon guingagamit imo datos?"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """Guingagamit namon an amon guintitirok nga impormasiyon
                                                        para sa nasunod nga mga tuyo:"""
                                                    ],
                                                    className = MarginSettings.paragraph
                                                ),
                                                html.Li("Para mapatuman ug madumara an pagreport san mga insidente;", className = 'ms-3'),
                                                html.Li("Para mag-analisar ug magresponder sa mga insidente nga may kalabutan san DRRM;", className = 'ms-3'),
                                                html.Li("Para mapaupay ug mapakusgan an mga kapabilidad san LáMRAG; ug", className = 'ms-3'),
                                                html.Li("Para maseguro an seguridad san sistema ug masalipdan ini kontra san diri guintutugutan nga pag-abri.", className = 'ms-3'),
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_war_process',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-share-fill me-2'),
                                                        "Pagbahin san datos"
                                                    ]
                                                ),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """Diri namon ibabahin an imo personal nga impormasiyon sa mga ikatulo nga
                                                        partido labot la san mga nasunod nga sitwasyon:"""
                                                    ],
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li(
                                                    [
                                                        html.B("Kinihanglan san balaod: "),
                                                        "Kun kinihanglan ini ibahin para sumunod sa balaod o legal nga proseso;"
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Pananalipod san mga katungod: "),
                                                        "Para mapanalipdan an mga katungod, pananag-iya, ug seguridad san Siyudad san Calbayog, an mga nagamit san LáMRAG, o an publiko; ug"
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Mga naghahatag serbisyo: "),
                                                        "Upod an mga tinapuran nga third-party service provider nga nabulig sa amon sa pagdudumara sini nga sistema, sa kondisyon nga natugot sira sa pagsalipod san impormasiyon ug paggamit sini para la sa mga tinuyo nga katuyuan."
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_war_sharing',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-shield-fill-check me-2'),
                                                        "Seguridad san datos"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """Guinpapatuman namon an durodilain nga mga pitad para maseguro an seguridad san imo
                                                        personal nga impormasiyon ug guinhahatag nga datos. Upod sini nga mga pitad an:"""
                                                    ],
                                                    className = MarginSettings.paragraph
                                                ),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li("Encryption san sensitibo nga datos;", className = 'ms-3'),
                                                html.Li("Regular nga pagsukol ug pagbag-o san sistema hiúnong san seguridad; ug", className = 'ms-3'),
                                                html.Li("Mga kontrol sa pag-abri para maiwasan an diri guintutugutan nga pag-abri.", className = 'ms-3'),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                    ],
                                    id = 'com_pri_div_body_war_security',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-file-lock-fill me-2'),
                                                        "Pagtipig san datos"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    """Amon guintitipig an imo personal nga impormasiyon sa sulod san pinakahalaba nga naangay nga panahon
                                                    para mapatuman an mga tuyo nga nakalatag sini nga mga patakaran o subay san pangingihanlan san balaod.
                                                    Guintitipig liwat subay sini nga mga patakaran an mga incident report ug datos nga may kalabutan sini.""",
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_war_retention',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-people-fill me-2'),
                                                        "An imo mga katungod"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    """Subay san Data Privacy Act of 2012, may-ada ka san mga nasunod nga mga katungod:""",
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li(
                                                    [
                                                        html.B("Katungod nga maging maaram: "),
                                                        """May katungod ka nga mabaro kun panano guinpoproseso an imo personal nga impormasiyon;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Katungod sa pag-abri: "),
                                                        """May katungod ka nga maabrihan ug mabasa an imo personal nga impormasiyon;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Katungod sa pag-ayad: "),
                                                        """May katungod ka nga aydon an bisan nano nga lipat o kulang nga datos;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Katungod sa pagpara: "),
                                                        """May katungod ka nga magsarit san pagpara san imo personal nga impormasiyon subay san legal ug kontraktuwal nga mga restriksiyon;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Katungod sa pagkontra: "),
                                                        """May katungod ka nga kumontra sa pagproseso san imo personal nga impormasiyon sa pinili nga mga sitwasyon;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Katungod sa data portability: "),
                                                        """May katungod ka nga makuha ug magamit utro an imo personal nga impormasiyon para san imo kalugaringon nga mga tuyo sa durodilain nga mga serbisyo; ug"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Katungod sa mga danyos: "),
                                                        """May katungod ka nga mabaydan san mga danyos tungod san diri sakto, diri kompleto, kinadaan, buwa,
                                                        ilegal nga nakuha, o diri guintugutan nga paggamit san imo personal nga impormasiyon."""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    """Para mapatuman nimo an ini nga mga katungod,
                                                    alayon pag-contact sa amon pinaagi san mga detalye nga nakasurat sa ubos
                                                    sini nga mga patakaran.""",
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                    ],
                                    id = 'com_pri_div_body_war_rights',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-pencil-square me-2'),
                                                        "Mga pagbabag-o sini nga patakaran"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """Puwede namon bag-uhon ini nga mga patakaran kun sano kinihanglan.
                                                        Ipapahibaro dinhi sini nga pahina an bisan nano nga pagbabag-o upod an petsa nga una ginpatuman
                                                        ini nga mga pagbag-o. Nakiki-alayon kami sa iyo ngatanan nga padanay-danay nga basahon ini nga mga
                                                        patakaran hiúnong san pribasidad para kamo mabaro kun panano namon ginpapanalipdan an iyo impormasiyon."""
                                                    ],
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_war_changes',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-envelope-fill me-2'),
                                                        "I-contact kami"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """Kun may-ada ka mga pakiana o karuyag ipaabot hiunong sini nga mga patakaran,
                                                        o kun karuyag mo ipatuman an imo mga katungod subay san
                                                        Data Privacy Act of 2012, alayon pag-contact sa amon sa:""", html.Br(),
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.H5("City Disaster Risk Reduction and Management Office", className = MarginSettings.paragraph),
                                                html.P(
                                                    [
                                                        """Bagacay Health Center, Magsaysay Extension (Diversion Road)""", html.Br(),
                                                        """Calbayog City, Samar 6710"""
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_war_contact',
                                    className = MarginSettings.div
                                )
                            ],
                            id = 'com_pri_div_body_war',
                            className = MarginSettings.div
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H2("English")
                                            ],
                                            id = 'com_pri_div_body_en_header',
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """Welcome to the """,
                                                        html.B("Local Management Platform for Risk Analytics and Governance"),
                                                        """ (hereinafter referred to as """, html.B("LáMRAG"),
                                                        """). LáMRAG in an information system developed for the
                                                        City Disaster Risk Reduction and Management Office (CDRRMO) of the City of Calbayog.
                                                        This system is designed to serve as a unified platform for incident reporting,
                                                        data collection, and data analysis related to various natural disasters that may hit or affect
                                                        the City of Calbayog. Access to LáMRAG is limited to barangay and city government officials."""
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        """As a user of LáMRAG, we value your privacy and are committed to protecting your personal data in accordance with """,
                                                        html.B("Republic Act No. 10173"),
                                                        """, also known as the """,
                                                        html.B("Data Privacy Act of 2012"),
                                                        """. This Privacy Policy outlines the types of information we collect, how we use it, and the measures we take to ensure its protection."""
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_en_intro',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-database-fill me-2'),
                                                        "What data do we collect?"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.H5(
                                                    "Personal information, such as:"
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li("Full name (first, middle, and surname);", className = 'ms-3'),
                                                html.Li("Date of birth;", className = 'ms-3'),
                                                html.Li("Assigned sex at birth;", className = 'ms-3'),
                                                html.Li("Affirmative identity (if applicable, such as lived name, honorific, and pronouns);", className = 'ms-3'),
                                                html.Li("Office and position/designation in the city government;", className = 'ms-3'),
                                                html.Li("Cellphone number;", className = 'ms-3'),
                                                html.Li("Email address, if any;", className = 'ms-3'),
                                                html.Li("Facebook name, if applicable; and", className = 'ms-3'),
                                                html.Li("Present and permanent addresses.", className = 'ms-3')
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.H5(
                                                    "Incident report content, such as:"
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li("Incident details such as type, location, date, time, et cetera;", className = 'ms-3'),
                                                html.Li("Descriptions and documentation, such as photos; and", className = 'ms-3'),
                                                html.Li("Reporter's information.", className = 'ms-3'),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.H5(
                                                    "System usage data, such as:"
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li("Log-in times; and", className = 'ms-3'),
                                                html.Li("User types of individual log-ins.", className = 'ms-3'),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                    ],
                                    id = 'com_pri_div_body_en_info',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-bank2 me-2'),
                                                        "Legal basis for processing"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """We process your personal information based on the following legal bases:"""
                                                    ],
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li(
                                                    [
                                                        html.B("Consent: "),
                                                        """When you have given your consent for us to process your personal information;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Legal obligation: "),
                                                        """When processing is necessary to comply with a legal obligation; and"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Public interest: "),
                                                        """When processing is necessary to perform a task carried out in the public interest or in the exercise of official authority."""
                                                    ],
                                                    className = 'ms-3'
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                    ],
                                    id = 'com_pri_div_body_en_basis',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-database-fill-gear me-2'),
                                                        "How do we use your information?"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """The information collected is used for the following purposes:"""
                                                    ],
                                                    className = MarginSettings.paragraph
                                                ),
                                                html.Li("To facilitate and manage incident reporting;", className = 'ms-3'),
                                                html.Li("To analyze and respond to disaster-related incidents;", className = 'ms-3'),
                                                html.Li("To enhance and improve the functionality of LáMRAG; and", className = 'ms-3'),
                                                html.Li("To ensure the security of the system and protect it against unauthorized access.", className = 'ms-3'),
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_en_process',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-share-fill me-2'),
                                                        "Data sharing and disclosure"
                                                    ]
                                                ),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """We do not share your personal information with third parties except in the following circumstances:"""
                                                    ],
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li(
                                                    [
                                                        html.B("Legal requirements: "),
                                                        "When disclosure is necessary to comply with the law or legal process;"
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Protection of rights: "),
                                                        "To protect the rights, property, and safety of the City of Calbayog, users of LáMRAG, or the public; and"
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Service providers: "),
                                                        "With trusted third-party service providers who assist us in operating this system, provided that they agree to keep information confidential and use it solely for the intended purposes."
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_en_sharing',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-shield-fill-check me-2'),
                                                        "Data security"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """We implement a variety of security measures to maintain the safety of your
                                                        personal information and the data you provide. These measures include:"""
                                                    ],
                                                    className = MarginSettings.paragraph
                                                ),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li("Encryption of sensitive data;", className = 'ms-3'),
                                                html.Li("Regular security assessments and updates; and", className = 'ms-3'),
                                                html.Li("Access controls to restrict unauthorized access.", className = 'ms-3'),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                    ],
                                    id = 'com_pri_div_body_en_security',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-file-lock-fill me-2'),
                                                        "Data retention"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    """We retain your personal information for the longest period necessary
                                                    to fulfill the purposes outlined in this Privacy Policy or as required by law.
                                                    Incident reports and related data are also retained in accordance with these policies.""",
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_en_retention',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-people-fill me-2'),
                                                        "Your rights"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    """Under the Data Privacy Act of 2012, you have the following rights:""",
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.Li(
                                                    [
                                                        html.B("Right to be informed: "),
                                                        """You have the right to be informed about how your personal information is processed;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Right to access: "),
                                                        """You have the right to access and read your personal information;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Right to rectification: "),
                                                        """You have the right to correct any inaccurate or incomplete data;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Right to erasure: "),
                                                        """You have the right to request the deletion of your personal information, subject to legal and contractual restrictions;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Right to object: "),
                                                        """You have the right to object to the processing of your personal information under certain circumstances;"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Right to data portability: "),
                                                        """You have the right to obtain and reuse your personal information for your own purposes across different services; and"""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                                html.Li(
                                                    [
                                                        html.B("Right to damages: "),
                                                        """You have the right to be indemnified for damages due to inaccurate, incomplete, outdated, false,
                                                        unlawfully obtained, or unauthorized use of personal information."""
                                                    ],
                                                    className = 'ms-3'
                                                ),
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    """To exercise these rights, please contact us using the details provided below.""",
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                    ],
                                    id = 'com_pri_div_body_en_rights',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-pencil-square me-2'),
                                                        "Changes to this Privacy Policy"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """We may update this Privacy Policy from time to time. Any changes will be posted on this page
                                                        with an updated effectivity date. We encourage you to review this Privacy Policy periodically to stay
                                                        informed about how we are protecting your information."""
                                                    ],
                                                    className = MarginSettings.paragraph
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_en_changes',
                                    className = MarginSettings.div
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    [
                                                        html.I(className = 'bi bi-envelope-fill me-2'),
                                                        "Contact us"
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    [
                                                        """If you have any questions or concerns about this Privacy Policy,
                                                        or if you wish to exercise your rights under the
                                                        Data Privacy Act of 2012, please contact us at:""", html.Br(),
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                html.H5("City Disaster Risk Reduction and Management Office", className = MarginSettings.paragraph),
                                                html.P(
                                                    [
                                                        """Bagacay Health Center, Magsaysay Extension (Diversion Road)""", html.Br(),
                                                        """Calbayog City, Samar 6710"""
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ],
                                    id = 'com_pri_div_body_en_contact',
                                    className = MarginSettings.div
                                )
                            ],
                            id = 'com_pri_div_body_en',
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