import pandas as pd
df = pd.read_csv('stb_all_details.csv')
def get_dict_from_str(d):
    d = eval(d)
    d = d[0]
    return d
def get_str_from_dict(d):
    output=''
    for i in d.keys():
        if d[i]!='':
            output = f"{i}:{d[i]}\n{output}"
    return output

df['addresses'] = df['addresses'].apply(get_dict_from_str)
address_df = pd.DataFrame(df['addresses'].tolist())
df['full_address']=df['addresses'].apply(get_str_from_dict)
del df['addresses']
pd.concat([df,address_df],axis=1).to_excel('stb_all_details.xlsx',index=0)
