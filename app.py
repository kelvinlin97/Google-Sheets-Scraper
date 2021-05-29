from os import link
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import guess
import json
import plotly.express as px
import plotly.graph_objects as go


app = Flask(__name__)
app.config['SECRET_KEY'] = 'alphabetically'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/about')
def about():
    return render_template('about.html')

#OAuth
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
            x, y = getLinkValues(link)
            # createBarGraph(x, y)
            conn = get_db_connection()
            conn.execute('INSERT INTO links (link) VALUES (?)', (link,))
            conn.commit()
            conn.close()
    return render_template('index.html')

def getLinkValues(url):
    wks = client.open_by_url(url)
    columns = wks.get_worksheet(0)
    sheetLength = wks.get_worksheet(0).col_count

    #TODO: Add option to select sheet to view

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

    fig = go.Figure(data=[go.Table(header=dict(values=columnHeaders),
                 cells=dict(values=formatAppearances))
                     ])
    fig.show()

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


#TODO(User): Add user login --> user can sign up and see their past sheets

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

#TODO: Create sheets assessment (table with each column and their datatype) and render on page

# -Deploy app
# -Add user login (see past sheets)
# -Get graph to show on click
# 	-User has to select sheet of file to check, input
# -Style page


