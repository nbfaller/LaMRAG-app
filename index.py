# Dash related dependencies
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# For opening browser
import webbrowser
# App definition
from app import app
from apps import dashboard, home, commonmodules as cm, error, sandbox, about
from apps.users import users_register, users_search
from apps.reports import reports_create, reports_view, reports_report
from apps.events import events_create, events_event, events_view
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
        dcc.Store(id = 'app_brgy_id', data = 138, storage_type = 'memory'), # CHANGE
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
        State('app_sessionlogout', 'data'),
        State('app_currentuser_id', 'data'),
        State('app_usertype_id', 'data')
    ]
)

def displaypage(pathname, sessionlogout, user_id, usertype_id):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if user_id < 0: # If logged out
                if pathname == '/' or pathname == '/home':
                    returnlayout = home.layout
                elif pathname == '/about' or pathname == '/about-lamrag':
                    returnlayout = about.layout
                elif pathname == '/data/barangays':
                    returnlayout = data_barangays.layout
                elif pathname == '/data/demographics':
                    returnlayout = data_demographics.layout
                else:
                    returnlayout = error.layout
            else:
                if pathname == '/logout':
                    returnlayout = home.layout
                    sessionlogout = True
                elif pathname == '/about' or pathname == '/about-lamrag':
                    returnlayout = about.layout
                elif pathname == '/data/barangays':
                    returnlayout = data_barangays.layout
                elif pathname == '/data/demographics':
                    returnlayout = data_demographics.layout
                elif pathname == '/dashboard':
                    returnlayout = dashboard.layout
                elif pathname == '/users/register':
                    returnlayout = users_register.layout
                elif pathname == '/users/search':
                    returnlayout = users_search.layout
                elif pathname == '/reports' or pathname == '/reports/view':
                    returnlayout = reports_view.layout
                elif pathname == '/reports/create':
                    returnlayout = reports_create.layout
                elif pathname == '/reports/report':
                    returnlayout = reports_report.layout
                elif pathname == '/events' or pathname == '/events/view':
                    returnlayout = events_view.layout
                elif pathname == '/events/create':
                    returnlayout = events_create.layout
                elif pathname == '/events/event':
                    returnlayout = events_event.layout
                elif pathname == '/data/activate':
                    returnlayout = data_activate.layout
                elif pathname == '/data/household/upload':
                    returnlayout = data_household_upload.layout
                elif pathname == '/data/barangay/upload':
                    returnlayout = data_barangay_upload.layout
                # SANDBOX PAGE
                elif pathname == '/sandbox':
                    returnlayout = sandbox.layout
                else:
                    returnlayout = error.layout
            # Decide sessionlogout value
            logout_conditions = [
                pathname in ['/', '/logout'],
                user_id == -1,
                not user_id
            ]
            sessionlogout = any(logout_conditions)

        else: raise PreventUpdate
        print(sessionlogout, user_id, usertype_id)
        return [returnlayout, sessionlogout]
    else: raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050', new = 0, autoraise = True)
    app.run_server(debug = False)