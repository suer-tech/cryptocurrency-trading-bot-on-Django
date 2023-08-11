import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='My Dashboard'),
    dcc.Graph(id='example-graph', figure=fig),
    dcc.Dropdown(
        id='example-dropdown',
        options=[
            {'label': 'Option 1', 'value': 'opt1'},
            {'label': 'Option 2', 'value': 'opt2'}
        ],
        value='opt1'
    ),
    html.Div(id='example-output')
])


