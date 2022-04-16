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
table_names = ['pytanie_1', 'pytanie_2', 'pytanie_3', 'pytanie_4', 'pytanie_5', 'pytanie_6', 'pytanie_7', 'pytanie_8', 'pytanie_9', 'pytanie_10', 'pytanie_11', 'pytanie_12', 'pytanie_13', 'pytanie_14', 'pytanie_15']

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
    """@declared_attr
    def questions(cls):
        return db.relationship('pytanie', backref='ankietowany', lazy=True)"""



class pytanie(object):
    ID_pytania = db.Column(db.Integer, primary_key=True)
    Odpowiedz = db.Column(db.String(200), nullable=False)
    @declared_attr
    def Person_ID(cls):
        return db.Column(db.Integer, db.ForeignKey('ankietowany.ID'), nullable=False)

for name in table_names:
    type(name.title(), (pytanie, db.Model), {'__tablename__' : name})

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
        dataPyt = table_names[0](Odpowiedz = dyes)
    return render_template('poll.html', dyes = dy, myes = my, idk = idk, mno = mn, dno = dn)


if __name__ == '__main__':
    app.run(debug=True)