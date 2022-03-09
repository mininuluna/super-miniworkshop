import os
from random import randint
from sre_parse import State
from typing import Any, Union

import dash
from dash import dcc
from dash import html
import flask
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from pandas import DataFrame
from pandas.io.parsers import TextFileReader

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))

app = dash.Dash(__name__, server=server)

df = pd.read_csv('data/iris.csv', encoding='utf-8')
flower_setosa = pd.read_csv('data/setosa.csv', encoding='utf-8')
flower_versicolor = pd.read_csv('data/versicolor.csv', encoding='utf-8')
flower_virginica = pd.read_csv('data/virginica.csv', encoding='utf-8')

fig = px.scatter(df, x="sepal.width", y="sepal.length", color="variety",
                 size='petal.length', hover_data=['petal.width'])

colors = {'background': '#111111', 'text': '#7FDBFF'}
colors['text']

app.layout = html.Div([
    html.Div(
        children=[
            html.H1('Hello Dash!', style={'textAlign': 'center', 'color': colors['text']}
                    )],
        style={'marginLeft': 10, 'marginRight': 10, 'marginTop': 0, 'marginBottom': 10,
               'backgroundColor': '#F7FBFE',
               'border': 'thin lightgrey dashed'}),
    html.Div([
        # Changed Dropdown Menus to Sliders
        html.H3('Select the Type of Flower:',
                className="app-header--menu"),
        dcc.Slider(
            id='slider',
            min=0,
            max=2,
            step=None,
            value=1,
            marks={
                0: {'label': 'Setosa', 'style': {'color': '#ffffff'}},
                1: {'label': 'Versicolor', 'style': {'color': '#ffffff'}},
                2: {'label': 'Virginica', 'style': {'color': '#ffffff'}},
            },
        ),

        html.Div([
            html.P(style={'textAlign': 'center',
                          'color': colors['text']}),
            dcc.Graph(
                id='main-plot',
                figure=fig
            ),
        ], style={'margin': '0 auto', 'width': '100%'}),
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),
    html.Div([
        html.Div([
            html.P('IMAGE TESTING', style={'textAlign': 'center',
                                           'color': colors['text']}),
            #html.Img(id='image_output',
            #        style={'display': 'block', 'margin-left': 'auto',
            #'margin-right': 'auto', 'max-width': '75%',
            #                'height': '300'})
        ], style={'margin': '0 auto', 'width': '100%'}),
        html.Div([
            html.P('IMAGE DR. PATRICK TESTING', style={'textAlign': 'center',
                                                       'color': colors['text']}),
            html.P(style={'textAlign': 'center',
                          'color': colors['text']}),
            dcc.Graph(
                id='graph',
            )
        ], style={'margin': '0 auto', 'width': '100%'})
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),
], style={'backgroundColor': colors['background']}
)

@app.callback(
    Output('graph', 'figure'),
    Input('slider', 'value')
)
def plot(flower):

    flowertype = flower

    if flowertype == 0:
        return px.scatter(flower_setosa, x="sepal.width", y="sepal.length", color="variety",
                 size='petal.length', hover_data=['petal.width'])

    elif flowertype == 1:
        return px.scatter(flower_versicolor, x="sepal.width", y="sepal.length", color="variety",
                 size='petal.length', hover_data=['petal.width'])
    else:
        return px.scatter(flower_virginica,  x="sepal.width", y="sepal.length", color="variety",
                 size='petal.length', hover_data=['petal.width'])

if __name__ == '__main__':
    app.server.run(debug=True)