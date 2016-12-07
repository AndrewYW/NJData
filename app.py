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
    return render_template('index.html')

@app.route("/predictions")
def predict():
    cur = mysql.connection.cursor()
    cur.execute('select County, Projected_Winner from NJ2016')
    ours = cur.fetchall()
    cur.execute('select County, Projected_Winner, Winner from NJ2016 Where Projected_Winner = Winner')
    right = cur.fetchall()
    cur.execute('select County, Projected_Winner, Winner from NJ2016 where Projected_Winner <> Winner')
    wrong = cur.fetchall()
    return render_template('predictions.html', **locals())

@app.route("/margins")
def margins():
    cur = mysql.connection.cursor()
    cur.execute('select cur.County , 2004NJ.PERCENT_DEM -2004NJ.PERCENT_REP AS DEM_2004_margin ,2008NJ.PERCENT_DEM -2008NJ.PERCENT_REP AS DEM_2008_margin ,2012NJ.PERCENT_DEM -2012NJ.PERCENT_REP AS DEM_2012_margin ,cur.`%Dem` - cur.`%Rep` AS DEM_2016_margin FROM NJ2016 cur, 2004NJ, 2008NJ, 2012NJ WHERE cur.County = 2004NJ.COUNTY AND 2008NJ.COUNTY = 2012NJ.COUNTY AND 2008NJ.COUNTY = cur.County')
    return render_template('margins.html', margins = cur.fetchall())

@app.route("/popgrowth")
def topPG():
    cur = mysql.connection.cursor()
    cur.execute('SELECT cur.County, 100 *2012NJ.TOTAL_POPULATION / 2004NJ.TOTAL_POPULATION -100 as PERCENT_POP_GROWTH, cur.Winner FROM NJ2016 cur, 2004NJ, 2012NJ WHERE cur.County = 2012NJ.COUNTY and cur.County = 2004NJ.COUNTY GROUP BY cur.Winner , cur.County , PERCENT_POP_GROWTH ORDER    BY    PERCENT_POP_GROWTH DESC limit 5')
    top5 = cur.fetchall()
    cur.execute('SELECT cur.County, 100 * 2012NJ.TOTAL_POPULATION / 2004NJ.TOTAL_POPULATION - 100 as PERCENT_POP_GROWTH, cur.Winner FROM NJ2016 cur, 2004NJ, 2012NJ WHERE cur.County = 2012NJ.COUNTY and cur.County = 2004NJ.COUNTY GROUP BY cur.Winner , cur.County , PERCENT_POP_GROWTH ORDER    BY    PERCENT_POP_GROWTH ASC limit 5')
    bottom5 = cur.fetchall()
    return render_template('popgrowth.html', **locals())

@app.route("/income")
def income():
    cur = mysql.connection.cursor()
    cur.execute("SELECT cur.County, cur.Winner, 100 * r1.PERCAPITA_INCOME / l1.PERCAPITA_INCOME -100  AS PERCENT_PERCAPITA_INCOME_GROWTH FROM NJ2016 cur, 2004NJ l1, 2004NJ l2, 2012NJ r1 , 2012NJ r2 WHERE cur.County <> 'Statewide' AND l2.COUNTY = 'Statewide' AND r2.COUNTY = 'Statewide' AND cur.County = l1.COUNTY AND cur.County = r1.COUNTY AND r1.PERCAPITA_INCOME / l1.PERCAPITA_INCOME > r2.PERCAPITA_INCOME / l2.PERCAPITA_INCOME")
    highincome = cur.fetchall()
    cur.execute("SELECT cur.County, cur.Winner, 100 * r1.PERCAPITA_INCOME / l1.PERCAPITA_INCOME - 100 AS PERCENT_PERCAPITA_INCOME_GROWTH FROM NJ2016 cur, 2004NJ l1, 2004NJ l2, 2012NJ r1 , 2012NJ r2 WHERE cur.County <> 'Statewide' AND l2.COUNTY = 'Statewide' AND r2.COUNTY = 'Statewide' AND cur.County = l1.COUNTY AND cur.County = r1.COUNTY AND r1.PERCAPITA_INCOME / l1.PERCAPITA_INCOME < r2.PERCAPITA_INCOME / l2.PERCAPITA_INCOME")
    lowincome = cur.fetchall()
    return render_template('income.html', **locals())
@app.route("/schema")
def schema():
    return render_template('schema.html')

if __name__ == "__main__":
    app.run()
