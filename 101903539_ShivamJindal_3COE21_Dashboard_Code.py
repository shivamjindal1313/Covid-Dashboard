#Name: Shivam Jindal
#Roll No: 101903539
#Batch: 3COE21
#Dashboard Code

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import datetime

covid = pd.read_csv("D:/Shivam Coe/TU Sem 5/Data Science/Dashboard/us-counties.csv",parse_dates=True)
covid['date'] = pd.to_datetime(covid['date'])
covid['month'] = covid['date'].dt.month
covid['year'] = covid['date'].dt.year

# creating the Dash app
app = dash.Dash()
Type = ['By Particular Month','By  Particular Year']
month = ['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
year = [2020,2021]

# set up the app layout
app.layout = html.Div(children=[
    html.H1(children='US Countries COVID-19 Visualization'),
    html.Div(children=[
        html.Div(children=[
            html.Label('Select Country'),
            dcc.Dropdown(id='geo-dropdown1',
                    options=[{'label': i, 'value': i}
                            for i in covid['county'].unique()],
                    value='Cook'),
            html.Label('Select month'),
            dcc.Dropdown(id='geo-dropdown3',
                    options=[{'label': i, 'value': i}
                            for i in month],
                    value='Jan')
            ],style={
                'width': '500px',
                'height':'200px',
                'position':'absolute',
                'top':'10%',
                'left':'10%',
                'font-size' : '20px'
                }),
        html.Div(children=[
            html.Label('Visualization Type'),
            dcc.Dropdown(id='geo-dropdown2',
                    options=[{'label': i, 'value': i}
                            for i in Type],
                    value='Jan'),
            html.Label('Select Year'),
            dcc.Dropdown(id='geo-dropdown4',
                    options=[{'label':i, 'value': i}
                            for i in year],
                    value='2020')
                ],style={
                'width': '500px',
                'height':'200px',
                'position':'absolute',
                'top':'10%',
                'left':'15%',
                'margin-left' : '500px',
                'font-size' : '20px'
                })
            ]),
    html.Div(children=[
    dcc.Graph(id='vaccine-graph1'),
    dcc.Graph(id='vaccine-graph2')  
    ],style={
        'margin-top' : '130px'
    }) 
],style={
    'text-align' : 'center'
})

# set up the call function
@app.callback(
    [Output(component_id='vaccine-graph1', component_property='figure'),
    Output(component_id='vaccine-graph2', component_property='figure')],
    [Input(component_id='geo-dropdown1', component_property='value'),
    Input(component_id='geo-dropdown2', component_property='value'),
    Input(component_id='geo-dropdown3', component_property='value'),
    Input(component_id='geo-dropdown4', component_property='value')]
)
def update_graph(selected_state1,selected_state2,selected_state3,selected_state4):
    filtered_state1 = covid[covid['county'] == selected_state1]
    if selected_state2 == 'By Particular Month':
        filtered_state1 = filtered_state1[filtered_state1['month'] == (month.index(selected_state3) + 1)]
        filtered_state1 = filtered_state1[filtered_state1['year'] == selected_state4]
        line_fig = px.bar(filtered_state1,
                           x='date', y='cases',
                           title=f'Covid Cases in {selected_state1}, {selected_state3} {selected_state4}',color_discrete_sequence =['maroon'])
        line_fig.update_layout(title_x=0.5,plot_bgcolor='#97c6e3',paper_bgcolor='#97c6e3')
        line_fig1 = px.bar(filtered_state1,
                           x='date', y='deaths',
                           title=f'Deaths in {selected_state1}, {selected_state3} {selected_state4} ',color_discrete_sequence =['black'])
        line_fig1.update_layout(title_x=0.5,plot_bgcolor='#F2DFCE',paper_bgcolor='#F2DFCE')
    else:
        filtered_state1 = filtered_state1[filtered_state1['year'] == selected_state4]
        line_fig = px.bar(filtered_state1,
                           x='date', y='cases',
                           title=f'Covid Cases in {selected_state1}, {selected_state4}',color_discrete_sequence =['maroon'])
        line_fig.update_layout(title_x=0.5,plot_bgcolor='#97c6e3',paper_bgcolor='#97c6e3')
        line_fig1 = px.bar(filtered_state1,
                           x='date', y='deaths',
                           title=f'Deaths in {selected_state1}, {selected_state4} ',color_discrete_sequence =['black'])
        line_fig1.update_layout(title_x=0.5,plot_bgcolor='#F2DFCE',paper_bgcolor='#F2DFCE')

    return line_fig,line_fig1


if __name__ == '__main__':
    app.run_server(debug=True)