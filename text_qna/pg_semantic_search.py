from sqlalchemy import create_engine,text
import pandas as pd
from openai_config import load_openai
# import openai
# from openai.embeddings_utils import get_embedding

import openai
from openai.embeddings_utils import get_embedding
import traceback
openai = load_openai()
from rich.console import Console
console = Console()
from generate_map import generate_map

from database_config import load_conn,base_ip,main_table_name,faq_table_name
connection_string = load_conn()
#http://127.0.0.1:8512/generate_map/?c=-4.3478359,55.83289869999999&name=vishnu
# base_ip='20.193.133.240:8518'
print(f"pg_semantic_search TABLE_NAME - {main_table_name}")
get_map_url = lambda name : f"http://{base_ip}/generate_map/?name={name}"
get_product_url = lambda url,product_name : f"""url: https://seychelles.com/listingdetails/{url}"""
engine = create_engine(connection_string)
conn = engine.connect()

menu = {
    "Plan your visit" : [
                        { "category_type": "Accommodation",
                          "link": "https://seychelles.com/planyourvisit/wheretostay" 
                        },
                        { "category_type": "Geeting Around",
                          "link": "https://seychelles.com/planyourvisit/gettingaround" 
                        },
                        { "category_type": "Tour Operators",
                          "link": "https://seychelles.com/planyourvisit/touroperators" 
                        },
                        { "category_type": "Travel Information",
                          "link": "https://seychelles.com/travelinfo/travelinformation" 
                        },
                        { "category_type": "About Seychelles",
                          "link": "https://seychelles.com/aboutus/aboutseychelles" 
                        },
                        { "category_type": "Airlines",
                          "link": "https://seychelles.com/planyourvisit/airlines" 
                        }], 
     "Experience" :     [{ "category_type": "Activities",
                          "link": "https://seychelles.com/experience/activities" 
                        },
                        { "category_type": "Walks & Trails",
                          "link": "https://seychelles.com/experience/walksandtrails" 
                        },
                        { "category_type": "General Servies",
                          "link": "https://seychelles.com/experience/generalservices" 
                        },
                        { "category_type": "Attractions",
                          "link": "https://seychelles.com/experience/attractions" 
                        },
                        { "category_type": "Food & Drinks",
                          "link": "https://seychelles.com/experience/food-drinks" 
                        },
                        { "category_type": "Events",
                          "link": "https://seychelles.com/experience/events" 
                        }],
     "The Islands" :     { "category_type": "The Islands",
                          "link": "https://seychelles.com/experience/theislands" 
                        }
}

def default_page():
    print("pg_semantic Startup_image_link")
    query = text(f"""WITH ranked_products AS ( SELECT "Category","productName", "productImage", ROW_NUMBER() OVER (PARTITION BY "Category" ORDER BY RANDOM()) AS row_num
    FROM {main_table_name} ) SELECT "Category","productName", "productImage" FROM ranked_products WHERE row_num <= 3""")
    result =[]
    try:result = conn.execute(query).fetchall()
    except Exception as e:print(e)
    print("*"*80)
    print("result :",result)
    print("*"*80)
    dict_list = []
    for item in result:
        category_type, description, image_url = item
        data_dict = {
            'category_type': category_type,
            'description': description,
            'image_url': image_url,
        }
        dict_list.append(data_dict)
    return dict_list

def semantic_search_id(field,query_field,query):
    query = query.lower().strip()
    embedding = get_embedding(query, engine = 'text-embedding-ada-002')
    #print(embedding)
    query = text(f"""SELECT {field}, 1- ({query_field}  <-> '{embedding}') as cos_sim
    from {main_table_name} ORDER BY cos_sim desc LIMIT 5""")
    #query = text(f"SELECT {field}   from stb_vector_data_store ORDER BY {query_field} <-> '{embedding}' LIMIT 5")
    try:result = conn.execute(query).fetchall()
    except Exception as e:print(e)
    result = pd.DataFrame(result)
    return result
    #return list(set([i[0] for i in result]))

def get_text_from_id(field,ids):
    query = text(f"""SELECT {main_table_name}.{field},"productId","productName","boundary","productImage","productDescription"  from {main_table_name} where index in {tuple(ids)}""")
    result = [list(i) for i in conn.execute(query).fetchall()]
    for i in range(len(result)):
        result[i][1]=get_product_url(result[i][1],result[i][2])
    return ['\n'.join(i[0:2]) for i in result],pd.DataFrame(result)

def semantic_search_faq(query,query_field='about_vector'):
    embedding = get_embedding(query, engine = 'text-embedding-ada-002')
    query = text(f"SELECT about,link,1- ({query_field}  <-> '{embedding}') as cos_sim from {faq_table_name} ORDER BY cos_sim desc LIMIT 5")
    try:result = conn.execute(query).fetchall()
    except Exception as e:print(e)
    return pd.DataFrame(result)

def semantic_search(query): 
    address_field = 'full_address_vector'
    product_field = 'full_product_vector'
    df = pd.concat([semantic_search_id('index',address_field,query),semantic_search_id('index',product_field,query)])
    df = df.drop_duplicates('index')
    df = df.sort_values(by='cos_sim',ascending=False)
    about_df = semantic_search_faq(query)
    #about_cos_sim_average = about_df['cos_sim'].tolist()[0]
    #product_cos_sim_average = df['cos_sim'].tolist()[0]
    about_cos_sim_average = sum(about_df['cos_sim'])/len(about_df) - 0.15
    product_cos_sim_average = sum(df['cos_sim'])/len(df)
    console.log(f"about cosine:{about_cos_sim_average} \n product cosine:{product_cos_sim_average}")
    map_url = ''
    related_links=''
    if about_cos_sim_average > product_cos_sim_average:

        result='\n\n'.join([f"{about_df['about'][i]} \n url:{about_df['link'][i]}" for i in range(len(about_df))])
        console.log(result)
        return result,map_url,related_links
    
    result,data = get_text_from_id('full_information',df['index'].to_list())
    try:
        related_links = '\n'.join(list(set([f"""<li><a href="{data[1][i].replace('url: ','')}">{data[2][i]}</a></li>""" for i in range(len(data))])))
        related_links = f"<ul>{related_links}</ul>"

        '''generate map section'''
        console.log('started map generation')
        map_url = generate_map(data,query.replace(' ','').lower())
        map_url = get_map_url(map_url)
    except Exception as e:
        console.log(traceback.format_exc())
    finally :
        return result,map_url,related_links
