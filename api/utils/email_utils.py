import os
from typing import List
from random import randint
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from config.config import settings


class SendEmail_Attachments:
    def __init__(self, email: List[EmailStr]):
        self.email_lst = email
        self.current_dir    = os.getcwd()
        self.report_folder  = f'{self.current_dir}/assets/reports'
        self.attachment_folder  = f'{self.current_dir}/assets/reports'

    #-------------------------------
    #   Send email asynchronously
    #-------------------------------
    async def send_mail(self, subject, email_message, files=[]):
        # Define the config
        success = False

        conf = ConnectionConfig(
            MAIL_USERNAME = settings.EMAIL_USERNAME,
            MAIL_PASSWORD = settings.EMAIL_PASSWORD,
            MAIL_FROM = settings.EMAIL_FROM,
            MAIL_PORT = settings.EMAIL_PORT,
            MAIL_SERVER = settings.EMAIL_HOST,
            MAIL_FROM_NAME=settings.EMAIL_USERNAME,
            MAIL_STARTTLS = True,
            MAIL_SSL_TLS = False,
            USE_CREDENTIALS = True,
            VALIDATE_CERTS = True
        )

        attachments = []
        for file in files:
            if file.filename:
                attachment_file = f'{self.report_folder}/report_{randint(1000_0000, 9999_9999)}_{file.filename}'
                with open(attachment_file, 'wb') as fp:
                    fp.write(await file.read())
                    attachments.append(attachment_file)

        message = MessageSchema(subject=subject, recipients=self.email_lst, body=email_message, subtype=MessageType.plain, attachments=attachments )

        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message)
        success = True

        return success
