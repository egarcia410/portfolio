import os
import boto3

import tornado.ioloop
import tornado.web

from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape

load_dotenv('.env')

PORT = int(os.environ.get('PORT', '8000'))

ENV = Environment(
    loader=PackageLoader('portfolio'),
    autoescape=select_autoescape(['html', 'xml'])
)

SES_CLIENT = boto3.client(
  'ses',
  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
  region_name="us-west-2"
)

print(os.environ.get('AWS_ACCESS_KEY'), os.environ.get('AWS_SECRET_KEY'))

class TemplateHandler(tornado.web.RequestHandler):
    def render_template (self, tpl, **context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))

class MainHandler(TemplateHandler):
    def get(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("home.html")

class AboutHandler(TemplateHandler):
    def get(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("about.html")

class ProjectsHandler(TemplateHandler):
    def get(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("projects.html")

class ContactHandler(TemplateHandler):
    def get(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("contact.html")

    def post (self):
        name = self.get_body_argument('name')
        email = self.get_body_argument('email')
        text = self.get_body_argument('text')
        
        response = SES_CLIENT.send_email(
        Destination={
            'ToAddresses': ['egarcia410@gmail.com'],
        },
        Message={
            'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': text,
            },
            },
            'Subject': {'Charset': 'UTF-8', 'Data': 'Portfolio Contact'},
        },
        Source='egarcia410@gmail.com',
        )
        messages = 'Thank you, your email has been sent!'
        self.render_template('contact.html', message=messages )

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/about", AboutHandler),
        (r"/projects", ProjectsHandler),
        (r"/contact", ContactHandler),
        (
        r"/static/(.*)",
        tornado.web.StaticFileHandler,
        {'path': 'static'}
        )
    ], autoreload=True)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    
    app = make_app()
    app.listen(PORT, print('Creating magic on port {}'.format(PORT)))
    tornado.ioloop.IOLoop.current().start()
