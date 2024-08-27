from dash import Dash, dcc, html, Input, Output, callback, ALL
from src.funcs import purchases_axis_maker,survey_axis_maker,df_maker_p,parallel_cordinates_plot_maker

# ----------------------------------------------------------------
# コールバック関数

# 軸の数を受け取り、軸の設定画面を表示
@callback(
    Output('plot_config', 'children'),
    Input('purchase_axis_num', 'value'),
    Input('survey_axis_num', 'value'),
)
def update_config(p_n, s_n):
    print('----------------------\nupdate_configを実行')
    return [purchases_axis_maker(str(i)) for i in range(1,p_n+1)]+[survey_axis_maker(str(j)) for j in range(1, s_n+1)]

# グラフの生成
@callback(
        Output('main_plot', 'figure'),
        Input({"type":"p_axis_selector", "index":ALL}, 'value'),
        Input({"type":"p_year_slider", "index":ALL}, 'value'),
        Input({"type":"p_month_slider", "index":ALL}, 'value'),
        Input({"type":"p_category_dropdown", "index":ALL}, 'value'),
        Input({"type":"p_axis_config", "index":ALL}, 'value'),
)
def update_main_scatter(p_axis_selectors, p_year_sliders, p_month_sliders, p_category_dropdowns, p_axis_configs):
    print('----------------------\nupdate_main_scatterを実行')
    df = df_maker_p(p_axis_selectors, p_year_sliders, p_month_sliders, p_category_dropdowns, p_axis_configs, axis_num=4)
    fig = parallel_cordinates_plot_maker(df=df)
    return fig

# ----------------------------------------------------------------
# メイン
app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Div([
        html.Div([
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
                className='custom-dropdown',
            ),
        ], className='mbox container_left'),
        html.Div(
            id='plot_config',
            className='mbox container'
        ),
        dcc.Graph(id='main_plot'),
    ], className='bbox')
])


if(__name__ == '__main__'):
    app.run(debug=True)
