from .models import table_name,Base,text_qna_config_model
from sqlalchemy import create_engine,inspect,insert
import pandas as pd
from utils.utils import console
class text_qna_config:

    def get_config(self,index=0):
        ''' Get config from sqllite config db'''
        engine = create_engine(
        "sqlite:///config.db",
        connect_args={"check_same_thread": False})
        ins = inspect(engine)
        if ins.has_table(table_name):
            pass
        else:
            console.log('Created a new table',style='green')
            Base.metadata.create_all(engine)
            ''' To install default values '''
            conn = engine.connect()
            conn.execute(insert(text_qna_config_model))
            conn.commit()
        return pd.read_sql(f'select * from {table_name}',con=engine).loc[index]


    

    
    def __init__(self,index) -> None:
        '''tHESE values will change depending on the user and rls , hence most values are instance and not static'''
        db_settings = self.get_config(index)
        self.QNA_PROMPT = db_settings.QNA_PROMPT

