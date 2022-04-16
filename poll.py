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


class ankietowany(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.String(200), nullable = False)
    Wiek = db.Column(db.Integer, nullable=False)
    Plec = db.Column(db.String(200), nullable=False)
    Pochodzenie = db.Column(db.String(200), nullable=False)
    Zawod = db.Column(db.String(200), nullable=True)
    Timestamp = db.Column(db.DateTime, default=datetime.now)
    @declared_attr
    def questions(cls):
        return db.relationship('pytanie', backref='ankietowany', lazy=True)

class pytanie(object):
    ID_pytania = db.Column(db.Integer, primary_key=True)
    Odpowiedz = db.Column(db.String(200), nullable=False)
    @declared_attr
    def Person_ID(cls):
        return db.Column(db.Integer, db.ForeignKey('ankietowany.ID'),nullable=False)

class pytanie_1(pytanie, db.Model):
    __tablename__ = 'Pytanie_1'

class pytanie_2(pytanie, db.Model):
    __tablename__ = 'Pytanie_2'

class pytanie_3(pytanie, db.Model):
    __tablename__ = 'Pytanie_3'

class pytanie_4(pytanie, db.Model):
    __tablename__ = 'Pytanie_4'

class pytanie_5(pytanie, db.Model):
    __tablename__ = 'Pytanie_5'

class pytanie_6(pytanie, db.Model):
    __tablename__ = 'Pytanie_6'

class pytanie_7(pytanie, db.Model):
    __tablename__ = 'Pytanie_7'

class pytanie_8(pytanie, db.Model):
    __tablename__ = 'Pytanie_8'

class pytanie_9(pytanie, db.Model):
    __tablename__ = 'Pytanie_9'

class pytanie_10(pytanie, db.Model):
    __tablename__ = 'Pytanie_10'

class pytanie_11(pytanie, db.Model):
    __tablename__ = 'Pytanie_11'

class pytanie_12(pytanie, db.Model):
    __tablename__ = 'Pytanie_12'

class pytanie_13(pytanie, db.Model):
    __tablename__ = 'Pytanie_13'

class pytanie_14(pytanie, db.Model):
    __tablename__ = 'Pytanie_14'

class pytanie_15(pytanie, db.Model):
    __tablename__ = 'Pytanie_15'


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