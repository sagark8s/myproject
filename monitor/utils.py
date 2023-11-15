from .database import insert_token_usage
import datetime as dt
''' THe object which we will cascade through all the functions and store the resuls & prompt lineage'''
class MonitorPipeLineObject:
    request_id = ''
    ''' How the query is transformed through the each layer'''
    query=[]
    ''' All the data referred to get the solution'''
    data_points=[]
    ''' All the answers from each additional module'''
    answer=[]
    ''' The previous questions from the user'''
    history=[]
    ''' Which stage of execution , the question is located at'''
    latest_query=''
    '''User email id'''
    user_id=''
    ''' Session Id of the user '''
    session_id=''
    default_entities={}
    '''Answer prefix needed since we need to display that info in frontend'''
    stage=[]
    thoughts=[]
    time = []
    ''' Latest stage input'''
    latest_query=''
    exchange_id=1
    default_entities={}
    ''' Tokens used '''
    tokens=[]
    def __init__(self,user_id,history,query,latest_query):
        self.user_id,self.session_id = user_id,user_id
        self.history,self.latest_query=history,latest_query
        self.query.append(query)
        
    def load_stats(self,query_='',data_points_='',answer_='',thought_='',stage_='',token_=0):
        self.query.append(query_)
        self.data_points.append(data_points_)
        self.answer.append(answer_)
        self.thoughts.append(thought_)
        self.stage.append(stage_)
        self.tokens.append(token_)
        self.time.append(dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30))
        self.store_token_usage()
    
    def get_api_response(self):
        result = {}
        result['data_points']=self.data_points
        result['thoughts']='<br><br>'.join(self.thoughts)
        result['exchange_id']=self.exchange_id
        result['answer'] = self.answer[-1]
        result['tokens']=sum(self.tokens)
        return result

    def store_token_usage(self,index=-1):
        ''' to store openai token usage across different stages of appn'''
        insert_token_usage(request_id=self.request_id,query=self.history[-1]['user'],stage=self.stage[index],tokens=self.tokens[index],time=self.time[index])

