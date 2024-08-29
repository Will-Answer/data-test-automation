import marking as m
import flask as f
app = f.Flask(__name__)

@app.route('/')
def home():
    return f.render_template('home.html')

@app.route('/process')
def process():
    m.main()
    return f.redirect(f.url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
