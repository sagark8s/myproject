from .models import table_name,Base,conversation_qna_config
from .utils import get_chat_history_as_text
from sqlalchemy import create_engine,inspect,insert
import pandas as pd
from utils.utils import console
class conversation_config:

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
            conn.execute(insert(conversation_qna_config))
            conn.commit()
        return pd.read_sql(f'select * from {table_name}',con=engine).loc[index]

    
    def GetOptimizationPrompt(self,history):
        latest_query = history[-1]['user']
        user_history = '\n'.join([i['content'] for i in get_chat_history_as_text(history,specific_role='user')])
        return self.CHAT_OPTIMIZATION_PROMPT.format(chat_history=user_history,latest_question=latest_query)
    

    
    def __init__(self,index) -> None:
        '''tHESE values will change depending on the user and rls , hence most values are instance and not static'''
        db_settings = self.get_config(index)
        self.CHAT_OPTIMIZATION_PROMPT = db_settings.CHAT_OPTIMIZATION_PROMPT
        self.CLASSIFER_PROMPT_TEMPLATE = db_settings.CLASSIFER_PROMPT_TEMPLATE

    