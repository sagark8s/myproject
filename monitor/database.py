from .models import table_name,Base,token_usage_config_model
from sqlalchemy import create_engine,inspect,insert,select
from utils.utils import console
import pandas as pd

''' Get config from sqllite config db'''
engine = create_engine(
"sqlite:///token_usage.db",
connect_args={"check_same_thread": False})
ins = inspect(engine)
if ins.has_table(table_name):
    pass
else:
    console.log(f'Created a new table {table_name}',style='green')
    Base.metadata.create_all(engine)
    ''' To install default values '''
    conn = engine.connect()
    
def insert_token_usage(request_id,query,stage,tokens,time):
    conn = engine.connect()
    conn.execute(insert(token_usage_config_model).values(request_id=request_id,query=query,stage=stage,tokens=tokens,time=time))
    conn.commit()
    conn.close()

def export_token_usage():
    conn=engine.connect()
    df = pd.DataFrame(conn.execute(select(token_usage_config_model)).fetchall())
    print(df)
    df.to_csv('token_usage.csv')
