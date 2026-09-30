from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_draggable

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# external CSS stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,external_stylesheets=external_stylesheets)
# адаптивность диаграмм - встраивание в окно
style_dashboard={
          "height":'100%',
          "width":'100%',
          "display":"flex",
          "flex-direction":"column",
          "flex-grow":"1"
      }

app.layout = html.Div([
    dash_draggable.ResponsiveGridLayout([
    html.Div([html.H1(children='Выбор нескольких графиков и оси у', style={'textAlign':'center'}),
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    dcc.Dropdown(df.country.unique(), value = ['Canada'], id='dropdown-selection', multi=True),
    dcc.Graph(id='graph-content'),
    html.Hr()]),

    html.Div([html.H1(children='Выбор года (кросс-фильтр)', style={'textAlign':'center'}), dcc.Dropdown(df.year.unique(), value = max(df.year.unique()), id='dropdown-selection-year')]),

    html.Div([html.H1(children='Пузырьковая диаграмма с выбором осей и радиуса по мерам', style={'textAlign':'center'}),
    html.Div(['Ось Х', dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap', 'year'], value='lifeExp', id='controls-bubble-x')]),
    html.Div(['Ось Y', dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap', 'year'], value='gdpPercap', id='controls-bubble-y')]),
    html.Div(['Радиус: ', dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='pop', id='controls-bubble-size')]),
    dcc.Graph(id='graph-bubble')]),

    html.Div([html.H1(children='Топ 15 стран по популяции за выбранный год', style={'textAlign':'center'}),
    html.Hr(),
    dcc.Graph(id='top15')]),

    html.Div([html.H1(children='Население на континентах', style={'textAlign':'center'}),
    html.Hr(),
    dcc.Graph(id='continent')])
])])
# График с выбором нескольких
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('controls-and-radio-item', 'value')
)
def update_graph(value, y_select):
    dff = df[df['country'].isin(value)]
    return px.line(dff, x='year', y=y_select, hover_name='country', line_group='country')
# Пузырьковая диаграмма с выбором осей и радиусом
@callback(
    Output('graph-bubble', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('controls-bubble-x', 'value'),
    Input('controls-bubble-y', 'value'),
    Input('controls-bubble-size', 'value'),
    Input('dropdown-selection-year', 'value')

)
def update_bubble(value, x_select, y_select, size, year):
    dff = df[df['country'].isin(value) & (df['year'] >= year)] # >= так как много годов пропущено
    return px.scatter(dff, x=x_select, y=y_select, hover_name='country', size = size)

# Топ 15 по населению
@callback(
    Output('top15', 'figure'),
    Input('dropdown-selection-year', 'value')
)
def top15(year):
  dff = df[df['year'] == year].sort_values('pop', ascending=False).head(15)
  return px.bar(dff, x = 'country', y = 'pop', hover_name='country')

# Круговая диаграмма по континенту
@callback(
    Output('continent', 'figure'),
    Input('dropdown-selection-year', 'value')
)
def continent(year):
  dff = df[df['year'] == year].groupby('continent')['pop'].sum().reset_index()
  return px.pie(dff, values = 'pop', names='continent')


import os

if __name__ == '__main__':
    app.run(debug=True)
else:
    server = app.server
