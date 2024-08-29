import marking as m
import flask as f
import datetime
app = f.Flask(__name__)

"""This python file is the framework for the web page used as a UI for the app.
It should be run as __main__ (which is done through auto-mark.cmd)
"""

@app.route('/')
def home():
    return f.render_template('home.html')

@app.route('/process')
def process():
    m.main(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    return f.redirect(f.url_for('output'))

@app.route('/output')
def output():
    return f.render_template('output.html')

if __name__ == '__main__':
    app.run(debug=True)
