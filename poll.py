from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Najlepszy@localhost/ankieta'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "sekretny klucz"
db = SQLAlchemy(app)


class ankietowany(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.String(200), nullable = False)
    Wiek = db.Column(db.Integer, nullable=False)
    Plec = db.Column(db.String(200), nullable=False)
    Pochodzenie = db.Column(db.String(200), nullable=False)
    Zawod = db.Column(db.String(200), nullable=True)
    Timestamp = db.Column(db.DateTime, default=datetime.now)

class pytanie_1(db.Model):
    ID_pytania = db.Column(db.Integer, primary_key=True)
    Odpowiedz = db.Column(db.String(200), nullable=False)
    PersonID = db.Column(db.Integer, db.ForeignKey('ankietowany'),nullable=False)
    Person = db.relationship('ankietowany',backref=db.backref('pytanie', lazy=True))

@app.route('/', methods=['GET', 'POST'])
def home_page():
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

    return render_template('index.html')


@app.route('/poll', methods=['GET', 'POST'])
def poll_page():
    dy = "Zdecydowanie tak"
    my = "Raczej tak"
    idk = "Nie wiem"
    mn = "Raczej nie"
    dn = "Zdecydowanie nie"
    if request.method == 'POST':   
        dyes = request.form['optradio1.dyes']
        myes = request.form['optradio1.myes']
        idk1 = request.form['optradio1.idk']
        mno = request.form['optradio1.mno']
        dno = request.form['optradio1.dno']
        dataPyt = pytanie_1()
    return render_template('poll.html', dyes = dy, myes = my, idk = idk, mno = mn, dno = dn)