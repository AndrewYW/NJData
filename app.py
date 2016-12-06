from flask import Flask, render_template


app = Flask(__name__)

# db = MySQLdb.connect(host="localhost", user="root", passwd="root321", db="NJData")
# cur = db.cursor()

@app.route("/")
def main():
    return render_template('index.html')
"""
@app.route("/predictions")
def predict():
    cur = db.execute('select County, Projected_Winner from NJ2016')
    ours = cur.fetchall()
    cur = db.execute('select County, Projected_Winner, Winner from NJ2016 Where Projected_Winner = Winner')
    right = cur.fetchall()
    cur = db.execute('select County, Projected_Winner, Winner from NJ2016 where Projected_Winner <> Winner')
    wrong = cur.fetchall()
    return render_template('predictions.html', ours, right, wrong)
"""
if __name__ == "__main__":
    app.run()
