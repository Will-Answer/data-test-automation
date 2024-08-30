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
    global recent
    os.chdir(root)
    maxtime = 0
    recent = ''
    for dir in os.listdir('results'):
        compare = os.path.getctime(root+'/results/'+dir)
        if compare > maxtime:
            maxtime = compare + 0
            recent = f'results/{dir}'
    info = readall(f'{recent}\\info.txt')
    return f.render_template('output.html', info=info, dir=recent)

@app.route('/output/scorecard')
def scores():
    return f.send_file(f'{recent}\\scorecard.txt')

@app.route('/output/mistakes')
def mistakes():
    return f.send_file(f'{recent}\\mistakes.txt')

@app.route('/output/log')
def log():
    return f.send_file(f'{recent}\\log.txt')

@app.route('/exit')
def appexit():
    os._exit(0)

def readall(file):
    info = ''
    with open(file) as opened:
        for line in opened:
            info += str(line)
    return info

if __name__ == '__main__':
    app.run(debug=True)
