from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, JSONResponse

from api.utils.export_pdf import GenerateReport
from api.utils.export_pdf_chart import GenerateReport_With_Chart
from api.utils.email_utils import SendEmail_Attachments
from api.utils.chat_info import ChatDetails
import api.schemas  as schemas

#-----------------------------------------------------
#   Get User information
#-----------------------------------------------------
async def GetUserInfo(request : Request):
 
    ret = {}
    ret['user_id'] = 'U-Chat'
    ret['status']   = 'FAIL'
    response_code = status.HTTP_400_BAD_REQUEST

    print(request.headers.keys())
    if 'user_id' in request.headers.keys():       
        ret['user_id']  = request.headers['user_id']
        ret['status']   = 'PASS'
        response_code = status.HTTP_200_OK

    json_compatible_response = jsonable_encoder(ret)    
    return JSONResponse(content=json_compatible_response, status_code=response_code)


#-----------------------------------------------------
#  Generate PDF File
#-----------------------------------------------------
async def Generate_PDF_Report(payload: schemas.Report_Generate_Schema):
    obj = GenerateReport()
    pdf_report_file = obj.populate_data(payload)
    return FileResponse(pdf_report_file,   media_type='application/pdf',filename=pdf_report_file)


#-----------------------------------------------------
#  Generate PDF File - with chart
#-----------------------------------------------------
async def Generate_PDF_Chart_Report(payload: schemas.Report_Generate_Schema):
    obj = GenerateReport_With_Chart()
    pdf_report_file = obj.populate_data(payload)
    return FileResponse(pdf_report_file,   media_type='application/pdf',filename=pdf_report_file)

    #json_compatible_response = jsonable_encoder({})    
    #return JSONResponse(content=json_compatible_response, status_code=status.HTTP_200_OK)



#-----------------------------------------------------
#   Send Email along with attachment
#-----------------------------------------------------

async def Send_Email(emails, subject, message, files):
    
    ret = {}
    ret['message'] = 'Error sending Email, please contact administrator'
    ret['status']   = 'FAIL'
    response_code = status.HTTP_400_BAD_REQUEST

    email_lst  =   emails.split(',')    
    obj = SendEmail_Attachments(email_lst)
    success = await obj.send_mail(subject, message, files)

    if success:
        ret['message'] = 'Email sent successfully'
        ret['status']   = 'PASS'
        response_code = status.HTTP_200_OK
    
    json_compatible_response = jsonable_encoder(ret)    
    return JSONResponse(content=json_compatible_response, status_code=response_code)



#-----------------------------------------
#  Get Chat History
#-----------------------------------------
async def GetChatHistory(user_id, page, limit, db):
 
    obj = ChatDetails(db, user_id)
    total, chat_info = obj.get_chat_details(page, limit)

    ret = {}
    ret['total'] = total
    ret['records'] = chat_info
    ret['page'] = page + 1
     
    json_compatible_response = jsonable_encoder(ret)    
    return JSONResponse(content=json_compatible_response)
