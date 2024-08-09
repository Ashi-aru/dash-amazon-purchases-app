import pandas as pd
import numpy as np
from pathlib import Path

# 現在のスクリプトが置かれているディレクトリを取得
PROJ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJ_DIR/'data'


def process_data(category="user"):
    """
    categoryで指定された値をインデックスにもつ派生表データを生成する
    Generate derivied tabular data which have the value specified in category as index.

    categoryは "user" または "product"
    category is "user" or "product"

    cullumnは、
    - "user"の場合: ユーザーID, 住所, 購入額（合計, 各年, 各年）, 購入数（合計, 各年, 各年）
    - "product"の場合: 商品ID, カテゴリ, 値段（平均）, 販売額（合計, 各年, 各年）, 販売数（合計, 各年, 各年）
    Cullumns are,
    - "user": user ID, address, value of purchases (total, each year, each year), number of purchases (total, each year, each year)
    - "product": product ID, category, price (average), amount sold (total, each year, each year), number sold (total, each year, each year)
    """

    df = add_derived_attriubte(df = pd.read_csv(DATA_DIR/'amazon-purchases.csv'))

    df_Y = generate_part_of_derived_tabular_data(df=df, category=category, time_span='Y')
    df_M = generate_part_of_derived_tabular_data(df=df, category=category, time_span='M')

    new_df = df_Y.join(df_M)
    new_df.to_csv(DATA_DIR/f'derived_{category}.csv', index=True)


def add_derived_attriubte(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Order Year'] = df['Order Date'].dt.to_period('Y')
    df['Order Month'] = df['Order Date'].dt.to_period('M')
    df['total price'] = df['Purchase Price Per Unit']*df['Quantity']
    return df


def generate_part_of_derived_tabular_data(df, category='user', time_span='Y'):
    new_Index = 'Survey ResponseID' if(category == "user") else 'ASIN/ISBN (Product Code)'
    # TODO:下のelse以下は要検討
    comb_d = {'total price':'sum', 'Quantity':'sum'} if(category == 'user') else {'total price':'sum', 'Quantity':'sum'}
    time_scale = 'Order Year' if(time_span=='Y') else 'Order Month'
    group= df.groupby([new_Index, time_scale]).agg(comb_d)

    df_ = group.unstack(level='Survey ResponseID').T
    df_p, df_q = df_.xs('total price',level=0), df_.xs('Quantity',level=0)
    df_p.columns = ['P_'+str(c) for c in df_p.columns]
    df_q.columns = ['Q_'+str(c) for c in df_q.columns]
    return df_p.join(df_q)


if(__name__=='__main__'):
    process_data(category='user')
    # process_data(category='product')