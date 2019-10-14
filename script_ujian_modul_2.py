import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from src.view import showDataFrame, showBarGraph
from dash.dependencies import Input, Output, State


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWlwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

dfTSA = pd.read_csv('tsa_claims_dashboard_ujian.csv')


def addAllOption():
    listoptions = [{'label' : i, 'value' : i} for i in dfTSA['Claim Site'].unique()]
    listoptions.append({'label' : 'All', 'value' : 'All'})
    return listoptions

app.layout = html.Div(children=[
    ## Judul
    html.H1('Ujian Modul 2 Dashboard TSA'),
    ## Nama
    html.P('Created by Fandri'),
    ## Tabs
    dcc.Tabs(value = 'tabs', id = 'tabs-1',children = [
        dcc.Tab(label= 'DataFrame Table', value = 'tab-nol', children = [
            html.H1('DATAFRAME TSA', style = {'text-align' : 'center'}),
            html.P('Claim Site : ', className = 'col-3'),
            ## Add dropdown menu
            html.Div(children = [dcc.Dropdown(id = 'table-dropdown',
                options = addAllOption(),
                    value = 'All')], className = 'col-3'),

            html.P('Max Rows : ', className = 'col-3'),
        
            ## Add input bar
            html.Div(dcc.Input(id='number-row', value=10, type='number'),className = 'col-3'),

            ## Add search button
            html.Div(html.Button('Search', id = 'search'), style = {'padding' : '15px'}),

            ## Show DataFrame
            html.Div(children = showDataFrame(dfTSA))
            ]),
        
        ## Tab 1 Bar Chart
        dcc.Tab(label = 'Bar-Chart', value = 'tab-satu', children = [
            ## Masukkan label dropdown
            html.Div(children = [
                html.P('Y1 : ', className = 'col-3'),
                html.P('Y2 : ', className = 'col-3'),
                html.P('X : ', className = 'col-3')],className = 'row'),
            ## Masukkan opsi dropdown
            html.Div(children = [
                html.Div(children = [
                dcc.Dropdown(id = 'x-axis-1',
                options = [{'label' : i, 'value' : i} for i in dfTSA.select_dtypes('number').columns],
                        value = 'Claim Amount')
                ], className = 'col-3'),
                html.Div(children = [
                dcc.Dropdown(id = 'x-axis-2',
                options = [{'label' : i, 'value' : i} for i in dfTSA.select_dtypes('number').columns],
                        value = 'Close Amount')
                ], className = 'col-3'),
                html.Div(children = [
                dcc.Dropdown(id = 'x-axis-3',
                options = [{'label' : i, 'value' : i} for i in ['Claim Type','Claim Site','Disposition']],
                        value = 'Claim Type')
                ], className = 'col-3'),
            ], className = 'row'),

            ## Masukkan Bar Graph
            html.Div(children = showBarGraph(dfTSA), className = 'col-12')

        ]),

        dcc.Tab(label = 'Scatter-Chart', value = 'tab-dua', children = [
            html.Div(children = dcc.Graph(
                id='graph-scatter',
                figure={
                'data': [go.Scatter(
                            x = dfTSA[dfTSA['Claim Type'] == i]['Claim Amount'],
                            y = dfTSA[dfTSA['Claim Type'] == i]['Close Amount'],
                            text = dfTSA[dfTSA['Claim Type'] == i]['Disposition'],
                            mode = 'markers',
                            name = i
                        ) for i in dfTSA['Claim Type'].unique()
                    ],
                'layout': go.Layout(
                    xaxis = {'title': 'Claim Amount'},
                    yaxis = {'title': 'Close Amount'},
                    hovermode = 'closest'
                )
            }
            ), className = 'col-12')

        ]),

        dcc.Tab(label = 'Pie-Chart', value = 'tab-tiga', children = [
            ## Masukkan label dropdown
            html.Div(children = [
                html.P('X1 : ', className = 'col-3')]),
            ## Masukkan opsi dropdown
            html.Div(children = [
                html.Div(children = [
                dcc.Dropdown(id = 'pie-input',
                options = [{'label' : i, 'value' : i} for i in dfTSA.select_dtypes('number').columns],
                        value = 'Claim Amount')
                ], className = 'col-3'),
            ]),
            html.Div(children = dcc.Graph(
                id='pie-chart',
                figure={
                'data': [go.Pie(labels = dfTSA['Claim Type'].unique(),
                                        values = dfTSA.groupby('Claim Type').mean()['Claim Amount'],
                                        sort = False

                        )
                    ],
                'layout': {'title': 'Mean Pie Chart'}
            }
            ),
             className = 'col-12')
             
        ])
        ], 
    ## Tabs Contet Style
    content_style = {
        'fontFamily' : 'Arial',
        'borderBottom' : '1px solid #d6d6d6',
        'borderLeft' : '1px solid #d6d6d6',
        'borderRight' : '1px solid #d6d6d6',
        'padding' : '44px'
    })

],
## All Style
style = {
    'maxWidth': '1100px',
    'margin' : '0 auto'
}
)

@app.callback(
    Output(component_id = 'example-graph', component_property = 'figure'),
    [Input(component_id = 'x-axis-1', component_property = 'value'),
    Input(component_id = 'x-axis-2', component_property = 'value'),
    Input(component_id = 'x-axis-3', component_property = 'value')]
)

def create_bar_graph(x1,x2,x3):
    figure = {
                'data': [
                    {'x': dfTSA[x3].unique(), 'y': dfTSA.groupby(x3).mean()[x1], 'type': 'bar', 'name': x1},
                    {'x': dfTSA[x3].unique(), 'y': dfTSA.groupby(x3).mean()[x2], 'type': 'bar', 'name': x2},
                    
                ],
                'layout': {'title': 'Dashboard TSA'}
            }
    return figure

@app.callback(
    Output(component_id = 'pie-chart', component_property = 'figure'),
    [Input(component_id = 'pie-input', component_property = 'value')],
)

def create_pie_chart(x1):
    figure = {
                'data': [go.Pie(labels = [i for i in dfTSA['Claim Type'].unique()],
                                        values = [dfTSA.groupby('Claim Type').mean()[x1][i] for i in list(dfTSA['Claim Type'].unique())],
                                        sort = False

                        )
                    ],
                'layout': {'title': 'Mean Pie Chart'}
            }       
    return figure


@app.callback(
    [Output(component_id = 'table', component_property = 'data'),
    Output(component_id = 'table', component_property = 'page_size')],
    [Input(component_id = 'search', component_property = 'n_clicks')],
    [State(component_id = 'table-dropdown', component_property = 'value'),
    State(component_id = 'number-row', component_property = 'value')]
)

def create_table(n_clicks, x1, x2):
    if x1 == 'All':
        data = dfTSA.to_dict('records')
        page_size = x2
        # return data, page_size
    else : 
        data = dfTSA[dfTSA['Claim Site'] == x1].to_dict('records')
        page_size = x2
    return data, page_size


if __name__ == '__main__':
    app.run_server(debug = True)
