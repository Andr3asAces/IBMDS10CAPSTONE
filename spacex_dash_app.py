# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
file_path   = r"C:\Users\abelegratis\OneDrive - CBI\Data Science\Capstone\data\spacex_launch_dash.csv"
spacex_df   = pd.read_csv(file_path)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sites   = spacex_df['Launch Site'].unique().tolist()
sites

option = [{'label': 'ALL sites', 'value': 'ALL'}]
for site in sites:
    option.append({'label': site, 'value': site})
print(option)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                 
                                html.Div(  dcc.Dropdown(id='site-dropdown',
                                                            options= option,
                                                            value='ALL',
                                                            placeholder="Launch site",
                                                            searchable=True
                                                            ),
                                            ),                               
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
                                    
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Callback decorator
@app.callback( [
               Output(component_id='success-pie-chart', component_property='figure')
               ],
               Input(component_id='site-dropdown', component_property='value'))


def get_pie_chart(entered_site):
    #filtered_df = spacex_df
    if entered_site == 'ALL':
        data = spacex_df.groupby(['Launch Site'])['class'].sum().reset_index()
        fig = px.pie(data, values='class', names='Launch Site', title='By launch site')
        return [fig]
    else:
        data = spacex_df[spacex_df['Launch Site']==entered_site]['class'].value_counts().reset_index()
        data.rename(columns={'index':'class','class':'values'},inplace=True)
        fig = px.pie(data, values='values', names='class', title=f'by {entered_site}')
        return [fig]


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( [
               Output(component_id='success-payload-scatter-chart', component_property='figure')
               ],
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value'),
               ])

def get_payload(entered_site, range_value):
    p_min = range_value[0]
    p_max = range_value[1]
    if entered_site == 'ALL':
        data = spacex_df[spacex_df['Payload Mass (kg)'].between(p_min, p_max, inclusive='both')] [['Payload Mass (kg)','class','Booster Version Category']]
        fig2 = px.scatter(data,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='All sites')#
        return [fig2]
    else:
        condition1 = spacex_df['Launch Site']==entered_site
        condition2 = spacex_df['Payload Mass (kg)'].between(p_min,p_max)
        data = spacex_df[condition1 & condition2][['Payload Mass (kg)','class','Booster Version Category']]
        fig2 = px.scatter(data,x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f'{entered_site}')
        return [fig2]

# Run the app
if __name__ == '__main__':
    app.run_server()


