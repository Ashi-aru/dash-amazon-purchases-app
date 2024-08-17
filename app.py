from dash import Dash, dcc, html, Input, Output, callback
from pathlib import Path
import pandas as pd
import plotly.express as px


# 現在のスクリプトが置かれているディレクトリを取得
PROJ_DIR = Path(__file__).resolve().parents[0]
DATA_DIR = PROJ_DIR/'data'
with open(DATA_DIR/'category.txt', 'r') as f:
    category_option = (f.readline()).split(',')

# ----------------------------------------------------------------
# メイン


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
            value='Scatter Plot',
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

# ----------------------------------------------------------------
# コールバック関数群


# graph_typeに応じて、適切な設定画面を表示
@callback(
    Output('plot_config', 'children'),
    Input('graph_type', 'value'),
)
def show_config(graph_type):
    if(graph_type=='Scatter Plot'):
        children = [
            purchases_axis_maker(axis_name='x'),
            purchases_axis_maker(axis_name='y'),
        ]
    if(graph_type=='Parallel Cordinates Plot'):
        children = [
            dcc.Dropdown(
                options=[i for i in range(7)],
                placeholder='purchase：軸の数を選択',
                id='config_purchase_axis_num',
                className='custom-dropdown',
            ),
            dcc.Dropdown(
                options=[i for i in range(7)],
                placeholder='survey：軸の数を選択',
                id='config_survey_axis_num',
                className='sbox custom-dropdown',
            ),
        ]
    return children


# graph_type=='Parallel Cordinates Plot'専用
# 軸の数に応じて、軸設定用パーツの数を変化させる
@callback(
    Output('plot_config', 'children', allow_duplicate=True),
    Input('config_purchase_axis_num', 'value'),
    Input('config_survey_axis_num', 'value'),
    prevent_initial_call=True
)
def update_config(p_n, s_n):
    children = [
            dcc.Dropdown(
                options=[i for i in range(7)],
                placeholder='purchase：軸の数を選択',
                value=p_n,
                id='config_purchase_axis_num',
                className='custom-dropdown',
            ),
            dcc.Dropdown(
                options=[i for i in range(7)],
                placeholder='survey：軸の数を選択',
                value=s_n,
                id='config_survey_axis_num',
                className='sbox custom-dropdown',
            ),
        ]
    return children+[purchases_axis_maker(str(i)) for i in range(1,p_n+1)]+[survey_axis_maker(str(j)) for j in range(1, s_n+1)]

# グラフの生成



# ----------------------------------------------------------------
# その他の関数群（srcに移動させる可能性あり）

def purchases_axis_maker(axis_name):
    output =  html.Div([
                dcc.Dropdown(
                    options=[
                        {'label': '使用額', 'value':'spent'},
                        {'label': '購入量', 'value':'amount'},
                        {'label': '使用回数', 'value':'times'},
                    ],
                    placeholder=f'p_{axis_name}軸の値を選択' if(axis_name != 'x' and axis_name != 'y') else f'{axis_name}軸の値を選択',
                    id=f'p_{axis_name}_axis_selector' if(axis_name != 'x' and axis_name != 'y') else f'{axis_name}_axis_selector',
                    className='ssbox',
                ),
                dcc.RangeSlider(
                    min=2020,
                    max=2024,
                    step=1,
                    value=[2021, 2023],
                    marks=dict([(i,str(i))for i in range(2020,2025)]),
                    id=f'{axis_name}_year_slider',
                    className='ssbox',
                ),
                dcc.RangeSlider(
                    min=1,
                    max=12,
                    step=1,
                    value=[3, 5],
                    marks=dict([(i,str(i)) for i in range(1,13)]),
                    id=f'{axis_name}_month_slider',
                    className='ssbox',
                ),
                dcc.Dropdown(
                    options=category_option,
                    placeholder='カテゴリを選択',
                    id=f'{axis_name}_category_dropdown',
                    className='ssbox',
                    multi=True
                ),
                dcc.RadioItems(
                    options=['linear', 'log'],
                    value='linear',
                    id=f'{axis_name}_axis_config',
                    inline=True,
                    className='ssbox',
                ),
            ], className='sbox')
    return output


def survey_axis_maker(axis_name):
    output =  html.Div([
                dcc.Dropdown(
                    options=[
                        'Q-demos-age',
                        'Q-demos-hispanic',
                        'Q-demos-race',
                        'Q-demos-education',
                        'Q-demos-income',
                        'Q-demos-gender',
                        'Q-sexual-orientation',
                        'Q-demos-state',
                        'Q-amazon-use-howmany',
                        'Q-amazon-use-hh-size',
                        'Q-amazon-use-how-oft',
                        'Q-substance-use-cigarettes',
                        'Q-substance-use-marijuana',
                        'Q-substance-use-alcohol',
                        'Q-personal-diabetes',
                        'Q-personal-wheelchair',
                        'Q-life-changes',
                        'Q-sell-YOUR-data',
                        'Q-sell-consumer-data',
                        'Q-small-biz-use',
                        'Q-census-use',
                        'Q-research-society'
                    ],
                    placeholder=f's_{axis_name}軸の値を選択',
                    id=f'p_{axis_name}_axis_selector(survey)',
                    className='ssbox',
                ),
            ], className='sbox')
    return output



if(__name__ == '__main__'):
    app.run(debug=True)