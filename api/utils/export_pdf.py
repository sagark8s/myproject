import os
import subprocess
from datetime import datetime


from random import randint
from docxtpl import DocxTemplate
import docx2pdf 


#-------------------------------------
#   Save Report based on the chat parameters
#-------------------------------------
class GenerateReport:
    def __init__(self, file_type='pdf'):
        self.file_type      = file_type
        self.current_dir    = os.getcwd()
        self.report_folder  = f'{self.current_dir}/assets/reports'        
        self.report_template = f'{self.current_dir}/assets/report_template/unilever_report.docx'
       

    #-------------------------------------------------
    #   Populate paramters (questions/responses)
    #-------------------------------------------------
    def populate_data(self, param:dict):

        #print(param)

        randno = randint(100_000, 999_999)
        report_file = f'{self.report_folder}/Unilever_ChatReport_{randno}.docx'
        doc = DocxTemplate(self.report_template)

        report_param = {}
        report_param.update(param)
        report_param['report_generation_date'] = datetime.today().strftime('%d %b, %Y')

        doc.render(report_param,  autoescape=True)

        if not os.path.exists(self.report_folder):
            os.makedirs(self.report_folder)
       
        doc.save(report_file)
        pdf_report_file = self.convert_doc_pdf(report_file)

        if pdf_report_file is not None:            
            os.remove(report_file) # Delete the Doc File

        return pdf_report_file

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






    