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

df = pd.read_csv('https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv')
flower_setosa = pd.read_csv(r'C:\\Users\\conse\Documents\\GitHub\super-miniworkshop\data\setosa.csv')
flower_versicolor = pd.read_csv(r'C:\\Users\\conse\Documents\\GitHub\super-miniworkshop\data\\versicolor.csv')
flower_virginica = pd.read_csv(r'C:\\Users\\conse\Documents\\GitHub\super-miniworkshop\data\\virginica.csv')

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
            value=[0, 1, 2],
            marks={
                0: {'label': 'Setosa',  'style': {'color': '#ffffff'}},
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
                id='plot'
            )
        ], style={'margin': '0 auto', 'width': '100%'})
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),
], style={'backgroundColor': colors['background']}
)
#index_vals = df['class'].astype('category').cat.codes

@app.callback([
    Output('graph', 'figure')
    ], [Input('slider', 'value')]
)
def plot(flower):

    flowertype = flower_setosa

    if flower == 0:
        flowertype = flower_setosa
    elif flower == 1:
        flowertype = flower_versicolor
    elif flower == 2:
        flowertype = flower_virginica
    #print(flower)
    
    figure = px.scatter(flowertype, x="sepal.width", y="sepal.length", color="variety",
                 size='petal.length', hover_data=['petal.width'])

    #print(figure)
    return figure

if __name__ == '__main__':
    app.server.run(debug=True)