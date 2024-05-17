import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from utils import load_and_clean_data, pre_process_planets
from flask import Flask

df = load_and_clean_data("./planetary_systems.csv")

server = Flask(__name__)

external_stylesheets = ['dashboard.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

app.layout = html.Div(
    style={
        'backgroundColor': '#000000',
        'padding': 10,
        'color': '#ffffff',
        'fontFamily': 'Helvetica'
    },
    children=[
        html.Div(
            className='header',
            children=[
                html.H2("EXOPLANET EXPLORATION", style={'textAlign': 'center', 'fontWeight': 200})
            ]
        ),

        # Planet dropdown.
        html.Div(
            style={'marginLeft': '53px', 'marginTop': '0px', 'width': '88.75vw'},
            children=[
                dcc.Dropdown(
                    id='planet-dropdown',
                    options=[{'label': planet_name, 'value': planet_name} for planet_name in df['pl_name']],
                    placeholder="Select a planet...",
                    style={'color': '#1e1e1e'}
                ),
            ]
        ),

        # Attribute checklist.
        html.Div(
            style={'marginLeft': '53px'},
            children=[
                html.H2(
                    "Select Attributes to Display:",
                    style={'textAlign': 'left', 'fontWeight': 300}
                ),
                dbc.Checklist(
                    id='attribute-checklist',
                    options=[{"label": attribute, "value": attribute} for attribute in df.columns[1:]],
                    value=["pl_name", "hostname"],
                    input_checked_style={
                        'border-radius': '10px',
                        'accent-color': 'rgba(65,79,142, 0.5)'
                    },
                    style={
                        'columnCount': 4,
                        'backgroundColor': '#191925',
                        'padding': '15px',
                        'border-radius': '10px',
                        'width': '88.75vw'
                    },
                )
            ]
        ),

        # Display selected attributes.
        html.Div(
            style={'marginLeft': '51px', 'width': '88.8vw'},
            children=[
                html.H2("Viewing Board", style={'textAlign': 'left', 'fontWeight': 300, 'marginBottom': '0px'}),
                html.Div(id='attribute-display', style={'marginTop': '10px', 'marginBottom': '30px', 'backgroundColor': '#191925', 'padding': '15px', 'border-radius': '10px'})
            ]
        ),

        # Surface view plug-in.
        html.Div(
            id='iframe-container',
            style={'marginLeft': '51px', 'width': '88.8vw'}
        ),

        # Footer.
        html.Div(
            style={'marginLeft': '51px', 'width': '88.8vw', 'fontSize': '15px'},
            children=[
                html.P([
                    "Data sourced from the ",
                    html.A(
                        "NASA Exoplanet Archive",
                        href="https://exoplanetarchive.ipac.caltech.edu/",
                        target="_blank",
                        style={'color': '#c8d0f2', 'textDecoration': 'underline'}
                    ),
                    ". Will be adding support for planet similarity scores and star classification soon! ✨"
                ])
            ]
        ),

    ]
)

# Callback to update the iframe based on selected planet
@app.callback(
    Output('iframe-container', 'children'),
    [Input('planet-dropdown', 'value')],
    [State('attribute-checklist', 'value')]
)
def update_iframe(selected_planet, selected_attributes):
    if selected_planet:
        src = f"https://eyes.nasa.gov/apps/exo/#/planet/{pre_process_planets(selected_planet)}"
        # print(src)
        return html.Iframe(src=src, title="", className="smd-iframe-iframe margin-left-auto margin-right-auto border-0", allow="fullscreen", style={'width': '88.75vw', 'height': '550px'})
    else:
        return html.Div()

# Callback to update displayed attributes based on selected planet and attributes
@app.callback(
    Output('attribute-display', 'children'),
    [Input('planet-dropdown', 'value'),
     Input('attribute-checklist', 'value')]
)
def update_displayed_attributes(selected_planet, selected_attributes):
    if selected_planet is None or not selected_attributes:
        return html.Div("Nothing to see here yet! Please select some attributes.")

    planet_data = df[df['pl_name'] == selected_planet]

    selected_data = planet_data[selected_attributes]

    table = html.Table([
        html.Tr([html.Th(col) for col in selected_data.columns]),
        *[
            html.Tr([html.Td(selected_data.iloc[i][col]) for col in selected_data.columns])
            for i in range(len(selected_data))
        ]
    ])

    return table

if __name__ == '__main__':
    app.run_server(debug=True)
