######### Import your libraries #######
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *

###### Import a dataframe #######
df = pd.read_pickle('virginia_totals.pkl')
options_list=list(df['jurisdiction'].value_counts().sort_index().index)

image1='https://www.vaco.org/wp-content/uploads/2017/03/VACoRegionMap17.png'
########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='VA 2016'

####### Layout of the app ########
app.layout = html.Div([
    html.H3('2016 Presidential Election: Vote Totals by Jurisdiction'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in options_list],
        value=options_list[0]
    ),
    html.Img(src=image1, style={'width': 'auto', 'height': 'auto'})
    html.Br(),
    dcc.Graph(id='display-value'),
    html.Br(),
    html.A('Code on Github', href='https://github.com/caroleonor/virginia_election_2016/edit/master/app.py'),
    html.Br(),
    html.A('Data Source', href='https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LYWX3D')
])


######### Interactive callbacks go here #########
@app.callback(dash.dependencies.Output('display-value', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def juris_picker(juris_name):
    juris_df=df[df['jurisdiction']==juris_name]

    mydata1 = go.Bar(x=list(juris_df['precinct'].value_counts().index),
                     y=list(juris_df['votes']['Donald Trump']),
                     marker=dict(color='#46E81B'),
                     name='Trump')
    mydata2 = go.Bar(x=list(juris_df['precinct'].value_counts().index),
                     y=list(juris_df['votes']['Hillary Clinton']),
                     marker=dict(color='#1BCCE8'),
                     name='Clinton')
    mydata3 = go.Bar(x=list(juris_df['precinct'].value_counts().index),
                     y=list(juris_df['votes']['Other']),
                     marker=dict(color='#777976'),
                     name='Other')

    mylayout = go.Layout(
        title='Votes by candidate for: {}'.format(juris_name),
        xaxis=dict(title='Precincts'),
        yaxis=dict(title='Number of Votes')
    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
