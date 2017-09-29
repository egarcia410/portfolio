import os

import tornado.ioloop
import tornado.web

from jinja2 import Environment, PackageLoader, select_autoescape

PORT = int(os.environ.get('PORT', '8888'))

ENV = Environment(
    loader=PackageLoader('portfolio'),
    autoescape=select_autoescape(['html', 'xml'])
)

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
