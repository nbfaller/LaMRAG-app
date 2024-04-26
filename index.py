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
from apps import home, commonmodules as cm, error, sandbox
from apps.users import users_register
from apps.reports import reports_create
from apps.events import events_create
from apps.data import data_barangays

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
        # Store variables for locking location of app
        dcc.Store(id = 'app_region_id', data = 8, storage_type = 'session'),
        dcc.Store(id = 'app_province_id', data = 60, storage_type = 'session'),
        dcc.Store(id = 'app_citymun_id', data = 3, storage_type = 'session'),
        dcc.Store(id = 'app_brgy_id', data = 1, storage_type = 'memory'), # CHANGE
        dcc.Store(id = 'app_census_cols', data = ['name', 2000, 2007, 2010, 2015, 2020], storage_type = 'session'),
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
        Output('page-content', 'children')
    ],
    [
        # Callback is triggered when path changes
        Input('url', 'pathname')
    ]
)

def displaypage(pathname):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if pathname == '/' or pathname == '/home':
                returnlayout = home.layout
            elif pathname == '/users/register':
                returnlayout = users_register.layout
            elif pathname == '/reports/create':
                returnlayout = reports_create.layout
            elif pathname == '/events/create':
                returnlayout = events_create.layout
            elif pathname == '/data/barangays':
                returnlayout = data_barangays.layout
            # SANDBOX PAGE
            elif pathname == '/sandbox':
                returnlayout = sandbox.layout
            else:
                returnlayout = error.layout
            return [returnlayout]
        else: raise PreventUpdate
    else: raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050', new = 0, autoraise = True)
    app.run_server(debug = False)