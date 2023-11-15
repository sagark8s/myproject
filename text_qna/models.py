from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqladmin import ModelView
from rich.console import Console
from .prompt import QNA_PROMPT
console = Console()



Base = declarative_base()
table_name='text_qna_config_model'
class text_qna_config_model(Base):
    __tablename__ = table_name
    id = Column(Integer, primary_key=True)
    QNA_PROMPT = Column(String,default=QNA_PROMPT)
    
    
class text_qna_config_admin_model(ModelView, model=text_qna_config_model):
    pass
