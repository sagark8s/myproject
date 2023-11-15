import os
import json
import subprocess
import requests
from datetime import datetime


from random import randint
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
#import docx2pdf 

from utils.utils import generate_response_chart

#-------------------------------------
#   Save Report based on the chat parameters
#-------------------------------------
class GenerateReport_With_Chart:
    def __init__(self, file_type='pdf'):
        self.file_type      = file_type
        self.current_dir    = os.getcwd()
        self.report_folder  = f'{self.current_dir}/assets/reports'        
        self.report_template = f'{self.current_dir}/assets/report_template/unilever_report.docx'
       
    #-------------------------------------------------
    #   Generate Repor paramters (questions/responses)
    #-------------------------------------------------
    def populate_data(self, payload):

        queries = []

        randno = randint(100_000, 999_999)
        report_file = f'{self.report_folder}/Unica_ChatReport_{randno}.docx'
        doc = DocxTemplate(self.report_template)

        for ind in payload.queries:

            chart_data = self.save_image(ind.chart)

            temp = {}
            temp['question'] = ind.question
            temp['answer'] = ind.answer
  
            if chart_data:
                temp['chart_image'] = InlineImage(doc, chart_data, width=Mm(100))

            queries.append(temp)

        report_param = {}
        report_param['queries'] = queries
        report_param['report_generation_date'] = datetime.today().strftime('%d %b, %Y')
        
        doc.render(report_param,  autoescape=True)

        if not os.path.exists(self.report_folder):
            os.makedirs(self.report_folder)
       
        doc.save(report_file)
        pdf_report_file = self.convert_doc_pdf(report_file)

        if pdf_report_file is not None:            
            os.remove(report_file) # Delete the Doc File

        return pdf_report_file



    #--------------------------------------
    #   Assumption:
    #   1. Image will be a URL
    #--------------------------------------
    def save_image(self, image_url):
        filepath = None
        if image_url:
            
            page = requests.get(image_url)

            randno = randint(100_000, 999_999)
            f_name = f"{self.report_folder}/chart_{randno}.png"
        
            with open(f_name, 'wb') as f:
                f.write(page.content)

            filepath = f_name
        
        return filepath


    
    #-------------------------------------------------
    #   Convert Word to PDF
    #-------------------------------------------------
    def convert_doc_pdf(self, doc_file):
        
        pdf_report_file = None

        pdf_report_file1 = doc_file.replace('.docx', '.pdf')
        
        # docx2pdf.convert(doc_file, pdf_report_file1)

        # if os.path.exists(pdf_report_file1): 
        #     pdf_report_file  = pdf_report_file1

        env = os.environ.copy()
        command = ["lowriter", "--headless", "--convert-to", "pdf",  '--outdir', self.report_folder, doc_file]
        p=subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

        exit_code = p.returncode #Typically 0
       
        if not exit_code:
            pdf_report_file1 = doc_file.replace('.docx', '.pdf')
            if os.path.exists(pdf_report_file1): 
                pdf_report_file  = pdf_report_file1

        return pdf_report_file
