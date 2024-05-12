import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import logging

# Create the application object (stored in app variable) along with CSS stylesheets
app = dash.Dash(
    __name__,
    assets_folder = 'static',
    assets_url_path = 'static',
    include_assets_files = True,
    external_stylesheets = [
        "static/bootstrap.css",
        "static/dcc.css",
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
    ]
)

# Make sure that the allbacks are not activated when input elements enter the layout
app.config.suppress_callback_exceptions = True
# Get CSS from a local folder
app.css.config.serve_locally = True
# Enables your app to run offline
app.scripts.config.serve_locally = True
# Set app title that appears in your browser tab
app.title = "LáMRAG • Local Management Platform for Risk Analytics & Governance"
# These two lines reduce the logs on your terminal so you
# could debug better when you encounter errors in the app.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)