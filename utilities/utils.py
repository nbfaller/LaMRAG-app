from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Styling classes
class MarginSettings:
    def __init__(self):
        self.header = 'mb-3'
        self.div = 'mt-3 mb-3'
        self.row = 'mb-2'
        self.subhead = 'mt-3'
        self.paragraph = 'mb-0'
        self.label = 'mb-0'
        self.form_text = 'mt-1'
        self.alert_icon = 'pe-0 me-0 col-12 col-md-auto mb-2 mb-md-0'
        self.footer = 'mt-3'

class CardStyle:
    @staticmethod
    def get_style():
        return {
            'border-radius': '0.75rem',
            'overflow': 'hidden',
            'box-shadow': '0 0 32px 4px rgba(135, 113, 90, 0.2)'
        }

class RequiredTag:
    tag = html.Sup("*", className='text-danger')

# Constructors
# This one is broken
class HeaderRowConstructor:
    def __init__(self, header_text, subheader_war = None, subheader_en = None):
        self.header_text = header_text
        self.subheader_war = subheader_war
        self.subheader_en = subheader_en
    
    def construct(self):
        header = [
            html.H1(
                self.header_text
            )
        ]
        subheader_components = []
        subheader = []

        if self.subheader_war:
            subheader_components.append(
                self.subheader_war
            )
            if self.subheader_en:
                subheader_components.append(
                    [
                        html.Br(),
                        html.Small(
                            self.subheader_en,
                            className = 'text-muted'
                        )
                    ]
                )
            subheader = [
                html.P(
                    subheader_components,
                    className = MarginSettings().paragraph
                )
            ]
        
        components = header + subheader

        return dbc.Row(
            components,
            class_name = MarginSettings().row
        )

# Common callbacks
class ReturnLinkCallback:
    def __init__(self, app, link_id, text_war_id, text_en_id):
        self.link_id = link_id
        self.text_war_id = text_war_id
        self.text_en_id = text_en_id

        @app.callback(
            [
                Output(self.link_id, 'href'),
                Output(self.text_war_id, 'children'),
                Output(self.text_en_id, 'children')
            ],
            [
                Input('url', 'pathname')
            ],
            [
                State('app_sessionlogout', 'data'),
                State('app_currentuser_id', 'data')
            ]
        )

        def update_link_and_texts(pathname, sessionlogout, user_id):
            pathnames = [
                '/data/barangays',
                '/events',
                '/events/view'
            ]
            if pathname in pathnames:
                href = '/'
                war = "Balik sa home"
                en = " (Return to home)"
                if not(sessionlogout) and int(user_id) > 0:
                    href = '/dashboard'
                    war = "Balik sa dashboard"
                    en = " (Return to dashboard)"
                return [href, war, en]
            else: raise PreventUpdate