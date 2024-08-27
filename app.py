from dash import Dash, dcc, html, Input, Output, callback, Patch, ALL
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# 現在のスクリプトが置かれているディレクトリを取得
PROJ_DIR = Path(__file__).resolve().parents[0]
DATA_DIR = PROJ_DIR/'data'
with open(DATA_DIR/'category.txt', 'r') as f:
    CATEGORY_OPTION = ['All']+(f.readline()).split(',')
DF_PURCHASE = pd.read_csv(DATA_DIR/'target.csv')
DF_SURVEY = pd.read_csv(DATA_DIR/'survey.csv', index_col='Survey ResponseID')
CUSTOMER_ID = DF_SURVEY.index

# ----------------------------------------------------------------
# メイン
app = Dash(__name__, suppress_callback_exceptions=True)


app.layout = html.Div([
    html.Div([
        # グラフの設定
        dcc.Dropdown(
            options=[i for i in range(5)],
            placeholder='purchase：軸の数を選択',
            id='purchase_axis_num',
            className='custom-dropdown',
        ),
        dcc.Dropdown(
            options=[i for i in range(5)],
            placeholder='survey：軸の数を選択',
            id='survey_axis_num',
            className='sbox custom-dropdown',
        ),
        
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
    print('----------------------\nshow_configを実行')
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
                id='purchase_axis_num',
                className='custom-dropdown',
            ),
            dcc.Dropdown(
                options=[i for i in range(7)],
                placeholder='survey：軸の数を選択',
                id='survey_axis_num',
                className='sbox custom-dropdown',
            ),
        ]
    return children


# graph_type=='Parallel Cordinates Plot'専用
# 軸の数に応じて、軸設定用パーツの数を変化させる
@callback(
    Output('plot_config', 'children', allow_duplicate=True),
    Input('purchase_axis_num', 'value'),
    Input('survey_axis_num', 'value'),
    prevent_initial_call=True
)
def update_config(p_n, s_n):
    print('----------------------\nupdate_configを実行')
    children = [
            dcc.Dropdown(
                options=[i for i in range(7)],
                placeholder='purchase：軸の数を選択',
                value=p_n,
                id='purchase_axis_num',
                className='custom-dropdown',
            ),
            dcc.Dropdown(
                options=[i for i in range(7)],
                placeholder='survey：軸の数を選択',
                value=s_n,
                id='survey_axis_num',
                className='sbox custom-dropdown',
            ),
        ]
    return children+[purchases_axis_maker(str(i)) for i in range(1,p_n+1)]+[survey_axis_maker(str(j)) for j in range(1, s_n+1)]

# グラフの生成
@callback(
        Output('main_plot', 'figure'),
        Input('graph_type', 'value'),
        Input({"type":"p_axis_selector", "index":ALL}, 'value'),
        Input({"type":"p_year_slider", "index":ALL}, 'value'),
        Input({"type":"p_month_slider", "index":ALL}, 'value'),
        Input({"type":"p_category_dropdown", "index":ALL}, 'value'),
        Input({"type":"p_axis_config", "index":ALL}, 'value'),
)
def update_main_scatter(graph_type, p_axis_selectors, p_year_sliders, p_month_sliders, p_category_dropdowns, p_axis_configs):
    print('----------------------\nupdate_main_scatterを実行')
    df = df_maker_p(p_axis_selectors, p_year_sliders, p_month_sliders, p_category_dropdowns, p_axis_configs, axis_num=2)
    fig = scatter_plot_maker(df=df)
    return fig

"""
@callback(
        Output('main_plot', 'figure'),
        Input('graph_type', 'value'),
        Input('purchase_axis_num', 'value'),
        Input('survey_axis_num', 'value'),
        Input({"type":"p_axis_selector", "index":ALL}, 'value'),
        Input({"type":"p_year_slider", "index":ALL}, 'value'),
        Input({"type":"p_month_slider", "index":ALL}, 'value'),
        Input({"type":"p_category_dropdown", "index":ALL}, 'value'),
        Input({"type":"p_axis_config", "index":ALL}, 'value'),
        Input({"type":"s_axis_selector", "index":ALL}, 'value'),
        prevent_initial_call=True
)
def update_main_parallel(graph_type, p_num, s_num, p_axis_selectors, p_year_sliders, p_month_sliders, p_category_dropdowns, p_axis_configs, s_axis_selectors):
    print('----------------------\nupdate_main_graphを実行')
    if(graph_type == "Parallel Cordinates Plot"):
        df = df_maker_p(p_axis_selectors, p_year_sliders, p_month_sliders, p_category_dropdowns, p_axis_configs, axis_num=p_num)
        df.join(df_maker_s(s_axis_selectors, axis_num=s_num), on="Survey ResponseID")
        fig = parallel_cordinates_plot_maker(df)
    return fig
"""
# ----------------------------------------------------------------
# その他の関数群（srcに移動させる可能性あり）

def purchases_axis_maker(axis_name):
    print('----------------------\npurchases_axis_makerを実行')
    output =  html.Div([
                dcc.Dropdown(
                    options=[
                        {'label': '使用額', 'value':'spent'},
                        {'label': '購入量', 'value':'amount'},
                        {'label': '使用回数', 'value':'times'},
                    ],
                    placeholder=f'p_{axis_name}軸の値を選択',
                    id={"type":"p_axis_selector", "index":axis_name},
                    className='ssbox',
                ),
                dcc.RangeSlider(
                    min=2020,
                    max=2024,
                    step=1,
                    value=[2021, 2023],
                    marks=dict([(i,str(i))for i in range(2020,2025)]),
                    id={"type":"p_year_slider", "index":axis_name},
                    className='ssbox',
                ),
                dcc.RangeSlider(
                    min=1,
                    max=12,
                    step=1,
                    value=[3, 5],
                    marks=dict([(i,str(i)) for i in range(1,13)]),
                    id={"type":"p_month_slider", "index":axis_name},
                    className='ssbox',
                ),
                dcc.Dropdown(
                    options=CATEGORY_OPTION,
                    placeholder='カテゴリを選択',
                    id={"type":"p_category_dropdown", "index":axis_name},
                    className='ssbox',
                    multi=True
                ),
                dcc.RadioItems(
                    options=['linear', 'log'],
                    value='linear',
                    id={"type":"p_axis_config", "index":axis_name},
                    inline=True,
                    className='ssbox',
                ),
            ], className='sbox')
    return output


def survey_axis_maker(axis_name):
    print('----------------------\nsurvey_axis_makerを実行')
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
                    id={"type":"s_axis_selector", "index":axis_name},
                    className='ssbox',
                ),
            ], className='sbox')
    return output


