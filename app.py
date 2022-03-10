import os
from random import randint
from sre_parse import State
from typing import Any, Union

import dash
from dash import dcc
from dash import html
import flask
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
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

setosa_pic = 'https://64.media.tumblr.com/cf75c154fc10358140397aec64aa643c/d9c7afeefef484e3-70/s2048x3072/4b528d3565ab3a89ffabf202d618cf1982ed1f68.jpg'
versicolor_pic = 'https://64.media.tumblr.com/7e7735db0afd9982f6dd0dd3872d18b2/tumblr_orki97Hid31uvqn0ko1_1280.jpg'
virginica_pic = 'https://64.media.tumblr.com/2cc0b486dce284aa1310349ca5d3a6bc/eac71ab1809a717b-3e/s2048x3072/e0d19ef89609cddd2a3198da45ce2222625d7791.jpg'

fig = px.scatter(df, x="sepal.width", y="sepal.length", color="variety",
                 size='petal.length', hover_data=['petal.width'], template='plotly_white')

fig3D = go.Figure(data=go.Scatter3d(
    x=df['sepal.width'],
    y=df['sepal.length'],
    z=df['petal.length'],
    text=df['variety'],
    mode='markers',
    marker=dict(
        sizemode='diameter',
        sizeref=0.25,
        size=df['petal.length'],
        color = df['petal.width'],
        colorscale = 'Viridis',
        colorbar_title = 'Petal<br>Width',
        line_color='rgb(140, 140, 170)'
    )
))

iris_features = ['sepal.length', 'sepal.width', 'petal.length', 'petal.width']
X_iris = df[iris_features]

pca_var = PCA(n_components=2)
components = pca_var.fit_transform(X_iris)

loadings_iris = pca_var.components_.T * np.sqrt(pca_var.explained_variance_)

pca_Figure = px.scatter(components, x = 0, y = 1, color = df[iris_features])

for i, feature in enumerate(iris_features):
    fig.add_shape(
        type='triangle',
        x0=0, y0=0,
        x1=loadings_iris[i, 0],
        y1=loadings_iris[i, 1]
    )
    fig.add_annotation(
        x=loadings_iris[i, 0],
        y=loadings_iris[i, 1],
        ax=0, ay=0,
        xanchor="center",
        yanchor="bottom",
        text=feature,
    )

colors = {'background': '#394551', 'text': '#7FDBFF'}
colors['text']

app.layout = html.Div([
    html.Div(
        children=[
            html.H1('Hello Pretty Flowers!', style={'textAlign': 'center', 'color': '#02075d'}
                    )],
        style={'marginLeft': 10, 'marginRight': 10, 'marginTop': 0, 'marginBottom': 10,
               'backgroundColor': '#F7FBFE',
               'border': 'thin lightgrey dashed'}),
        # Changed Dropdown Menus to Sliders
        html.H3('Select the Type of Flower:',
                style={'textAlign': 'center', 'color': colors['text']}),
    html.Div(
        dcc.Slider(
            id='slider',
            min=0,
            max=2,
            step=None,
            value=1,
            marks={
                0: {'label': 'Setosa', 'style': {'color': colors['text']}},
                1: {'label': 'Versicolor', 'style': {'color': colors['text']}},
                2: {'label': 'Virginica', 'style': {'color': colors['text']}},
            },
            included=False
        )
    ),
    html.Div([
        html.Div([
            html.H3('Scatter Graph of All the Types of Flowers',
                style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Graph(
                id='main-plot',
                figure=fig),
            html.H3('3D Bubble Scatter Graph of All the Types of Flowers',
                style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Graph(
                id='secondary-plot',
                figure=fig3D)
            ], style={'margin': '0 auto', 'width': 750, 'height': 250}),
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),
    html.Div([
        html.Div([
            html.H3('Flower Image', style={'textAlign': 'center', 'color': colors['text']}),
            html.Img(id='image_output',
                    style={'display': 'block', 'margin-left': 'auto',
            'margin-right': 'auto', 'max-width': 500,
                            'height': 450})
        ], style={'margin': '0 auto', 'width': '100%'}),
        html.Div([
            html.H3('Type of Flower Scatter Graph', style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Graph(
                id='graph',
            )
        ],  style={'margin': '0 auto', 'width': 750, 'height': 550}),
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),
    html.Div([
        html.Div([
            html.H3('Scatter Graph to Visualize Loading of All Flowers',
                style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Graph(
                id='another-plot',
                figure=pca_Figure)
            ], style={'margin': '0 auto', 'width': 750, 'height': 250}),
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),
], style={'backgroundColor': colors['background']}
)

@app.callback(
   Output('image_output', 'src'),
    Input('slider', 'value')
)
def plot(flower):

    flowertype = flower

    if flowertype == 0:
        return setosa_pic

    elif flowertype == 1:
        return versicolor_pic

    else:
        return virginica_pic

@app.callback(
    Output('graph', 'figure'),
    Input('slider', 'value')
)
def plot(flower):

    flowertype = flower

    prettyFlower = flower_setosa

    if flowertype == 0:
        prettyFlower = flower_setosa

    elif flowertype == 1:
        prettyFlower = flower_versicolor

    else:
        prettyFlower = flower_virginica

    return px.scatter(prettyFlower, x="sepal.width", y="sepal.length", color='petal.width',
                 size='petal.length', hover_data=['variety'], template='plotly_white')

if __name__ == '__main__':
    app.server.run(debug=True)