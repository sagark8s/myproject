''' common imports across all the programs '''
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,URL
from config.config import settings
''' Loading from Config'''
connection_string = URL.create(
'postgresql+psycopg2',
username=settings.DB_USER,
password=settings.DB_PASSWORD,  # plain (unescaped) text
host=settings.DB_HOST,
database=settings.DB_NAME,
)
engine = create_engine(connection_string,pool_size=1)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
op=0
def get_db_con():
    global op
    db = engine.connect()
    op=op+1
    try:
        yield db
    finally:
        op=op-1
        db.close()


def execute_sql_query(stmt,output=False):
     res=None
     with engine.connect() as conn:
         res = conn.execute(stmt)
         conn.commit()
     if output:
         return res.fetchall()
     return res
