from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from dependencies import Injector


settings = {
    'support_address': 'user@gmail.com',
    'support_user': 'user',
    'support_passwd': 'secret',
    'smtp_host': 'smtp.gmail.com',
    'smtp_port': 587,
}


class SMTPSender:

    def __init__(self, support_address, support_user, support_passwd, smtp_host, smtp_port):

        self.from_address = support_address
        self.user = support_user
        self.passwd = support_passwd
        self.host = smtp_host
        self.port = smtp_port

    def send(self, recipient, message):
        data = self.prepare(recipient, message)
        with SMTP(self.host, self.port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(self.user, self.passwd)
            smtp.sendmail(self.from_address, [recipient], data)

    def prepare(self, recipient, message):
        email = MIMEMultipart()
        email['From'] = self.from_address
        email['To'] = recipient
        html = MIMEText(message, 'html')
        email.attach(html)
        return email.as_string()


class EmailTemplate:

    def render(self, username):
        return """
        <html>
            <head>
            </head>
            <body>
                Hello, {username}.
            </body>
        </html>
        """.format(username=username)


class NotificationHandler:

    def __init__(self, template, sender):

        self.template = template
        self.sender = sender

    def handle(self, recipient):

        username = self.get_username(recipient)
        message = self.template.render(username)
        self.sender.send(recipient, message)

    def get_username(self, recipient):

        return recipient.split('@')[0]


class App(Injector):
    handler = NotificationHandler
    template = EmailTemplate
    sender = SMTPSender


AppContainer = App.let(**settings)

AppContainer.handler.handle('tagretuser@gmail.com')
