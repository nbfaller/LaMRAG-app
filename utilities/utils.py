from dash import html
import dash_bootstrap_components as dbc

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