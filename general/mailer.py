from general.utils import singletone
from logger import push_to_log
from general.config_parser import parser
import os

#--------------------------#e-mailing#------------------------------------------#


import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class mailer(singletone):
    def __init__(self, path = 'config.ini'):
        super().__init__()
        if not self.initialized:
            self.loadconfig(path)
            self.initialized = True
        return

    def loadconfig(self, path):
        if not os.path.exists(path):
            raise ValueError
        parser.instance.parsefile(path)
        for name, value in parser.instance.getSection("smtp"):
            self.__setattr__(name, value)

    def setArgs(self, args):
        if not(args.host is None):
            self.host = args.host
        if not(args.to_addr is  None):
            self.to_addr = args.to_addr
        if not(args.from_addr is  None):
            self.from_addr = args.from_addr
        if not(args.login is None):
            self.login = args.login
        if not(args.password is None):
            self.password = args.password

    @push_to_log
    def send(self, subject, body_text, file):
        header = 'Content-Disposition', 'attachment; filename="%s"' %file
        msg = MIMEMultipart()
        msg["From"] = self.from_addr
        msg["To"] = self.to_addr
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, 'plain'))

        attachment = MIMEBase('application', "octet-stream")
        try:
            with open(file, "rb") as fh:
                data = fh.read()
                attachment.set_payload( data )
                encoders.encode_base64(attachment)
                attachment.add_header(*header)
                msg.attach(attachment)
        except IOError:
            raise ValueError("File not found")

        server = smtplib.SMTP(self.host)
        server.login(self.login, self.password)
        server.sendmail(self.from_addr, self.to_addr.split(), msg.as_string())
        server.quit()