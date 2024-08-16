from dash import Dash, dcc, html, Input, Output, callback
from pathlib import Path
import pandas as pd
import plotly.express as px


# 現在のスクリプトが置かれているディレクトリを取得
PROJ_DIR = Path(__file__).resolve().parents[0]
DATA_DIR = PROJ_DIR/'data'

app = Dash(__name__, suppress_callback_exceptions=True)


app.layout = html.Div([
    dcc.RadioItems(
        options=['English', 'Japanese'],
        value='Japanese',
        id='language-selector',
        inline=True,
    ),
    html.Div([
        # クラスタ探索方法の設定（散布図 or Parallel Cordinates Plot）
        dcc.Dropdown(
            options=[
                {'label': 'Scatter Plot', 'value':'Scatter Plot'},
                {'label': 'Parallel Cordinates Plot', 'value':'Parallel Cordinates Plot'},
            ],
            placeholder='クラスタ探索方法を選択',
            id='graph_type',
            className='mbox',
        ),

        # グラフの設定
        html.Div(id='plot_config', className='mbox container'),

        # グラフの出力
        dcc.Graph(id='main_plot'),
    ], className='bbox')
])


@callback(
    Output('plot_config', 'children'),
    Input('graph_type', 'value'),
)
def update_config(graph_type):
    if(graph_type=='Scatter Plot'):
        children = [
            html.Div([
                dcc.Dropdown(
                    options=[
                        {'label': 'OOO', 'value':'OOO'},
                        {'label': 'xxx', 'value':'xxx'},
                    ],
                    placeholder='x軸の値を選択',
                    id='x_axis_selector',
                ),
                dcc.RadioItems(
                    options=['linear', 'log'],
                    value='linear',
                    id='x_axis_config',
                    inline=True
                ),
            ], className='sbox'),
            html.Div([
                dcc.Dropdown(
                    options=[
                        {'label': 'OOO', 'value':'OOO'},
                        {'label': 'xxx', 'value':'xxx'},
                    ],
                    placeholder='y軸の値を選択',
                    id='y_axis_selector',
                ),
                dcc.RadioItems(
                    options=['linear', 'log'],
                    value='linear',
                    id='y_axis_config',
                    inline=True
                ),
            ], className='sbox'),
            # できることならここにクエリを入れる
        ]
    if(graph_type=='Parallel Cordinates Plot'):
        children = [
            dcc.Dropdown(
                options=[
                    {'label': 'OOO', 'value':'OOO'},
                    {'label': 'xxx', 'value':'xxx'},
                ],
                placeholder='軸の値を選択',
                id='parallel_axis_config',
                multi=True,
                className='custom-dropdown',
            ),
            # ここに各ラベルに対してlinear or logを選択するボタンを入れたい
        ]
    return children




if(__name__ == '__main__'):
    app.run(debug=True)