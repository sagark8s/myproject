import requests
import pandas as pd
import time

api_key = '6e85bc2cb31f46f6a282d064f7d2bdec'
def get_all_categories():
    return pd.DataFrame(requests.get(url=f'https://api.parrapi.com/api/atlas/categories?key={api_key}&out=json').json())
def get_category_product_types(product_type):
    return pd.DataFrame(requests.get(url=f'https://api.parrapi.com/api/atlas/producttypes?key={api_key}&cats={product_type}').json())
def get_all_elements(product_type):
    '''url visit pattern'''
    get_url = lambda page_index : f"https://api.parrapi.com/api/atlas/products?key={api_key}&cla={product_type}&out=JSON&pge={page_index}&page_size=30"
    final_df = []
    for i in range(1,10):
        time.sleep(0.5)
        data = requests.get(url=get_url(i)).json()
        print(len(data))
        try:
            final_df.extend(pd.DataFrame(data)['products'].to_list())
        except Exception as e:
            print(e)

    final_df = pd.DataFrame(final_df)
    return final_df
final_dfs = []
categories = get_all_categories()
#print(get_all_categories())
for i in range(len(categories)):
    print(get_category_product_types(categories['CategoryId'][i]))
'''
all_categories = []
all_product_types = []
for i in range(len(categories)):
    category = categories.loc[i]['CategoryId']
    product_types = get_category_product_types(category)
    for j in range(len(product_types)):
        df = get_all_elements(product_types['ProductTypeId'][j])
        df['category']=category
        df['product_types']=product_types['ProductTypeId'][j]
        final_dfs.append(df)

        final_df = pd.concat(final_dfs)
        final_df.to_csv('stb_all_details.csv')
'''
#product_types = get_category_product_types('ATTRACTION')
#df = get_all_elements('SHOPPING')
