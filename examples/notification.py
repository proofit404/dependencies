from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from uuid import uuid4

from dependencies import Injectable, Injector
from redis import StrictRedis


settings = {
    'redis': {
        'host': 'localhost',
        'port': 6379,
    },
    'email': {
        'support': {
            'address': 'support@service.com',
        },
        'relay': {
            'host': 'localhost',
            'port': 8025,
        },
    },
}


def uuid_generator():
    return uuid4().hex


class RedisStore(Injectable):

    def write(self, **kwargs):
        id = self.generate_id()
        redis = self.get_connection()
        redis.hmset(id, **kwargs)
        return id

    def get_connection(self):
        if not hasattr(self, 'connection'):
            conf = self.settings['redis']
            address = (conf['host'], conf['port'])
            self.connection = StrictRedis(address)
        return self.connection


class RedisDB(Injector, RedisStore):
    settings = settings
    generate_id = uuid_generator


class SMTPSender(Injectable):

    def send(self, recipient, message):
        address = self.settings['email']['support']['address']
        relay_host = self.settings['email']['relay']['host']
        relay_port = self.settings['email']['relay']['port']
        data = self.get_data(address, recipient, message)
        with SMTP(relay_host, relay_port) as smtp:
            smtp.sendmail(address, [recipient], data)

    def get_data(self, address, recipient, message):
        email = MIMEMultipart()
        email['From'] = address
        email['To'] = recipient
        html = MIMEText(message, 'html')
        email.attach(html)
        return email.as_string()


class Sender(Injector, SMTPSender):
    settings = settings


class RegisterUser(Injectable):

    def execute(self, username, email):
        id = self.db.write(username=username, email=email)
        message = self.render_notification(id, username)
        self.sender.send(email, message)

    def render_notification(self, id, username):
        return """
        <html>
            <head>
                <title>Hello, {username}.</title>
            </head>
            <body>
                <a href="http://www.service.com/profile/{id}/">Your profile.</a>
            </body>
        </html>
        """.format(id=id, username=username)


class UserRegistration(Injector):
    db = RedisDB()
    sender = Sender()


UserRegistration().execute('me', 'me@gmail.com')
