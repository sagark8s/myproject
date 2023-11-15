from sqlalchemy import Column, Integer, String , DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqladmin import ModelView
import datetime as dt



Base = declarative_base()
table_name='token_usage'
class token_usage_config_model(Base):
    __tablename__ = table_name
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer,default=0)
    query = Column(String,default='')
    stage = Column(String,default='')
    tokens = Column(String,default=0)
    time = Column("time",DateTime, default=dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30))


    
class token_usage_config_admin_model(ModelView, model=token_usage_config_model):
    pass


