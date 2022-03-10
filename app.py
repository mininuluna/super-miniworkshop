import os
from random import randint

import dash 
from dash import dcc
from dash import html

import flask
import pandas as pd

import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

#To run the flask application
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))

#To run the application within Dash from Plotly
app = dash.Dash(__name__, server=server)

#Reading the csv file to be used
df = pd.read_csv('data/iris.csv', encoding='utf-8')

#Reading more csv files to be used, but for each type of flower
flower_setosa = pd.read_csv('data/setosa.csv', encoding='utf-8')
flower_versicolor = pd.read_csv('data/versicolor.csv', encoding='utf-8')
flower_virginica = pd.read_csv('data/virginica.csv', encoding='utf-8')

#Declaring each variable with the image source path from the internet for each type of Flower
setosa_pic = 'https://64.media.tumblr.com/cf75c154fc10358140397aec64aa643c/d9c7afeefef484e3-70/s2048x3072/4b528d3565ab3a89ffabf202d618cf1982ed1f68.jpg'
versicolor_pic = 'https://64.media.tumblr.com/7e7735db0afd9982f6dd0dd3872d18b2/tumblr_orki97Hid31uvqn0ko1_1280.jpg'
virginica_pic = 'https://64.media.tumblr.com/2cc0b486dce284aa1310349ca5d3a6bc/eac71ab1809a717b-3e/s2048x3072/e0d19ef89609cddd2a3198da45ce2222625d7791.jpg'


fig = px.scatter(df, x="sepal.width", y="sepal.length", color="variety",
                 size='petal.length', hover_data=['petal.width'], template='plotly_white')

fig3D = go.Figure(data=go.Scatter3d(
    x=df['sepal.width'],
    y=df['sepal.length'],
    z=df['petal.length'],
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

fig3D.update_layout(scene = dict(
                    xaxis_title='Sepal Width',
                    yaxis_title='Sepal Length',
                    zaxis_title='Petal Length'),
                    width=250,
                    margin=dict(r=10, b=10, l=10, t=10))

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
    #html.Div([
        #html.Div([
            #html.H3('Scatter Graph to Visualize Loading of All Flowers',
            #    style={'textAlign': 'center', 'color': colors['text']}),
            #dcc.Graph(
            #    id='another-plot',
            #    figure=pca_Figure)
            #], style={'margin': '0 auto', 'width': 750, 'height': 250}),
    #], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),
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

    nameFlower = "Setosa"

    if flowertype == 0:
        prettyFlower = flower_setosa
        nameFlower = "Setosa"

    elif flowertype == 1:
        prettyFlower = flower_versicolor
        nameFlower = "Versicolor"

    else:
        prettyFlower = flower_virginica
        nameFlower = "Virginica"

    return px.scatter(prettyFlower, x="sepal.width", y="sepal.length", color='petal.width',
                 size='petal.length', hover_data=['variety'], template='plotly_white', title=nameFlower)

if __name__ == '__main__':
    app.server.run(debug=True)