from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqladmin import ModelView
from rich.console import Console
from .prompt import CLASSIFER_PROMPT_TEMPLATE,CHAT_OPTIMIZATION_PROMPT
console = Console()



Base = declarative_base()
table_name='conversation_qna_config'
class conversation_qna_config(Base):
    __tablename__ = table_name
    id = Column(Integer, primary_key=True)
    CLASSIFER_PROMPT_TEMPLATE = Column(String,default=CLASSIFER_PROMPT_TEMPLATE)
    CHAT_OPTIMIZATION_PROMPT = Column(String,default=CHAT_OPTIMIZATION_PROMPT)

    
class conversation_qna_config_admin_model(ModelView, model=conversation_qna_config):
    pass
