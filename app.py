from flask import Flask, render_template
from sucuri import rendering
from bs4 import BeautifulSoup
from pcml import *

app = Flask(__name__)


@app.route('/post')
def vuetify():
    html = rendering.template('templates/test.html')
    #html = render_template_string(template)
    return render_template(
        '_base.html', html=html)

@app.route('/idea')
def idea():
    html = rendering.template('templates/idea.html')
    return render_template(
        '_base_primer.html', html=html)

@app.route("/pcml")
def pcml():
    with open('templates/idea.pcml', encoding='utf-8') as f:
        content = f.read()
        phtml = get_pretty_html(content)
        return render_template(
            '_base.html', html=phtml)

@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
