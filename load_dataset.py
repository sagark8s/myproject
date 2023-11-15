from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)
import pandas as pd
from openai_config import load_openai
openai = load_openai()
from openai.embeddings_utils import get_embedding
import os
import numpy as np
from config.database_config import engine
from sqlalchemy import text
''' Function to create embedding from openai'''
def get_text_embedding(text):
    try:
        return list(get_embedding(text, engine = 'text-embedding-ada-002'))
    except:
        return get_embedding('Unable to retrieve embedding', engine = 'text-embedding-ada-002')

''' Creating embeddings ''' 
def push_vector_database():
    data_store_disk_file = 'stb_embedding.pkl'
    if os.path.exists(data_store_disk_file):
        df = pd.read_csv(data_store_disk_file)
    else:
        """
        
        """
        df = pd.read_excel('stb_all_details.xlsx')
        try:del df['Unnamed: 0']
        except Exception as e:print(e)
        df['full_product']=df['productName']+'\n'+df['productDescription']
        df['full_information'] = df['full_product']+df['full_address']
        print(df.columns)
        for i in ['full_product','full_information','full_address']:
            print(df[i])
            df[f'{i}_vector'] = df[i].parallel_apply(get_text_embedding)
        df.to_csv(data_store_disk_file)

    ''' pushing to database '''
    del df['index']
    df.reset_index(inplace = True)
    df.to_sql('stb_vector_data_store',engine,index=False,if_exists='replace')
    conn = engine.connect()

    queries=['ALTER TABLE public.stb_vector_data_store ALTER COLUMN full_product_vector TYPE public.vector USING full_product_vector::public.vector::public.vector;',
    'ALTER TABLE public.stb_vector_data_store ALTER COLUMN full_information_vector TYPE public.vector USING full_information_vector::public.vector::public.vector;',
    'ALTER TABLE public.stb_vector_data_store ALTER COLUMN full_address_vector TYPE public.vector USING full_address_vector::public.vector::public.vector;']
    for i in queries:
        conn.execute(text(i))
        conn.commit()

    conn.close()
def push_faq_file():
    df = pd.read_csv('final.csv')
    updated_link = []
    updated_text = []
    for i in range(len(df)):
        chunks = df['about'][i].split(' ')
        split_n = len(chunks)//100
        if split_n<1:
            split_n=1
        split_text = [' '.join(i) for i in list(np.array_split(chunks,split_n))]
        updated_text = updated_text + split_text
        updated_link = updated_link + len(split_text)*[df['link'][i]]
    updated_df = pd.DataFrame()
    updated_df['link']=updated_link
    updated_df['about']=updated_text
    updated_df['about_vector'] = updated_df['about'].parallel_apply(get_text_embedding)
    #updated_df['about_vector'] = updated_df['about_vector'].str.replace('{',"'[").replace('}',"]'")
    print(updated_df)
    updated_df.reset_index(inplace = True)
    updated_df.to_sql('stb_vector_faq_store',engine,index=False,if_exists='replace')
    conn = engine.connect()
    queries=["""update stb_vector_faq_store set about_vector  = replace(about_vector,'{','[')""",
             """update stb_vector_faq_store set about_vector  = replace(about_vector,'}',']')""",
             """ALTER TABLE public.stb_vector_faq_store ALTER COLUMN about_vector TYPE public.vector USING about_vector::public.vector::public.vector;"""]
    for i in queries:
        conn.execute(text(i))
        conn.commit()

    conn.close()
    
push_vector_database()
print('FInished first vector database')
push_faq_file()
