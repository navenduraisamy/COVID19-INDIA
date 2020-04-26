import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import flask
from dash.dependencies import Output
from dash.dependencies import Input
import plotly
import os
from random import randint

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)
app.title = 'COVID19-DASH'
app.layout = html.Div(
    html.Div([
        html.H1(children='COVID19 TRACKER INDIA',
        style={
            'marginTop':'10px',
            'textAlign':'left',
            'background':'#EAECEE',
            'padding':'25px',
            'color':'#2C3E50',
            'borderRadius':'5px'
        }),
        html.Div([
            html.Div([
                html.H1(id='confirmed'),
                html.P('Confirmed')
            ],className='redbox'),
            html.Div([
                html.H1(id='active'),
                html.P('Active')
            ],className='bluebox'),
            html.Div([
                html.H1(id='recovered'),
                html.P('Recovered')
            ],className='greenbox'),
            html.Div([
                html.H1(id='deaths'),
                html.P('Deceased')
            ],className='blackbox')
        ],className='cases'),

        html.Div([
            html.Div([
                html.H1(id='maxrecovery'),
                html.P('the state with maximum recovery ratio')
            ],className='greenbox'),
            html.Div([
                html.H1(id='maxdeath'),
                html.P('the state  with maximum deceased ratio')
            ],className='redbox')
        ],className='ratioblock'),

        html.Div([dcc.Graph(id='live-update-graph1-scatter'),dcc.Graph(id='live-update-graph2-scatter')],
        style={'marginLeft':"10%","width":"80%",'marginRight':"10%"}),

        html.Div(id='statetable',style={'marginLeft':'20%','paddingTop':'50px','paddingBottom':'40px'}),
        html.Div([
            html.P('State Helpline:     104'),
            html.P('Central Helpline:   1075'),
            html.A('Contact Developer',href='mailto:naven.duraisamy5859@gmail.com')
        ],style={
            'marginTop':'20px',
            'textAlign':'left',
            'background':'#EAECEE',
            'padding':'25px',
            'color':'#2C3E50',
            'borderRadius':'5px',
            'marginBottom':'20px'
        }),
        dcc.Interval(
            id='interval-component',
            interval=1*1000
        )
    ])
)

@app.callback(Output('statetable','children'),[Input('interval-component','interval')])
def datatable(self):
    sheet_id='1nwIYvvH7ILPsH9wpXbiNzsV_-t2YFoiprINpSaQBUHs'
    df_state=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0")
    df_temp=df_state[['state','confirmed','active','recovered','deaths']]
    return dash_table.DataTable(
                columns=[{"name":i,"id":i} for i in df_temp.columns],
                data=df_temp.to_dict("rows"),
                style_table={'maxHeight':'500px','width':'70%','title':'hello'},
                style_cell={
                            'fontFamily':'sans-serif',
                            'textAlign':'center',
                            'border':'2px solid white',
                            'borderCollapse':'collapse'},
                style_header={
                            'color':'#2C3E50',
                            'backgroundColor':'#EAECEE'},
                style_cell_conditional=[{
                'if':{'row_index':'odd'},
                'backgroundColor':'#F4F6F6'}],
                fixed_rows={'headers':True}
                )


@app.callback(Output('confirmed','children'),[Input('interval-component', 'interval')])
def update_confirmed(self):
    sheet_id='1nwIYvvH7ILPsH9wpXbiNzsV_-t2YFoiprINpSaQBUHs'
    df_state=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0")
    con_total=df_state.confirmed.sum()
    return con_total

@app.callback(Output('recovered','children'),[Input('interval-component', 'interval')])
def update_confirmed(self):
    sheet_id='1nwIYvvH7ILPsH9wpXbiNzsV_-t2YFoiprINpSaQBUHs'
    df_state=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0")
    rec_total=df_state.recovered.sum()
    return rec_total

