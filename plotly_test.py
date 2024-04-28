from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

import pandas as pd

## hi pookie 

planets = pd.read_csv("./planetary_systems.csv", skiprows=90)
planets.dropna(inplace=True)
planets.reset_index(inplace=True)
planets.drop("index", axis=1, inplace=True)
planets.iloc[:-54]

external_stylesheets = ['dashboard.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children='Planets 🪐', className="nunito", style={"textAlign": "center", "color": "black", "fontFamily": "Nunito"}),
    dcc.Dropdown(planets.discoverymethod.unique(), 'Transit', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)

def update_graph(value):
    dff = planets[planets.discoverymethod == value]
    df_grouped = dff.groupby('disc_year').size().reset_index(name='count')
    return px.line(df_grouped, x='disc_year', y='count', title=f'Number of Planets Discovered per Year (by {value} method)')

if __name__ == '__main__':
    app.run(debug=True)