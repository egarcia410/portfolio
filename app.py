from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, render_template

app = Flask(__name__)

# ENV = Environment(loader=FileSystemLoader('./templates'))

# PAGE_LIST = ['home', 'about', 'projects', 'contact',]

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/projects")
def projects():
    return render_template('projects.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')


    # for item in PAGE_LIST:
    #     file_name = item + '.html'
    #     template = ENV.get_template(file_name)
    #     html = template.render()

    #     with open(file_name, 'w') as out_file:
    #         out_file.write(html)

if __name__ == "__main__":
    app.run(debug=True)