@app.callback(Output('active','children'),[Input('interval-component', 'interval')])
def update_confirmed(self):
    sheet_id='1nwIYvvH7ILPsH9wpXbiNzsV_-t2YFoiprINpSaQBUHs'
    df_state=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0")
    act_total=df_state.active.sum()
    return act_total

@app.callback(Output('deaths','children'),[Input('interval-component', 'interval')])
def update_confirmed(self):
    sheet_id='1nwIYvvH7ILPsH9wpXbiNzsV_-t2YFoiprINpSaQBUHs'
    df_state=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0")    
    dec_total=df_state.deaths.sum()    
    return dec_total

@app.callback(Output('maxrecovery','children'),[Input('interval-component', 'interval')])
def update_confirmed(self):
    sheet_id='1nwIYvvH7ILPsH9wpXbiNzsV_-t2YFoiprINpSaQBUHs'
    df_state=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0")
    max_recovery_ratio=(df_state['recovered']/df_state['confirmed']).max()
    max_recovery_state=df_state.loc[df_state['recovered']/df_state['confirmed']==max_recovery_ratio,'state_name']
    max_recovery_state=list(max_recovery_state)
    return max_recovery_state[0]

@app.callback(Output('maxdeath','children'),[Input('interval-component', 'interval')])
def update_confirmed(self):
    sheet_id='1nwIYvvH7ILPsH9wpXbiNzsV_-t2YFoiprINpSaQBUHs'
    df_state=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0")
    max_death_ratio=(df_state['deaths']/df_state['confirmed']).max()
    max_death_state=df_state.loc[df_state['deaths']/df_state['confirmed']==max_death_ratio,'state_name']
    max_death_state=list(max_death_state) 
    return max_death_state[0]



@app.callback(Output('live-update-graph1-scatter', 'figure'),[Input('interval-component', 'interval')])
def update_graph_scatter(self):
    sheet_id='1nwIYvvH7ILPsH9wpXbiNzsV_-t2YFoiprINpSaQBUHs'
    df_state=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0")
    traces = list()
    traces.append(plotly.graph_objs.Scatter(
        x=df_state.state,
        y=df_state.confirmed,
        name='confirmed',
        mode= 'lines',
        line={'color':'red'},
            ))
    traces.append(plotly.graph_objs.Scatter(
        x=df_state.state,
        y=df_state.recovered,
        name='recovered',
        mode= 'lines',
        line={'color':'#2ECC71'}
            ))
    traces.append(plotly.graph_objs.Scatter(
        x=df_state.state,
        y=df_state.deaths,
        name='deaths',
        mode= 'lines',
        line={'color':'#85929E'}
            ))
    layout=plotly.graph_objs.Layout(hovermode='x unified',title='STATE - TOTAL CASES',xaxis={'title':'State/Union Territory','showgrid':False},)
    return {'data': traces,'layout':layout}

@app.callback(Output('live-update-graph2-scatter', 'figure'),[Input('interval-component', 'interval')])
def update_graph_scatter(self):
    sheet_id='1nwIYvvH7ILPsH9wpXbiNzsV_-t2YFoiprINpSaQBUHs'
    df_ts=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=2096381866")
    traces = list()
    traces.append(plotly.graph_objs.Scatter(
        x=df_ts.date,
        y=df_ts.totalConfirmed,
        name='confirmed',
        mode= 'lines',
        line={'color':'red'},
            ))
    traces.append(plotly.graph_objs.Scatter(
        x=df_ts.date,
        y=df_ts.totalRecovered,
        name='recovered',
        mode= 'lines',
        line={'color':'#2ECC71'}
            ))
    traces.append(plotly.graph_objs.Scatter(
        x=df_ts.date,
        y=df_ts.totalDeceased,
        name='deaths',
        mode= 'lines',
        line={'color':'#85929E'}
            ))
    layout=plotly.graph_objs.Layout(hovermode='x unified',title='CUMULATIVE CASES BY DATE',xaxis={'showgrid':False})
    return {'data': traces,'layout':layout}


if __name__=='__main__':
    app.run_server(threaded=True)
