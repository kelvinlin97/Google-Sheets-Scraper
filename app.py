from os import link
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import guess
import json
import plotly.express as px
import plotly.graph_objects as go
from google.oauth2 import service_account
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'alphabetically'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/about')
def about():
    return render_template('about.html')

####OAuth####

scope = ['https://spreadsheets.google.com/feeds']

json_str = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
gcp_project = os.environ.get('salty-woodland-35192')

#Deployment
if json_str is not None:
    json_data = json.loads(json_str)
    # json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')
    credentials = ServiceAccountCredentials.from_json(json_data)

#Development
else:
    credentials = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)

client = gspread.authorize(credentials)

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        link = request.form['link']
        sheetNumber = request.form['sheet']
        if not link:
            flash('Error: Link is required!')
        elif not sheetNumber:
            flash('Error: Sheet number must be entered')
        else:
            getLinkValues(link, sheetNumber)
            conn = get_db_connection()
            conn.execute('INSERT INTO links (link) VALUES (?)', (link,))
            conn.commit()
            conn.close()
    return render_template('index.html')

def getLinkValues(url, sheetNum):
    sheetNum = int(sheetNum)
    wks = client.open_by_url(url)
    columns = wks.get_worksheet(sheetNum)

    if not columns:
         flash('Error: Sheet number entered was out of range')
    else:
        sheetLength = wks.get_worksheet(sheetNum).col_count

        data = [[]]

        for i in range(1, sheetLength):
            dataType = colTypeGuess(columns.col_values(i))
            data[0].append(dataType)

        x, y = formatData(data[0])
        return x, y

def createTable(columnHeaders, columnValues):
    columnNumber = 1
    formatAppearances = []
    for columnValue in columnValues:
        formattedHeader = excelFormat(columnNumber)
        columnHeaders.append('Column ' + formattedHeader)
        formatAppearances.append([columnValue])
        columnNumber += 1

    fig = go.Figure(data=[go.Table(header=dict(values=columnHeaders), cells=dict(values=formatAppearances))])

    fig.show()

    flash('Sheet data should have loaded in another page, to analyze another sheet change the sheet number!')

def excelFormat(n):
    abc="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ans=""
    while n:
        n=n-1
        ans=abc[n%26]+ans
        n=n//26
    return ans

def formatData(data):
    createTable([], data)
    formattedData = {}

    for type in data:
        if "Unable to type guess with certainty, most prevalent data type was:" in type:
            type = type[67: len(type)]
        if "Column is empty!" in type:
            type = "Blank"
        formattedData[type] = formattedData.get(type, 0) + 1

    x = formattedData.keys()
    y = formattedData.values()

    return list(x), list(y)

def colTypeGuess(column):
    count = {}
    #Ignore label of column (first cell)
    for cell in column[1:]:
        cellType = guess.cellType(cell)
        if cellType not in ('blank', None):
            count[cellType] = count.get(cellType, 0) + 1

    if not count:
        return 'Column is empty!'

    #If 95% of column values are one type, make a guess that column is that type. Otherwise, return error
    totalVTC = 0

    for cellCount in count:
       totalVTC += count[cellCount]


    maxKey = max(count, key=count.get)
    highestVal = max(count.values())
    #In the case of multiple data types, return error
    if highestVal/totalVTC >= .95:
        return maxKey
    else:
        return 'Unable to type guess with certainty, most prevalent data type was: ' + maxKey


