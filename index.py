# Dash related dependencies
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# For opening browser
import webbrowser
# Other libraries
from urllib.parse import urlparse, parse_qs
# App definition
from app import app
from apps import dbconnect as db
from apps import dashboard, home, commonmodules as cm, error, sandbox, about, forbidden
from apps.users import users_register, users_search
from apps.reports import reports, reports_create, reports_report
from apps.events import events, events_create, events_event
from apps.data import data_activate, data_barangays, data_demographics
from apps.data.household import data_household_upload
from apps.data.barangay import data_barangay_upload

# Layout definition
CONTENT_STYLE = {
    'margin' : '5em 2em 1em',
    'padding' : '1em 1em'
}

app.layout = html.Div(
    [
        html.Meta(
            name = "theme-color",
            content = '#203354'
            #content = '#2e215e'
            #content = '#2a3385'
        ),
        # Location variable: contains details about the url
        dcc.Location(id = 'url', refresh = True),
        # Login data
        dcc.Store(id = 'app_sessionlogout', data = True, storage_type = 'session'),
        dcc.Store(id = 'app_currentuser_id', data = -1, storage_type = 'session'),
        dcc.Store(id = 'app_usertype_id', data = -1, storage_type = 'session'),
        # Store variables for locking location of app
        dcc.Store(id = 'app_region_id', data = 8, storage_type = 'session'),
        dcc.Store(id = 'app_province_id', data = 60, storage_type = 'session'),
        dcc.Store(id = 'app_citymun_id', data = 3, storage_type = 'session'),
        dcc.Store(id = 'app_brgy_id', data = -1, storage_type = 'session'),
        # Auxiliary store variables for data retrieval
        dcc.Store(id = 'app_brgyinfo_cols', data = ['name', 2000, 2007, 2010, 2015, 2020], storage_type = 'memory'),
        dcc.Store(id = 'app_latestcensusyear', data = 2020, storage_type = 'memory'),
        # Navbar
        cm.navbar,
        # Sidebar
        cm.sidebar,
        # Page content: div that contains layout
        html.Div(
            id = 'page-content',
            #style = CONTENT_STYLE,
            className = 'mt-6 mb-3 mx-3 mx-md-4pt5 p-2 p-md-3'
        ),
        cm.change_password,
        # Footer
        cm.footer
    ]
)

# Server object
server = app.server

# Callback for displaying page
@app.callback(
    [
        Output('page-content', 'children'),
        Output('app_sessionlogout', 'data')
    ],
    [
        # Callback is triggered when the path changes
        Input('url', 'pathname')
    ],
    [
        State('url', 'search'),
        State('app_sessionlogout', 'data'),
        State('app_currentuser_id', 'data'),
        State('app_usertype_id', 'data'),
        State('app_brgy_id', 'data')
    ]
)

def displaypage(pathname, search, sessionlogout, user_id, usertype_id, brgy_id):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if user_id < 0: # If logged out
                public_paths = [
                    '/about',
                    '/data/barangays',
                    '/data/demographics',
                    '/events',
                    '/events/event'
                ]
                if pathname == '/' or pathname == '/home':
                    returnlayout = home.layout
                elif pathname in public_paths:
                    returnlayout = eval(pathname.replace('/', '_').replace('-', '_')[1:] + '.layout')
                else:
                    returnlayout = error.layout
            else:
                access_control = {
                    # Public access
                    '/about': [1, 2, 3],
                    '/data/barangays' : [1, 2, 3],
                    '/data/demographics' : [1, 2, 3],
                    '/events' : [1, 2, 3],
                    '/events/event' : [1, 2, 3],
                    # Common access
                    '/dashboard' : [1, 2, 3],
                    '/reports' : [1, 2, 3],
                    '/reports/create' : [1, 2, 3],
                    '/data/household/upload' : [1, 2, 3],
                    '/data/barangay/upload' : [1, 2, 3],
                    # Administrator-restricted
                    '/users/search' : [2, 3],
                    # Superadministrator-restricted
                    '/users/register' : [3],
                    '/events/create' : [3],
                    '/data/activate' : [3],
                    '/sandbox' : [3],
                }
                if pathname == '/logout':
                    returnlayout = home.layout
                    sessionlogout = True
                elif pathname == '/reports/report':
                    if brgy_id > 0:
                        parsed = urlparse(search)
                        if parse_qs(parsed.query)['id'][0]:
                            report_id = parse_qs(parsed.query)['id'][0]
                            sql = """SELECT brgy_id FROM reports.report WHERE id = %s;"""
                            values = [report_id]
                            cols = ['brgy_id']
                            df = db.querydatafromdatabase(sql, values, cols)
                            if int(df['brgy_id'][0]) == brgy_id:
                                returnlayout = reports_report.layout
                            else:
                                returnlayout = forbidden.layout
                        else:
                            returnlayout = error.layout
                    else:
                        returnlayout = reports_report.layout
                elif pathname in access_control:
                    if usertype_id in access_control[pathname]:
                        returnlayout = eval(pathname.replace('/', '_').replace('-', '_')[1:] + '.layout')
                    else:
                        returnlayout = forbidden.layout
                else:
                    returnlayout = error.layout
            # Decide sessionlogout value
            logout_conditions = [
                pathname in ['/', '/logout'],
                user_id == -1 or usertype_id == -1,
                not(user_id) or not(usertype_id)
            ]
            sessionlogout = any(logout_conditions)

        else: raise PreventUpdate
        print(sessionlogout, user_id, usertype_id, brgy_id)
        return [returnlayout, sessionlogout]
    else: raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050', new = 0, autoraise = True)
    app.run_server(debug = False)