from django.template import Engine, Context, Template
import smtplib, ssl
from email.mime import text, multipart, base
from email.encoders import encode_base64
import csv

class TemplateNotSetError(ValueError):
    ...

class InvalidOptionError(ValueError):
    ...

class EmailSender():
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._templateEngine = Engine(dirs=['.'])
        self._template = None
    

    def loadAttachment(self, fileName):
        with open(fileName, "rb") as file:
            attachment = base.MIMEBase("application", "octet-stream")
            attachment.set_payload(file.read())
        encode_base64(attachment)
        attachment.add_header('content-disposition', 'attachment', filename=('utf-8', '', fileName))
        return attachment

    
    def setTemplate(self, templateFileName):
        self._template = self._templateEngine.get_template(templateFileName)


    def sendPlain(self, receiver, subject, content, attachments=[]):
        message = multipart.MIMEMultipart()
        message["Subject"] = subject
        message["From"] = self._username
        message["To"] = receiver

        for attachment in attachments:
            message.attach(self.loadAttachment(attachment))

        SSLContext = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=SSLContext) as server:
            server.login(self._username, self._password)
            server.sendmail(self._username, receiver, message.as_string())

    def renderTemplate(self, context):
        try:
            HTMLContent = self._template.render(Context(context))
        except ValueError:
            raise TemplateNotSetError("You haven't set a template yet")
        return HTMLContent


    def sendFancy(self, receiver, subject, context={}, attachments=[]):
        context["sender"] = self._username
        context["receiver"] = receiver
        context["subject"] = subject
        
        HTMLContent = self.renderTemplate(context)

        message = multipart.MIMEMultipart()
        message["Subject"] = subject
        message["From"] = self._username
        message["To"] = receiver
        message.attach(text.MIMEText(HTMLContent, "html"))

        for attachment in attachments:
            message.attach(self.loadAttachment(attachment))

        SSLContext = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=SSLContext) as server:
            server.login(self._username, self._password)
            server.sendmail(self._username, receiver, message.as_string())


    def sendFromCSV(self, CSVFileName, fancy=False, subject=None):
        with open(CSVFileName, "r") as file:
            for email in csv.DictReader(file):
                try:
                    attachments = [attachmen.strip() for attachment in email["attachments"].split(",")]
                except KeyError:
                    attachments = []
                currentSubject = subject if subject else email["subject"]
                if not fancy:
                    self.sendPlain(email["receiver"], currentSubject, email["content"], attachments)
                else:
                    self.sendFancy(email["receiver"], currentSubject, email, attachments)

