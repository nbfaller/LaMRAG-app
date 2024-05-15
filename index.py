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
from apps import dashboard, home, commonmodules as cm, error, sandbox
from apps.users import users_register
from apps.reports import reports_create
from apps.events import events_create
from apps.data import data_barangays, data_enable

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
        html.Div(id = 'page-content', style = CONTENT_STYLE),
        # Footer
        cm.footer
    ]
)

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
                else:
                    returnlayout = error.layout
            else:
                if pathname == '/logout':
                    returnlayout = home.layout
                    sessionlogout = True
                elif pathname == '/dashboard':
                    returnlayout = dashboard.layout
                elif pathname == '/users/register':
                    returnlayout = users_register.layout
                elif pathname == '/reports/create':
                    returnlayout = reports_create.layout
                elif pathname == '/events/create':
                    returnlayout = events_create.layout
                elif pathname == '/data/barangays':
                    returnlayout = data_barangays.layout
                elif pathname == '/data/enable':
                    returnlayout = data_enable.layout
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
    app.run(debug = False)