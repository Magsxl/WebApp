from flask import Flask, make_response, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mgasxl:Najlepszy@magsxl.mysql.pythonanywhere-services.com/magsxl$ankieta'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "sekretny klucz"

db = SQLAlchemy(app)
currID = 0

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

class Pytania(db.Model):
    __abstract__ = True
    ID_pytania = db.Column(db.Integer, primary_key=True)
    Nr_Pytania = db.Column(db.Integer, nullable=False)
    Odpowiedz = db.Column(db.String(200), nullable=False)

class Pytania1_4(Pytania, db.Model):
    Person_ID = db.Column(db.Integer, db.ForeignKey('ankietowany.ID'), nullable=False)

class Pytania5_12(Pytania, db.Model):
    Person_ID = db.Column(db.Integer, db.ForeignKey('ankietowany.ID'), nullable=False)

class Pytania13_15(Pytania, db.Model):
    Person_ID = db.Column(db.Integer, db.ForeignKey('ankietowany.ID'), nullable=False)

class ankietowany(db.Model):
    __tablename__ = 'ankietowany'
    ID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.String(200), nullable = False)
    Wiek = db.Column(db.Integer, nullable=False)
    Plec = db.Column(db.String(200), nullable=False)
    Pochodzenie = db.Column(db.String(200), nullable=False)
    Zawod = db.Column(db.String(200), nullable=True)
    Timestamp = db.Column(db.DateTime, default=datetime.now)
    question1_4 = db.relationship('Pytania1_4', backref='ankietowany', lazy=True)
    question5_9 = db.relationship('Pytania5_12', backref='ankietowany', lazy=True)
    question10_15 = db.relationship('Pytania13_15', backref='ankietowany', lazy=True)

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
        count = ankietowany.query.count()
        resp = make_response(redirect(url_for('poll_page')))
        resp.set_cookie('userID', str(count))
        return resp

@app.route('/poll', methods=['GET', 'POST'])
def poll_page():
    dy = "Zdecydowanie tak"
    my = "Raczej tak"
    idk = "Nie wiem"
    mn = "Raczej nie"
    dn = "Zdecydowanie nie"
    currID = request.cookies.get('userID')
    if request.method == 'GET':
        if currID is not None:
            return render_template('poll.html', dyes=dy, myes=my, idk=idk, mno=mn, dno=dn)
        else:
            return render_template('500.html')
    if request.method == 'POST':   
        myDict = dict(request.form)
        i = 0
        for key in myDict:
            i += 1
            questionDict["pytanie" + str(i)] = int(myDict[key][6:])
        for key in questionDict:
            if int(key[7:]) < 5:
                data2 = Pytania1_4(Nr_Pytania=int(key[7:]), Odpowiedz=questionDict[key], Person_ID=currID)
                db.session.add(data2)
                db.session.commit()
            elif int(key[7:]) < 13:
                data2 = Pytania5_12(Nr_Pytania=int(key[7:]), Odpowiedz=questionDict[key], Person_ID=currID)
                db.session.add(data2)
                db.session.commit()
            elif int(key[7:]) < 16:
                data2 = Pytania13_15(Nr_Pytania=int(key[7:]), Odpowiedz=questionDict[key], Person_ID=currID)
                db.session.add(data2)
                db.session.commit()
        return redirect(url_for('end_page'))

@app.route('/end', methods=['GET'])
def end_page():
    currID = request.cookies.get('userID')
    if request.method == 'GET':
        if currID is not None:
             resp = make_response(render_template('end.html'))
             resp.set_cookie('userID','',expires=0)
             return resp
        else:
            return render_template('500.html')

if __name__ == '__main__':
    app.run(debug=True)
