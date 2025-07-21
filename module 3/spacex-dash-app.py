# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

options_list = [
    {'label': 'All Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
]
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id = 'site-dropdown',
                                            options = options_list,
                                            value = 'ALL',
                                            placeholder = 'Select a Launch Site',
                                            searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'),
            Input(component_id = 'site-dropdown', component_property = 'value'))
def get_pie_chart(input_site):
    if input_site == 'ALL':
        chart_data = spacex_df[spacex_df['class'] == 1]
        chart_values = 'class'
        chart_names = 'Launch Site'
        chart_title = 'Total success launches by site'
    else:
        chart_data = spacex_df[spacex_df['Launch Site'] == input_site].groupby('class')['class'].count().reset_index(name = 'count')
        chart_values = 'count'
        chart_names = 'class'
        chart_title = f'Total success launches for site {input_site}'
    
    fig = px.pie(chart_data,
                values = chart_values,
                names = chart_names,
                title = chart_title)
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
            [Input(component_id = 'site-dropdown', component_property = 'value'),
            Input(component_id = "payload-slider", component_property = "value")])
def get_scatter_chart(input_site, input_payload):
    if input_site == 'ALL':
        filtered_spacex_df = spacex_df
        chart_title = 'Correlation between payload and success rate for all sites'
    else:
        filtered_spacex_df = spacex_df[spacex_df['Launch Site'] == input_site]
        chart_title = f'Correlation between payload and success rate for site {input_site}'

    chart_data = filtered_spacex_df[(filtered_spacex_df['Payload Mass (kg)'] >= input_payload[0])
                                    & (filtered_spacex_df['Payload Mass (kg)'] <= input_payload[1])]

    fig = px.scatter(chart_data,
                    x = 'Payload Mass (kg)',
                    y = 'class',
                    color = 'Booster Version Category',
                    title = chart_title)
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
