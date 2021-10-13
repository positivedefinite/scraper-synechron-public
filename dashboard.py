import dash
from dash import dcc, dash_table, html

from dash.dependencies import Input, Output, State
#import dash_bootstrap_components as dbc

app = dash.Dash(__name__)
app.scripts.config.serve_locally = True

import pandas as pd
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
df = pd.read_csv('companies_formatted.csv', delimiter=',', error_bad_lines=False)
df = df.drop(columns='Index')
name_column = 'Commercial Name (English)'

app.layout = html.Div([
    html.Div(id='header',
             children='Enter a company name that you would like to search for, or search for an empty field to see all:'),
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a query and press Search'),        
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
])


@app.callback(
    Output('container-button-basic', 'children'), 
    Output('table','data'),
    Output('table','columns'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, query):
    message = f'The input query "{query}" and the button has been clicked {n_clicks} times'
    query = str(query)
    if query=='' or query==None or query=='None':
        print(f'No query: {query}')
        columns=[{"name": i, "id": i} for i in df.columns]
        data=df.to_dict('records')
    else:
        print(f"Query: {query}")
        query =  query.upper()
        matches = df[name_column].str.contains(query)
        data = df[matches].to_dict('records')
        columns = [{"name": i, "id": i} for i in df[matches].columns]
    output = [message, data, columns]
    return output
if __name__ == "__main__":
    app.run_server(port=8053)
