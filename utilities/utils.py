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
    def __init__(self, app, prefix):
        self.link_id = prefix + '_hta_returnlink'
        self.text_war_id = prefix + '_spa_returnlink_war'
        self.text_en_id = prefix + '_sma_returnlink_en'

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

class DropdownDataLoader:
    def __init__(self, db):
        self.db = db

    # Basic dropdowns
    def load_event_types(self):
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.eventtype
        ORDER BY id ASC;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')

    def load_report_types(self):
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.reporttype;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')

    def lock_report_type(self, df):
        type_value = None
        type_disabled = False
        if df.shape[0]:
            type_value = df['type_id'][0]
            type_disabled = True
        return type_value, type_disabled

    def load_user_types(self):
        sql = """SELECT label AS label, id AS value
        FROM utilities.usertype
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')

    # Personal information dropdowns
    def load_assignedsexes(self):
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.assignedsex;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')
    
    # Work information dropdowns
    def load_offices(self):
        sql = """SELECT name AS label, id AS value
        FROM utilities.office
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')
    
    # Time dropdowns
    def load_time_hh(self):
        sql = """SELECT label, value
        FROM utilities.time_hh
        ORDER BY value ASC;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')

    def load_time_mmss(self):
        sql = """SELECT label, value
        FROM utilities.time_mmss
        ORDER BY value ASC;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')
    
    # Address dropdowns
    def load_regions(self):
        sql = """SELECT name as label, id as value
        FROM utilities.addressregion;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')

    def load_barangays(self, region, province, citymun):
        sql = """SELECT name AS label, id AS value
        FROM utilities.addressbrgy
        WHERE region_id = %s AND province_id = %s AND citymun_id = %s;
        """
        values = [region, province, citymun]
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')

    def lock_brgy(self, brgy):
        brgy_value = None
        brgy_disabled = False
        if brgy and int(brgy) > 0:
            brgy_value = brgy
            brgy_disabled = True
        return brgy_value, brgy_disabled
    
    # Report dropdowns
    def load_casualty_types(self):
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') as label, id as value
        FROM utilities.casualtytype;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')
    
    def load_casualty_statuses(self):
        sql = """SELECT CONCAT(label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.casualtystatus;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')

    def load_public_utility_types(self):
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.pubutiltype;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')

    def load_public_utility_interruption_types(self):
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') AS label, id AS value, desc_war, desc_en
        FROM utilities.pubutilinttype;
        """
        values = []
        cols = ['label', 'value', 'desc_war', 'desc_en']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df[['label', 'value']].to_dict('records')
    
    def load_infra_types(self):
        sql = """SELECT CONCAT(symbol, ' ', label_war, ' (', label_en, ')') as label, id as value
        FROM utilities.infratype;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')
    
    def load_infra_classes(self):
        sql = """SELECT CONCAT(label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.infraclass;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')

    def load_qty_units(self):
        sql = """SELECT CONCAT(label_war, ' (', label_en, ')') AS label, id AS value
        FROM utilities.qtyunit;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        return df.to_dict('records')

    # Sectors and needs dropdowns
    def load_sectors(self):
        sql = """SELECT CONCAT(symbol, ';', desc_war, ';', desc_en) AS label, id AS value
        FROM utilities.demographicsector;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        for i in range (len(df.index)):
            df.at[i, 'label'] = [
                str(df['label'][i]).split(";")[0] + " " + str(df['label'][i]).split(";")[1],
                html.Br(),
                html.Small(
                    str(df['label'][i]).split(";")[2],
                    className = 'text-muted'
                )
            ]
        return df.to_dict('records')
    
    def load_needs(self):
        sql = """SELECT CONCAT(symbol, ';', desc_war, ';', desc_en) AS label, id AS value
        FROM utilities.demographicneed;
        """
        values = []
        cols = ['label', 'value']
        df = self.db.querydatafromdatabase(sql, values, cols)
        df = df.sort_values('value')
        for i in range (len(df.index)):
            df.at[i, 'label'] = [
                str(df['label'][i]).split(";")[0] + " " + str(df['label'][i]).split(";")[1],
                html.Br(),
                html.Small(
                    str(df['label'][i]).split(";")[2],
                    className = 'text-muted'
                )
            ]
        return df.to_dict('records')