import pandas as pd
from pathlib import Path

# 現在のスクリプトが置かれているディレクトリを取得
PROJ_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJ_DIR/'data'


def generate_new_tabular_data(new_index='Survey ResponseID'):
    """
    数的データである、注文額、注文量、注文回数を以下の階層性に分けて整理した表データを生成。
    - ユーザーID
        - 注文時期（Y-M）
            - カテゴリ

    """
    df = add_derived_attriubte(df = pd.read_csv(DATA_DIR/'amazon-purchases.csv'))

    df_categories = generate_new_categorical_tabular_data(df=df)
    df_quantitative = generate_new_quantitative_tabular_data(df=df)
    new_df =  df_quantitative.join(df_categories, on=new_index)
    return new_df.to_csv(DATA_DIR/'target.csv', index=True)


def add_derived_attriubte(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    df['total price'] = df['Purchase Price Per Unit']*df['Quantity']
    return df


def generate_new_categorical_tabular_data(df, new_index='Survey ResponseID'):
    comb_d = {'Shipping Address State':'first'} if(new_index=='Survey ResponseID') else {'Category':'first'}
    return df.groupby(new_index).agg(comb_d)


def generate_new_quantitative_tabular_data(df, new_index='Survey ResponseID'):
    comb_d = {'total price':'sum', 'Quantity':'sum'} if(new_index=='Survey ResponseID') else {'total price':'sum', 'Quantity':'sum', 'Purchase Price Per Unit':'mean'}
    multi_index = [new_index, 'Order Year', 'Order Month', 'Category']
    group1= df.groupby(multi_index).agg(comb_d)
    group2= df.groupby(multi_index).agg(Count=('Survey ResponseID', 'count'))
    return group1.join(group2, on=multi_index)

if(__name__=='__main__'):
    generate_new_tabular_data(new_index='Survey ResponseID')
