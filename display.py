import marking as m
import flask as f
import datetime
import os
app = f.Flask(__name__)

"""This python file is the framework for the web page used as a UI for the app.
It should be run as __main__ (which is done through auto-mark.cmd)
"""
root = os.getcwd()

@app.route('/')
def home():
    return f.render_template('home.html')

@app.route('/process')
def process():
    m.main(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    return f.redirect(f.url_for('output'))

@app.route('/output')
def output():
    os.chdir(root)
    maxtime = 0
    recent = ''
    for dir in os.listdir('results'):
        compare = os.path.getctime(root+'/results/'+dir)
        if compare > maxtime:
            maxtime = compare + 0
            recent = f'results/{dir}'
    info = ''
    with open(f'{root}/{recent}/info.txt') as infofile:
        for line in infofile:
            info += str(line)
    """
    scores = f'{recent}/scorecard.txt'
    mistakes = f'{recent}/mistakes.txt'
    log = f'{recent}/log.txt'
    """

    return f.render_template('output.html', info=info)

if __name__ == '__main__':
    app.run(debug=True)
