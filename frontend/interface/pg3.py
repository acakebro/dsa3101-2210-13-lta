import dash
from datetime import datetime, date,timedelta
from time import localtime, strftime
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash import Dash, html, dcc

d_exp_cam = {
        'KPE': ['1001', '1002', '1003', '1004', '1005', '1006', '7793','7794', '7795'],
        'ECP': ['1001', '1002', '1003', '1004', '1005', '1006', '1501', '1503', '1505', '7791'],
        'KJE': ['2708', '6714'],
        'SLE': ['1701', '1702', '1703', '1704', '1705', '1706', '1707', '1709','1711', '7791', '7793', '7795', '7796', '7797'],
        'MCE': ['1501', '1502', '1503', '1504', '1505', '4704'],
        'CTE': ['1705', '4704', '7797', '7798'], 
        'TPE': ['1001', '1003', '1005', '1006', '7798', '9701', '9702', '9703', '9704', '9705', '9706'], 
        'BKE': ['2702', '7798', '8701', '8702', '8704', '8706', '9701', '9702','9703', '9704', '9705', '9706'], 
        'PIE': ['1002', '1003', '1004', '1703', '2703', '2705', '2706', '2707','2708', '7791', '7793', '7794', 
                '7795', '7796', '7797', '8701','8702', '8704', '8706', '9703'],  
        'AYE': ['1502', '1503', '1504', '1703', '1704', '1706', '1707', '3795','3796', '4713', '6716'],
        'Woodlands Causeway/Johor': ['2701', '2702', '2703', '2704', '2705','2706', '2707', '2708', '9703'], 
        'Tuas/Johor': ['1002', '1004', '1703', '4703', '4707', '4712', '4713','6708', '6715', ],
        'Changi': ['1001', '1002', '1003', '1703', '2703', '3704', '3793', '3796','3797', '3798', '4702', '5794', '5795', '5797',
                   '5798', '5799','6701', '6703', '6704', '6705', '6706', '6708', '6710', '6712','6713', '6714', '6715', '6716'],
        'City': ['1001', '1701', '1702', '1709', '1711', '3702', '3704', '3705','3793', '3795', '3796', 
                 '3797','3798', '4701', '4705', '4707','4708', '4709', '4710', '4712', '4716', '6711'],
        'Moulmein': ['1701'],
        'Yio Chu Kang': ['1706'],
        'Jalan Bukit Merah': ['1707'],
        'Jurong' : ['2703', '4701', '4702', '4705', '4706', '4709', '4710', '4714','4716', '5794', '5795', '5797', 
                    '5798', '5799', '6701', '6703','6704', '6705', '6706', '6710', '6711', '6712', '6713'],
        'Airport' : ['3702', '3705', '6711'],
        'Xilin Ave': ['3705'],
        'Marine Parade': ['3795'],
        'Telok Blangah': ['4798', '4799'],
        'Sentosa': ['4799'],
        'Toa Payoh': ['6701'],
        'Thomson': ['6703'],
        'Pasir Ris Dr 12': ['7793'],
        'Punggol/Sengkang': ['7796'],
        'Choa Chu Kang': ['8701', '8704'],
        'Woodlands Ave 2': ['9705']
             }

def road_options(cam):
    options=[]
    for road in d_exp_cam.keys():
        options+=[{'label':str(road), 'value':str(road)}]
    return options

layout = html.Div(
    children=[
    html.Br(),
    html.Br(),
    html.H4("Prediction of traffic condition in 2 months", style={'align-items':'center'}),
    html.H5("Please choose the camera, road, day, and time you would like to view."),
    html.Br(),
        
    html.Div(
        # Road dropdown
        children = [
        html.H6('Select road', style={'font-weight': 'bold'}),
        dcc.Dropdown(id='road_name1',
        options=road_options(d_exp_cam),
                placeholder="Select road...",
                style={'width':'200px','margin':'0 auto', 'display': 'inline-block'})
        ],
        style = {'width':'41.4%','display':'flex','margin-left':'480px','align-items':'center','justify-content':'center'}
        ),

    html.Br(),
    html.Div(
        # Camera dropdown
        children = [
        html.H6('Select camera', style={'font-weight': 'bold'}),
        dcc.Dropdown(id='camera_id1',
                        placeholder='Select camera...',
                        style={'width':'203px', 'margin':'0 auto','display': 'inline-block', 'justify-content':'center'})
            ],
        style = {'width':'39.8%','margin-left':'480px','display':'flex','align-items':'center'}
        ),

    html.Br(),
    #Date pick
    html.Div(
        children=[
        html.H6("Select date", style={'font-weight': 'bold'}),
        dcc.DatePickerSingle(id = "traffic_date1",
                                min_date_allowed = date.today(), max_date_allowed = date.today()+timedelta(days=60),
                                initial_visible_month = date.today(),
                                placeholder='DD/MM/YYYY',
                                style = {'width':'400px','margin':'0 auto', 'border-radius': '0 auto', 'font_family': 'Tahoma'})
        ],
        style ={'margin-left':'480px','width':'37%','display':'flex','align-items':'center','justify-content':'center'}
        ),

    html.Br(),
    #Time input
    html.Div(
        children=[
        html.H6('Select time of the day', style={'font-weight': 'bold'}),
        dcc.Input(id="traffic_time1", type="text",
                      placeholder="HHMM",
                      style = {'width':'190px','margin':'0 auto', 'height':'32px',
                               'fontSize': '15px','display': 'inline-block', 'align-items':'center','justify-content':'center'})
        ],
        style = {'width':'35.3%','margin-left':'480px','display':'flex','align-items':'center','justify-content':'center'}
        ),
    html.Br(),
    html.Br(),
    
    #Predictions
    html.Div(
            children=[
            #Prediction attributes
            html.Div(
                children=[
                html.H5('Traffic condition:', style={'font-weight': 'bold'}),
                ],style={'padding':'20px','text-align': 'right'},
                ),
            html.Div(id = 'predict')
            ],    
            style = {'display':'flex','align-items':'center','justify-content':'center'}
            ),],
    style={'text-align':'center', 'display':'inline-block', 'width':'100%', 'background-color': 'white'}
    )
