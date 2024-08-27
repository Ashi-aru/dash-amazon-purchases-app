from dash import dcc, html
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go


# ----------------------------------------------------------------
# 定数定義
PROJ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJ_DIR/'data'
with open(DATA_DIR/'category.txt', 'r') as f:
    CATEGORY_OPTION = ['All']+(f.readline()).split(',')
DF_PURCHASE = pd.read_csv(DATA_DIR/'target.csv')
DF_SURVEY = pd.read_csv(DATA_DIR/'survey.csv', index_col='Survey ResponseID')
CUSTOMER_ID = DF_SURVEY.index


# ----------------------------------------------------------------
# 関数群
def purchases_axis_maker(axis_name):
    print('----------------------\npurchases_axis_makerを実行')
    output = html.Div([
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
        # print(df)
    return df

def df_maker_s(axis_num, s_axis_selectors):
    print('----------------------\ndf_maker_sを実行')
    df = pd.DataFrame(index={"Survey ResponseID":CUSTOMER_ID})
    for i in range(axis_num):
        df.join(DF_SURVEY[s_axis_selectors[i]], on='Survey ResponseID')
    print(df)
    return df

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
    # go.Figure(data=data, layout=layout)で良いっぽい
    return fig


# ----------------------------------------------------------------
if(__name__ == '__main__'):
    print('funcs.py DONE!!')