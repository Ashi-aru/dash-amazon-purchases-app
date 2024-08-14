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
    ),
])


if(__name__ == '__main__'):
    app.run(debug=True)