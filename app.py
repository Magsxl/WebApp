from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
import pymysql
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Najlepszy@localhost/ankieta'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "sekretny klucz"
db = SQLAlchemy(app)

table_names = ['pytanie1', 'pytanie2', 'pytanie3', 'pytanie4', 'pytanie5', 'pytanie6', 'pytanie7', 'pytanie8', 'pytanie9', 'pytanie10', 'pytanie11', 'pytanie12', 'pytanie13', 'pytanie14', 'pytanie15']

# 1 = dyes, 2 = myes, 3 = idk, 4 = mno, 5 = dno
questionDict = {
    "pytanie1": 0,
    "pytanie2": 0,
    "pytanie3": 0,
    "pytanie4": 0,
    "pytanie5": 0,
    "pytanie6": 0,
    "pytanie7": 0,
    "pytanie8": 0,
    "pytanie9": 0,
    "pytanie10": 0,
    "pytanie11": 0,
    "pytanie12": 0,
    "pytanie13": 0,
    "pytanie14": 0,
    "pytanie15": 0,
}

class ankietowany(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.String(200), nullable = False)
    Wiek = db.Column(db.Integer, nullable=False)
    Plec = db.Column(db.String(200), nullable=False)
    Pochodzenie = db.Column(db.String(200), nullable=False)
    Zawod = db.Column(db.String(200), nullable=True)
    Timestamp = db.Column(db.DateTime, default=datetime.now)
    for name in table_names:
        question = db.relationship(name.title(), backref='ankietowany', lazy=True)

class pytanie(object):
    ID_pytania = db.Column(db.Integer, primary_key=True)
    Odpowiedz = db.Column(db.String(200), nullable=False)
    @declared_attr
    def Person_ID(cls):
        return db.Column(db.Integer, db.ForeignKey('ankietowany.ID'), nullable=False)

def initDB(): 
    for name in table_names:
        type(name.title(), (pytanie, db.Model), {'__tablename__' : name})

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        status = request.form['status']
        age = request.form['age']
        sex = request.form['sex']
        place = request.form['place']
        job = request.form['job']
        now = datetime.now()
        data = ankietowany(Status = status, Wiek = age, Plec = sex, Pochodzenie = place, Zawod = job, Timestamp = now)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('poll_page'))


@app.route('/poll', methods=['GET', 'POST'])
def poll_page():
    dy = "Zdecydowanie tak"
    my = "Raczej tak"
    idk = "Nie wiem"
    mn = "Raczej nie"
    dn = "Zdecydowanie nie"
    if request.method == 'GET':
        return render_template('poll.html', dyes=dy, myes=my, idk=idk, mno=mn, dno=dn)
    if request.method == 'POST':   
        myDict = dict(request.form)
        i = 0
        for key in myDict:
            i += 1
            questionDict["pytanie" + str(i)] = int(myDict[key][6:])
        for key in questionDict:
            data = key(ODPOWIEDZ=questionDict[key])


if __name__ == '__main__':
    initDB()
    app.run(debug=True)