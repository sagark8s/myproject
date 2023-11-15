import time
import random
import string
from fastapi import status,Request,Response
from starlette.middleware.base import BaseHTTPMiddleware
from utils.utils import console,TimeOutException,generate_response
import logging

class add_process_time_header(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ''' This will add processing time on every request '''
        start_timestamp = time.time()
        request.state.timestamp = start_timestamp
        response = await call_next(request)
        process_time = time.time() - start_timestamp
        response.headers["X-Process-Time"] = str(process_time)
        print('add_process_time_header middleware')
        print(f'Took {process_time} to process')
        return response

class timeout_middleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ''' Will return exceptions in code as a response'''
        get_local_time = lambda x : str(x.tm_year)+'-'+str(x.tm_mon)+'-'+str(x.tm_mday)+','+str(x.tm_hour)+':'+str(x.tm_min)+':'+str(x.tm_sec)
        idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        start_time = time.time()
        local_time_formatted = get_local_time(time.localtime(start_time))
        logging.info(f"{local_time_formatted} rid={idem} start request path={request.url.path}")
        status_code=0
        response=None
        except_flag=False
        ''' will timeout after certain after amount of time '''
        try:
            response = await call_next(request)
        except TimeOutException:
            response = Response(generate_response('Operation timed out.Please try again',status.HTTP_200_OK))
        except Exception as e:
            response = Response(generate_response('Something went wrong.Please try again',status.HTTP_200_OK))

        finally:
            print('timeout_middleware middleware')
            return response

class user_tracking_middleware(BaseHTTPMiddleware):
    async def dispatch(self, request : Request, call_next):
        ''' tracking msft request header injection '''
        query_params_dict = dict(request.query_params)
        console.log(f"{query_params_dict}",style='red')
        console.log(request.url.path,style='red')
        user_id=str(request.client.host)
        msft_principal_name = 'X-Ms-Client-Principal-Name'
        if msft_principal_name in request.headers.keys():
            user_id= request.headers[msft_principal_name]
        headers = dict(request.scope['headers'])
        headers[b'user_id'] = str.encode(user_id)
        request.scope['headers'] = [(k, v) for k, v in headers.items()]
        ''' Api runtime '''
        response = await call_next(request)
        ''' Setting cookie '''
        if request.url.path=='/':
            cookie_defaults={'bg':'Global_BG_All_BU_ALL','business_group':'HC'}
        else:
            cookie_defaults={}
        for i in cookie_defaults.keys():
            if request.query_params.__contains__(i):
                cookie_value=query_params_dict[i]
                console.log(cookie_value,style='red')
                response.set_cookie(key=i,value=cookie_value)
            else:
                response.set_cookie(key=i,value=cookie_defaults[i])
        console.log('user_tracking_middleware middleware',style='green')
        return response
