import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        link = request.form['link']
        if not link:
            flash('Link is required!')
        else:
            print(link)
            # wks = client.open_by_url(link)
            # val = wks.get_worksheet('A1').cell
            # print(val)
            conn = get_db_connection()
            conn.execute('INSERT INTO links (link) VALUES (?)', (link,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('index.html')