def df_maker_p(p_axis_selectors, p_year_sliders, p_month_sliders, p_category_dropdowns, p_axis_configs, axis_num=2):
    print('----------------------\ndf_maker_pを実行')
    df = pd.DataFrame(index={"Survey ResponseID":CUSTOMER_ID})
    for i in range(axis_num):
        axis_name = p_axis_selectors[i]
        year_query = (p_year_sliders[i][0]<=DF_PURCHASE['Order Year']<=p_year_sliders[i][1])
        month_query = (p_month_sliders[i][0]<=DF_PURCHASE['Order Month']<=p_month_sliders[i][1])
        category_query = (DF_PURCHASE['Category'].isin(p_category_dropdowns[i])) if(p_category_dropdowns[i][0]!='All') else True

        df_tmp = DF_PURCHASE[year_query and month_query and category_query].groupby("Survey ResponseID")[axis_name].sum()
        df_tmp.reindex(CUSTOMER_ID, fill_value=0) # ひょっとしたら{"Survey ResponseID":CUSTOMER_ID}
        if(p_axis_configs[i]=='log'):
            df_tmp.log1p(df_tmp)
        
        df.join(df_tmp, on='Survey ResponseID')
        print(df)
    return df


def df_maker_s(axis_num, s_axis_selectors):
    print('----------------------\ndf_maker_sを実行')
    df = pd.DataFrame(index={"Survey ResponseID":CUSTOMER_ID})
    for i in range(axis_num):
        df.join(DF_SURVEY[s_axis_selectors[i]], on='Survey ResponseID')
    print(df)
    return df


def scatter_plot_maker(df):
    print('----------------------\nscatter_plot_makerを実行')
    data = go.Scatter(
        x=df.iloc[:,0],
        y=df.iloc[:,1],
        mode='markers',
        marker=dict(size=12,color=df.index,),
        # text=df.iloc[:,2],
    )
    layout = go.Layout(
        title='Scatter Plot',
        xaxis=dict(title='Survey ResponseID'),
        yaxis=dict(title='Value'),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    fig = go.Figure()
    fig.add_trace(data)
    fig.update_layout(layout)
    # go.Figure(data=data, layout=layout)で良いっぽい
    return fig


def parallel_cordinates_plot_maker(df):
    print('----------------------\nparallel_cordinates_plot_makerを実行')
    data = go.Parcoords(
        # line=dict(
            # color=,
            # coloscal='Rainbow',
            # showscale=True,
        # ),
        dimensions=[dict(label='', values=df.iloc[:,i]) for i in range(len(df.columns))]
    )
    layout = go.Layout(
        title='Parallel Coordinates Plot',
        # margin=dict(l=0, r=0, t=0, b=0),
    )

    fig = go.Figure()
    fig.add_trace(data)
    fig.update_layout(layout)
    return fig


if(__name__ == '__main__'):
    app.run(debug=True)
