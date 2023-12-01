''' common imports across all the programs '''
import warnings
warnings.filterwarnings("ignore")
from utils.Logging import debug
''' if linux set True , windows set False '''
from fastapi import FastAPI,Request,Cookie,BackgroundTasks
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
''' For starting separate process and then killing after time out'''
from utils.utils import *
''' pydantic import '''
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
''' For file downloads '''
from starlette.responses import FileResponse
import logging
import hashlib
from database.samodels import *
from router import api_router
from database.database import engine
from conversation.qna import run_query_pipeline
from text_qna.pg_semantic_search import default_page



''' Rich text formatting for better view in terminal '''
''' Refresh embeddings '''

from utils.utils import console

''' Creating a  cache key '''
create_cache_key = lambda x : str(hashlib.md5(x.encode()).hexdigest())
''' For session tracking '''
session_id_dict = {}
''' convert dict to json '''
def jsonify(dict):
    return dict



''' FastAPI object for router class '''

description = r'Unica API provides the complete documentation of all the API for required for the Unica voicebot web application.'
title_name = r'Unica Voicebot API'
app = FastAPI(title=title_name, description=description)



app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Router Definition
# ---------------------------
app.include_router(api_router)


''' Token monitor imports'''

from monitor.router import router as monitor_router
app.include_router(monitor_router)
from monitor.utils import MonitorPipeLineObject


import hashlib
create_cache_key = lambda x : str(hashlib.md5(x.encode()).hexdigest())
session_id_dict = {}

manager=None
return_dict=None
@app.on_event("startup")
async def startup_event():
    ''' Declaring global multiprocessing dictionary '''
    from conversation.config import conversation_config
    from text_qna.config import text_qna_config
    global configs
    configs = {}
    configs['conversation']=conversation_config(0)
    configs['text_qna']=text_qna_config(0)
    console.log('Finished loading configs',style='green')
    ''' Declaring global multiprocessing dictionary '''

''' The above variable is common in global memory'''

@app.post("/Startup_image_link")
async def default_page_result():
    ''' Startup Page image'''
    # response = {}
    print("Startup_image_link")
    result = default_page()
    return result


@app.post("/chat")
async def chat(request : Request,bg: str = Cookie(None),business_group=Cookie(None)):
    ''' Cookie preprocessing'''
    bg=bg.replace(' ','')
    console.log(f'bg={bg} ; business_group={business_group}',style='red')
    bg = bg.split(',')
    request_id = str(time.time())
    session_id = request.headers['user_id']
    msft_principal_name = 'X-Ms-Client-Principal-Name'
    if msft_principal_name in request.headers.keys():
        session_id= request.headers[msft_principal_name]
    chat_history = await request.json()
    try:
        pipeline_obj = MonitorPipeLineObject(user_id=session_id,history=chat_history['history'],
        query=chat_history['history'][-1]['user'],latest_query=chat_history['history'][-1]['user'])
    except Exception as e:
        print(e)
    console.print('Starting Gpt Pipeline \n Created pipeline object : ',style='green1')
    pipeline_obj = run_query_pipeline(pipeline_obj,configs=configs)
    result = pipeline_obj.get_api_response()
    del pipeline_obj
    return result

''' pydantic model for chatgpt chart'''
class ChartInput(BaseModel):
    data : str



''' Feedback api for comments , like dislike '''
@app.post("/feedback")
async def feedback(request : Request):
    """ To submit user feedback  on chatbot message.
    param:exchange_id
    param:reaction
    param:comment (optional)
    return: {}
    e.g. request_data = {
        "exchange_id":1,
        "reaction":"LIKE",
        "comment":"test"
        }
    """
    try:
        like_dict = {'LIKE':1,'DISLIKE':-1,'RESET':0}
        json_payload= await request.json()
        print(json_payload)
        exchange_id=json_payload['exchange_id']
        like=like_dict[json_payload['reaction']]
        additional_comments=''
        comment_categories=''
        ''' comment only on dislike so that condition is checked here '''
        if like == -1:
            ''' to check if normal dislike or dislike with comment '''
            if 'additional_comments' in json_payload.keys():
                additional_comments = json_payload['additional_comments']
            if 'comment_categories' in json_payload.keys():
                comment_categories = ','.join(json_payload['comment_categories'])
        update_like(additional_comments,comment_categories,like,exchange_id)
        print('updated in database')
        return jsonify({'status':'PASS', "message":"Thank you for your feedback"}), 200
    except Exception as e:
        logging.exception("Exception in /feedback")
        return jsonify({'status':'FAIL', "message":"Bad request"}), 400

''' for maps'''
from generate_map import generate_map
from fastapi.responses import HTMLResponse
@app.get("/generate_map/")
async def api_data(request: Request):
    query_params = dict(request.query_params)
    name = query_params['name']
    if os.path.exists(name):
        response = HTMLResponse(open(name,"r").read())
    else:
        response = HTMLResponse("""<html>File does not exist</html>""")
    return response

''' API to enable file download '''
from starlette.responses import FileResponse

@app.get('/generate_excel_file')
def generate_download_file(request : Request,start_time:str = '23-07-18 11:00:0', end_time: str = '23-07-18 12:00:0'):
    print(f"Generating Excel File between {start_time} - {end_time}")
    file_path = export_all_data(start_time,end_time)
    return file_path

@app.get('/download')
def downloadFile (request : Request,file_path:str):
    print(f"Filedownload")
    return FileResponse(file_path)

''' admin module attachment '''
from sqladmin import Admin
from conversation.models  import conversation_qna_config_admin_model
from text_qna.models import text_qna_config_admin_model
''' Static files serving section '''
from middleware import *
app.add_middleware(user_tracking_middleware)
app.mount("/", StaticFiles(directory="static", html = True), name="static")
''' Middleware section of the code '''
app.add_middleware(add_process_time_header)

admin = Admin(app, engine)
admin.add_model_view(conversation_qna_config_admin_model)
admin.add_model_view(text_qna_config_admin_model)


if __name__ == "__main__":
    uvicorn.run("app:app", reload =False, host="0.0.0.0",port=8518,workers=2)
    # uvicorn.run("app:app", reload =True, host="0.0.0.0",port=8590)
