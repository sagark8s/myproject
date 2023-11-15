from fastapi import APIRouter, Form, Request, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import  List


from database.database import get_db_con 


import api.schemas  as schemas
from api.service import (GetUserInfo,
                        Generate_PDF_Report,
                        Generate_PDF_Chart_Report,
                        Send_Email,
                        GetChatHistory

                        )



api_router = APIRouter()


#-----------------------------------------
#   Get User Information
#-----------------------------------------
@api_router.get("/get_user_info")
async def get_user_info(request : Request):
    ''' Will take remote ip if principal name is not present , x-ms-client-principal-name'''
    return await GetUserInfo(request)


#-----------------------------------------
#  Get Chat History
#-----------------------------------------
@api_router.get("/chat_history")
async def get_chat_history(request : Request,
                            page: int = 0,
                            limit: int = 10,
                            db: Session =Depends(get_db_con)):
    '''
    Will take remote ip if principal name is not present , x-ms-client-principal-name
    '''
    user_id='local_system'
    if 'x-ms-client-principal-name' in request.headers.keys():
        user_id=request.headers['x-ms-client-principal-name']

    return await GetChatHistory(user_id, page, limit, db)

#-----------------------------------------------------
#   Generate PDF Report
#   Generate a PDF report based on the payload sent from the front-end
#-----------------------------------------------------
@api_router.post("/export_pdf")
async def export_pdf(payload: schemas.Report_Generate_Schema):
    """
    Generate a PDF report based on the payload sent from the front-end
    """
    return await Generate_PDF_Report(payload)


#-----------------------------------------------------
#   Generate PDF Report - With Charts
#   Generate a PDF report based on the payload sent from the front-end
#-----------------------------------------------------
@api_router.post("/export_pdf_chart")
async def export_pdf_chart(payload: schemas.Report_Generate_Schema):
    """
    Generate a PDF report based on the payload sent from the front-end along with Chart
    """
    return await Generate_PDF_Chart_Report(payload)


#-----------------------------------------------------
#   Send Email along with attachment
#-----------------------------------------------------
@api_router.post("/send_mail")

async def send_mail(email: str = Form(...),
                    subject: str = Form(...),
                    message: str = Form(...),
                    files: List[UploadFile] = File(...)):

    """
    Send Email along with attachment
    """
    return await Send_Email(email, subject, message, files)
