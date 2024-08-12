from dash import Dash, dcc, html, Input, Output, callback


app = Dash(__name__)


app.layout = html.Div([
    dcc.RadioItems(
        options=['English', 'Japanese'],
        value='English',
        id='language-selector',
    ),
    html.Div(id='main-content')
])


# 以下にメインコンテンツが続く。

EN_LAYOUT = [
    html.Div([
        html.Div([
            html.H5('Select how you want to find clusters'),
            dcc.RadioItems(
                # TODO:option名をいい感じにする
                    options=['Find clusters from visualisation', 'Use the clusters prepared here'],
                    value='Find clusters from visualisation',
                    id='cluster_type1',
                    inline=True,
                ),
        ], className="box"),
        html.Div([
            html.H5('Select how you want to find clusters'),
            dcc.RadioItems(
                # TODO:option名をいい感じにする
                    options=['Find clusters from visualisation', 'Use the clusters prepared here'],
                    value='Find clusters from visualisation',
                    id='cluster_type',
                    inline=True,
                ),
        ], className="box"),
    ], className="container"),
]


JA_LAYOUT = [
    html.Div([
        html.Div([
            html.H5('クラスタの見つけ方を選択'),
            dcc.RadioItems(
                # TODO:option名をいい感じにする
                    options=['可視化からクラスタを見つける', '用意したクラスタを使用する'],
                    value='可視化からクラスタを見つける',
                    id='cluster_type1',
                    inline=True,
                ),
        ], className="box"),
        html.Div([
            html.H5('クラスタの見つけ方を選択'),
            dcc.RadioItems(
                # TODO:option名をいい感じにする
                    options=['可視化からクラスタを見つける', '用意したクラスタを使用する'],
                    value='可視化からクラスタを見つける',
                    id='cluster_type',
                    inline=True,
                ),
        ], className="box"),
    ], className="container"),
]


REPORT_D = {"English":EN_LAYOUT, "Japanese":JA_LAYOUT}


@callback(
        Output('main-content', 'children'),
        Input('language-selector', 'value')
)
def select_language(language):
    return REPORT_D[language]


if(__name__ == '__main__'):
    app.run(debug=True)