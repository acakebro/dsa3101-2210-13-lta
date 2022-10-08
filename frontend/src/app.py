'''
 # @ Create Time: 2022-10-08 23:39:32.168931
'''

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = Dash(__name__, title="frontend")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

traffic_incidents = pd.read_csv("traffic_incidents.csv")
traffic_speedbands = pd.read_csv("traffic_speedbands.csv")
traffic_images = pd.read_csv("traffic_images.csv")


fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

d_table = dash_table.DataTable(
            data=traffic_incidents.to_dict('records'),
            columns = [{"name": i, "id": i} for i in traffic_incidents.columns[:len(traffic_incidents.columns)-1]],
            cell_selectable=False,
            sort_action='native',
            filter_action='native',
            page_action = 'native',
            page_current = 0,
            page_size = 10
            )

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    html.Div(children = [html.H2("Traffic Incidents"),
                         d_table],
             style = {'width':'1000px', 'height':'350px', 'margin':'10px auto', 'padding-right':'30px'})
    
])



if __name__ == '__main__':
    app.run_server(debug=True)

