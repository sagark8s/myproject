import pandas as pd
from sqlalchemy import desc
import database.samodels

#-------------------------------------
#   Get Chat Details
#-------------------------------------
class ChatDetails:
    def __init__(self, db, user_id):
        self.db      = db
        self.user_id = user_id
        self.model   = samodels.ChatHistory

    #-----------------------------------------------
    #   Get Chat Details
    #-----------------------------------------------
    def get_chat_details(self, page, limit):

        query = self.db.query(self.model.id, self.model.email, self.model.text, self.model.response).filter(self.model.email == self.user_id)

        #query = self.db.query(self.model)
        total = query.count()
        query = query.order_by(desc(self.model.id))
        query = query.offset(page * limit).limit(limit)

        df = pd.read_sql(query.statement, self.db.bind)

        df = df[['id', 'email', 'text', 'response']]
        records = df.to_dict('records')

        return (total, records)
