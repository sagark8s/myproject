import os
from inspect import currentframe, getframeinfo
import datetime as dt
from sqlalchemy import MetaData,Table, Column, Integer, String,DateTime,text
from sqlalchemy.orm import relationship
from sqlalchemy import insert,select,update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.database import *
import pandas as pd
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #for data retrieval

''' Chat history table model '''

class ChatHistory(Base):
    __tablename__ = "unica_chat_history"
    id = Column(Integer, primary_key=True)
    email = Column("email",String)
    role = Column("role",String)
    text = Column("text",String)
    response = Column("response",String)
    session_id = Column("session_id",String)
    time = Column("time",DateTime, default=dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30))
    like = Column("like",Integer)
    supporting_content = Column("supporting_content",String)
    prompt = Column("prompt",String)
    additional_comments = Column("additional_comments",String)
    comment_categories = Column("comment_categories",String)



''' Section to upload chat history '''

def insert_chat_to_db(email='test',role='test',session_id='test',text='test',response='test_response',like=0,supporting_content='',prompt=''):
    stmt = insert(ChatHistory).values(email=email,role=role,text=text,response=response,like=like,supporting_content=supporting_content,session_id=session_id,prompt=prompt,time=dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30))
    execute_sql_query(stmt)
def get_latest_id(email='test'):
    current_session = SessionLocal()
    stmt = select(ChatHistory.id).where(ChatHistory.email==email).order_by(ChatHistory.id.desc())
    res = current_session.execute(stmt)
    current_session.close()
    return res.fetchone()[0]
def update_like(additional_comments='',comment_categories='',like_value='',id=0):
    current_session = SessionLocal()
    if additional_comments!='':
        stmt = update(ChatHistory).where(ChatHistory.id==id).values(additional_comments=additional_comments)
        current_session.execute(stmt)
        current_session.commit()
    if comment_categories!='':
        stmt = update(ChatHistory).where(ChatHistory.id==id).values(comment_categories=comment_categories)
        current_session.execute(stmt)
        current_session.commit()
    stmt = update(ChatHistory).where(ChatHistory.id==id).values(like=like_value)
    print(stmt)
    print(additional_comments,comment_categories,like_value)
    current_session.execute(stmt)
    current_session.commit()
    current_session.close()
def export_all_data(start_time,end_time):
    print('Started export process')
    current_session = SessionLocal()
    time_format = '%y-%m-%d %H:%M:%S'
    start_time,end_time=dt.datetime.strptime(start_time, time_format),dt.datetime.strptime(end_time,time_format)
    stmt = select(ChatHistory.id,ChatHistory.email,ChatHistory.text,ChatHistory.response,ChatHistory.time,ChatHistory.supporting_content,ChatHistory.prompt).where((end_time>=ChatHistory.time) & (start_time<=ChatHistory.time)).order_by(ChatHistory.id.asc())
    res = current_session.execute(stmt)
    res = res.fetchall()
    df = pd.DataFrame(res)
    filename=f"user_data_{start_time}_{end_time}.xlsx".replace(' ','_')
    if os.path.exists(filename):
        pass
    else:
        df.to_excel(filename,index=False)
    current_session.close()
    return f'/download?file_path={filename}'

def get_table_metadata():
    current_session=SessionLocal()
    res = current_session.execute(text(f"SELECT column_name,data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}';"))
    sql_column_data = { i[0]:i[1] for i in res.fetchall()}
    current_session.close()
    return sql_column_data

def get_supervised_columns_data():
    supervised_list=['period','year','country','business_unit_level','category','brand']
    current_session=SessionLocal()
    distinct_dict={}
    get_distinct_query = lambda column_name : text(f'select distinct {column_name} from {table_name}')
    for i in supervised_list:
        res = current_session.execute(get_distinct_query(i))
        distinct_dict[i]=[i[0] for i in res.fetchall()]
    current_session.close()
    return distinct_dict

def chat_history(user_email_id):
    current_session = SessionLocal()
    stmt = select(ChatHistory.id,ChatHistory.email,ChatHistory.text,ChatHistory.response).where(ChatHistory.email==user_email_id).order_by(ChatHistory.id.asc())
    res = current_session.execute(stmt)
    res = res.fetchall()
    df = pd.DataFrame(res)
    current_session.close()
    return df.to_json(orient='records')
