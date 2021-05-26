import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'alphabetically'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#TODO(Bugfix): About page routing
@app.route('/#')
def about():
    return render_template('about.html')

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        link = request.form['link']

        if not link:
            flash('Link is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO links (link) VALUES (?)', (link,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('index.html')

