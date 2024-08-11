import pandas as pd
from pathlib import Path

# 現在のスクリプトが置かれているディレクトリを取得
PROJ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJ_DIR/'data'


def generate_new_tabular_data(new_index='Survey ResponseID'):
    """
    new_indexで指定された値をインデックスにもつ派生表データを生成する
    Generate derivied tabular data which have the value specified in new_index as index.

    new_indexは "Survey ResponseID" または "ASIN/ISBN (Product Code)"
    new_index is "Survey ResponseID" or "ASIN/ISBN (Product Code)"

    cullumnは、
    - "user"の場合: ユーザーID(Survey ResponseID), 住所, 購入額（合計, 各年, 各年）, 購入数（合計, 各年, 各年）
    - "product"の場合: 商品ID(ASIN/ISBN), カテゴリ, 値段（平均）, 販売額（合計, 各年, 各年）, 販売数（合計, 各年, 各年）
    Cullumns are,
    - "user": user ID(Survey ResponseID), address, value of purchases (total, each year, each year), number of purchases (total, each year, each year)
    - "product": product ID(ASIN/ISBN), category, price (average), amount sold (total, each year, each year), number sold (total, each year, each year)
    """
    df = add_derived_attriubte(df = pd.read_csv(DATA_DIR/'amazon-purchases.csv'))

    df_categories = generate_new_categorical_tabular_data(df=df, new_index=new_index)
    df_Y = generate_new_quantitative_tabular_data(df=df, new_index=new_index, time_span='Y')
    df_M = generate_new_quantitative_tabular_data(df=df, new_index=new_index, time_span='M')

    new_df = df_categories.join(df_Y, on=new_index).join(df_M, on=new_index)
    file_name = 'userID' if(new_index=='Survey ResponseID') else 'productID'
    new_df.to_csv(DATA_DIR/f'derived_{file_name}.csv', index=True)


def add_derived_attriubte(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Order Year'] = df['Order Date'].dt.to_period('Y')
    df['Order Month'] = df['Order Date'].dt.to_period('M')
    df['total price'] = df['Purchase Price Per Unit']*df['Quantity']
    return df


def generate_new_categorical_tabular_data(df, new_index='Survey ResponseID'):
    comb_d = {'Shipping Address State':'first'} if(new_index=='Survey ResponseID') else {'Category':'first'}
    return df.groupby(new_index).agg(comb_d)


def generate_new_quantitative_tabular_data(df, new_index='Survey ResponseID', time_span='Y'):
    comb_d = {'total price':'sum', 'Quantity':'sum'} if(new_index=='Survey ResponseID') else {'total price':'sum', 'Quantity':'sum', 'Purchase Price Per Unit':'mean'}
    time_scale = 'Order Year' if(time_span=='Y') else 'Order Month'
    group= df.groupby([new_index, time_scale]).agg(comb_d)

    # new_indexはIndexに固定したまま、それ以外を転置する
    # new_index remains fixed as Index and transposes the others
    df_ = group.unstack(level=new_index).T
    # 転置したdfを二つ目のindexによって分離
    # Separate the transposed df by a second index
    df_p, df_q = df_.xs('total price',level=0), df_.xs('Quantity',level=0)
    # カラム名に"価格を表すP" or "量を表すQ"のいずれかを適宜付け加える
    # Add either "P for price" or "Q for quantity" to the column name appropriately.
    df_p.columns = ['P_'+str(c) for c in df_p.columns]
    df_q.columns = ['Q_'+str(c) for c in df_q.columns]
    # new_indexを軸に、横向きに合体させる
    return df_p.join(df_q, on=new_index)


if(__name__=='__main__'):
    generate_new_tabular_data(new_index='Survey ResponseID')
    generate_new_tabular_data(new_index='ASIN/ISBN (Product Code)')