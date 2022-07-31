# import important libraries
from telnetlib import OUTMRK
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from unicodedata import name
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

# Read the data from csv
spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Unique Launch Sites
launchSites = []
for i in spacex_df['Launch Site'].unique():
    launchSites.append(i)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
                                html.H1('SpaceX Launch Records Dashboard'),
                                html.Div(dcc.Dropdown(id='identify-the-dropdown',options=[
                                    {'label': 'All sites', 'value': 'ALL' },
                                    {'label': launchSites[0], 'value': launchSites[0]},
                                    {'label': launchSites[1], 'value': launchSites[1]},
                                    {'label': launchSites[2], 'value': launchSites[2]},
                                    {'label': launchSites[3], 'value': launchSites[3]}], value = 'ALL')),
                                html.Br(),
                                html.Div([ ],id='success-pie-chart'),
                                html.Br(),
                                html.P('Payload Range (Kg):'),
                                dcc.RangeSlider(   id = 'identify-the-slider', 
                                                            min = 0,  max = 10000, step = 1000,
                                                            marks={ 0:'0',
                                                                    2500: '2500',
                                                                    5000: '5000',
                                                                    7500: '7500',
                                                                    10000: '10000'}),
                                html.Div([ ], id='another-graph')
                                ])

# The callback function
@app.callback(  [Output(component_id='success-pie-chart', component_property='children')],
                [Input(component_id='identify-the-dropdown', component_property='value')])

# The Functions

# 
def pie_chart(valueFromDropdown):
    if valueFromDropdown == 'ALL':
        fig = px.pie(   spacex_df,
                        values='class', 
                        names = 'Launch Site', 
                        title='Total Successful Launches By Site')

        return [dcc.Graph(figure=fig)]
    else:
        new_df = spacex_df[spacex_df['Launch Site'] == valueFromDropdown]
        fig = px.pie(new_df, names = 'class', title = f'Total Successful Launches For Site {valueFromDropdown}')
        return [dcc.Graph(figure  = fig)]

@app.callback(  [Output(component_id='another-graph', component_property='children')],
                [Input(component_id='identify-the-dropdown', component_property='value'),
                Input(component_id='identify-the-slider', component_property='value')])

def other_graph(valueFromDropdown,valueFromRangeSlider):
    data_range = spacex_df[
                                (spacex_df['Payload Mass (kg)'] >= valueFromRangeSlider[0]) 
                                & (spacex_df['Payload Mass (kg)'] <= valueFromRangeSlider[1])
                                ]
    if valueFromDropdown == 'ALL':
        scatterPlot = px.scatter(   data_range, 
                                    x = 'Payload Mass (kg)', 
                                    y = 'class', 
                                    color='Booster Version Category', 
                                    title='Correlation between Payload and Succes for all sites')
        return [dcc.Graph(figure = scatterPlot)]
    else:
        dataFrame = spacex_df[spacex_df['Launch Site'] == valueFromDropdown]
        scatterPlot = px.scatter(   dataFrame, 
                                    x='Payload Mass (kg)', 
                                    y= 'class', 
                                    color='Booster Version Category', 
                                    title=f'Correlation between Payload and Success for site {valueFromDropdown}')
        return [dcc.Graph(figure = scatterPlot)]
# Run the app
if __name__ == '__main__':
    app.run_server()