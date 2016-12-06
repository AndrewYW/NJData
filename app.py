from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = '192.34.63.230'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root321'
app.config['MYSQL_DB'] = 'NJData'
mysql = MySQL(app)

@app.route("/")
def main():
    cur = mysql.connection.cursor()
    return render_template('index.html')

@app.route("/predictions")
def predict():
    cur = db.execute('select County, Projected_Winner from NJ2016')
    ours = cur.fetchall()
    cur = db.execute('select County, Projected_Winner, Winner from NJ2016 Where Projected_Winner = Winner')
    right = cur.fetchall()
    cur = db.execute('select County, Projected_Winner, Winner from NJ2016 where Projected_Winner <> Winner')
    wrong = cur.fetchall()
    return render_template('predictions.html', ours, right, wrong)
if __name__ == "__main__":
    app.run()
