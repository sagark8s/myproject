from datetime import datetime,date
from fastapi import File, Form, UploadFile
import uuid
from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional, Literal, List


#--------------------------------------
#   Question Schema
#--------------------------------------
class Question_Schema(BaseModel):
    question: str
    answer: str
    chart : Optional[str] = None
   
    class Config:
        orm_mode = True

#--------------------------------------
#   Report Generation Schema
#--------------------------------------
class Report_Generate_Schema(BaseModel):

    queries: List[Question_Schema]
  
    class Config:
        schema_extra = {
            "example": {
                "queries": [
                    {
                        "question": "What are the Business Units within Homecare ?",
                        "answer": "The given <content> & **#^#()<>)#*# does not provide information about the specific Business Units within Homecare.",
                        "chart" : r'https://images.pexels.com/photos/6476589/pexels-photo-6476589.jpeg?cs=srgb&dl=pexels-mikael-blomkvist-6476589.jpg&fm=jpg&_gl=1*rk9afu*_ga*NDA1MTY1MTA2LjE2OTIxNzU2OTM.*_ga_8JE65Q40S6*MTY5MjE3NTY5My4xLjEuMTY5MjE3NTczNC4wLjAuMA..'
                    }, 
                    {
                        "question": "What are the Business Units within Homecare ?",
                        "answer": "The given <content> & **#^#()<>)#*# does not provide information about the specific Business Units within Homecare.",
                        "chart" : r'https://images.pexels.com/photos/6476589/pexels-photo-6476589.jpeg?cs=srgb&dl=pexels-mikael-blomkvist-6476589.jpg&fm=jpg&_gl=1*rk9afu*_ga*NDA1MTY1MTA2LjE2OTIxNzU2OTM.*_ga_8JE65Q40S6*MTY5MjE3NTY5My4xLjEuMTY5MjE3NTczNC4wLjAuMA..'
                    }
                ]
            }
        }
        orm_mode = True

