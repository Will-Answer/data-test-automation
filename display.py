import marking as m
import flask as f
import datetime
app = f.Flask(__name__)

@app.route('/')
def home():
    return f.render_template('home.html')

@app.route('/process')
def process():
    m.main(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    return f.redirect(f.url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
