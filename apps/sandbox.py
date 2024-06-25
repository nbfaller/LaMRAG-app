# Dash related dependencies
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# Sandbox imports
import base64
import os
from werkzeug.utils import secure_filename
# App definition
from app import app
from apps import dbconnect as db
from utilities.utils import MarginSettings, CardStyle, RequiredTag, DropdownDataLoader, FormFieldConstructor

input_brgy_id = FormFieldConstructor(
    id_prefix = 'sbox',
    id_actual = 'brgy_id',
    input_type = dcc.Dropdown,
    label_war = "Barangay",
    label_en = "Barangay",
    required = True,
    form_text_war = "Kun opisyal ka san barangay, awtomatiko nga pipilion dinhi an imo barangay.",
    form_text_en = "If you are a barangay official, your barangay will be automatically selected."
)

input_docu = FormFieldConstructor(
    id_prefix = 'sbox',
    id_actual = 'docu',
    input_type = dcc.Upload,
)

UPLOAD_DIRECTORY = 'static/uploads/'

if not os.path.exists(UPLOAD_DIRECTORY): os.makedirs(UPLOAD_DIRECTORY)

layout = html.Div(
    [
        dcc.Store(id = 'sandbox_event_id', data = 1),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Form(
                            [
                                # Common information
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.H1(
                                                    "File a report",
                                                    id = 'sbox_h1_header'
                                                ),
                                                html.P(
                                                    [
                                                        "Kinihanglan pun-on an mga patlang nga may pula nga asterisk ", RequiredTag.tag, ".",
                                                        html.Br(),
                                                        html.Small(
                                                            ["(Fields with red asterisks ", RequiredTag.tag, " are required.)"],
                                                            className = 'text-muted'
                                                        )
                                                    ], className = MarginSettings.paragraph
                                                )
                                            ],
                                            id = 'sbox_row_header',
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dcc.Upload(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        html.H3(
                                                                            html.I(className = 'bi bi-file-earmark-plus'),
                                                                        ),
                                                                        html.P(
                                                                            [
                                                                                'Pagdanas ug hulog file dinhi o ',
                                                                                html.A('pindot para ka makapili file nga isusumite.'),
                                                                                html.Br(),
                                                                                html.Small(
                                                                                    [
                                                                                        'Drag and drop a file or ', html.A('click here to select files for upload.')
                                                                                    ],
                                                                                    className = 'text-muted'
                                                                                )
                                                                            ],
                                                                            className = MarginSettings.paragraph
                                                                        ),
                                                                    ],
                                                                )
                                                            ],
                                                            id = 'sbox_upl_docu',
                                                            # Allow multiple files to be uploaded
                                                            multiple = True,
                                                            className = 'Upload text-center'
                                                        ),
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Div(
                                                            id = 'sbox_div_docu',
                                                        )
                                                    ]
                                                )
                                            ],
                                            class_name = MarginSettings.row
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    class_name = 'col-md-10'
                )
            ],
            class_name = 'justify-content-center'
        )
    ]
)

sandbox_url = '/sandbox'

@app.callback(
    [
        Output('sbox_upl_docu', 'children'),
        Output('sbox_upl_docu', 'className'),
    ],
    [
        Input('sbox_upl_docu', 'contents'),
    ],
    [
        State('sbox_upl_docu', 'filename'),
        State('sbox_upl_docu', 'last_modified')
    ]
)

def sbox_displayuploads(contents, names, dates):
    if contents is not None:
        children = [
            #names,
            #sbox_savefile(name, content) for name, content in zip(names, contents)
        ]
        # Mapping of file extensions to Bootstrap icons
        icon_mapping = {
            '.pdf': 'bi bi-file-earmark-pdf-fill',
            '.docx': 'bi bi-file-earmark-word-fill',
            '.doc': 'bi bi-file-earmark-word-fill',
            '.xlsx': 'bi bi-file-earmark-excel-fill',
            '.xls': 'bi bi-file-earmark-excel-fill',
            '.csv': 'bi bi-file-earmark-spreadsheet-fill',
            '.pptx': 'bi bi-file-earmark-ppt-fill',
            '.ppt': 'bi bi-file-earmark-ppt-fill',
            '.txt': 'bi bi-file-earmark-text-fill',
            '.zip': 'bi bi-file-earmark-zip-fill',
            '.rar': 'bi bi-file-earmark-zip-fill',
            '.jpg': 'bi bi-file-earmark-image-fill',
            '.png': 'bi bi-file-earmark-image-fill',
            '.gif': 'bi bi-file-earmark-image-fill',
            '.mp4': 'bi bi-file-earmark-play-fill',
            '.mp3': 'bi bi-file-earmark-music-fill',
            '.wav': 'bi bi-file-earmark-music-fill',
            '.flac': 'bi bi-file-earmark-music-fill',
            '.ogg': 'bi bi-file-earmark-music-fill',
        }
        default_icon = 'bi bi-box-fill'
        for name in names:
            _, ext = os.path.splitext(name)
            # Get the icon class from the mapping or use the default
            icon_class = icon_mapping.get(ext, default_icon)
            children.append(html.Li([html.I(className = icon_class + ' me-2'), name]))
        return [children, 'Upload text-start']
    else: raise PreventUpdate

def sbox_savefile(name, content):
    # Filename sanitization
    secure_name = secure_filename(name)

    # Ensure the filename does not result in path traversal
    final_path = os.path.realpath(os.path.join(UPLOAD_DIRECTORY, secure_name))
    upload_dir_realpath = os.path.realpath(UPLOAD_DIRECTORY)
    if not final_path.startswith(upload_dir_realpath):
        raise ValueError("Attempted directory traversal in file upload.")
    
    # Decode the content and save the file
    data = content.encode("utf8").split(b";base64,")[1]
    with open(final_path, "wb") as fp:
        fp.write(base64.decodebytes(data))
    
    return html.Div(f'{secure_name} has been uploaded.')