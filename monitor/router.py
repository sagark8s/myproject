from fastapi import APIRouter
import time
from utils.utils import console
from .database import export_token_usage
''' API to enable file download '''
from starlette.responses import FileResponse
router = APIRouter()



@router.on_event('startup')
async def monitor_startup_event():
    console.log('Creating global token tracker')
    ''' Declaring global multiprocessing dictionary '''
    global token_start_time
    global token_count
    global token_limit
    token_start_time = time.time()
    token_count = 0
    token_limit = 20000

@router.get('/export_token_usage')
async def export_token_usage_api():
    export_token_usage()
    return FileResponse('token_usage.csv')

