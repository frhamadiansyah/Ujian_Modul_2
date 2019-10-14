import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


def showDataFrame(data):
    tab = dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in data.columns],
                data=data.to_dict('records'),
                page_action = 'native',
                page_current = 0,
                page_size = 10,
                style_table = {'overflowX' : 'scroll'}
            )

    return tab

def showBarGraph(data):
    tab = dcc.Graph(
                id='example-graph',
                figure={
                'data': [
                    {'x': data['Claim Type'].unique(), 'y': data.groupby('Claim Type').mean()['Claim Amount'], 'type': 'bar', 'name': 'Claim Amount'},
                    {'x': data['Claim Type'].unique(), 'y': data.groupby('Claim Type').mean()['Close Amount'], 'type': 'bar', 'name': 'Close Amount'},
                    
                ],
                'layout': {'title': 'Dashboard TSA'}
            }
            )
    return tab