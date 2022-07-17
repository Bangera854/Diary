
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
db=SQLAlchemy(app)

class Diary(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),unique=True, nullable=False)
    desc = db.Column(db.String(500),unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Todo("{self.sno}","{self.title}")'


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        title=request.form['title']
        desc=request.form['desc']
        diary=Diary(title=title,desc=desc)
        db.session.add(diary)
        db.session.commit()
    return render_template('index.html')

@app.route('/pages')
def pages():
    allreq = Diary.query.all()
    print(allreq)
    return render_template('pages.html',allreq=allreq)

@app.route('/settings')
def settings():
    return '<h4> nothing here </h4>'

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title=request.form['title']
        desc=request.form['desc']
        diary=Diary.query.filter_by(sno=sno).first()
        diary.title=title
        diary.desc=desc
        db.session.add(diary)
        db.session.commit()
        return redirect('/pages')
    diary=Diary.query.filter_by(sno=sno).first()
    return render_template('update.html',diary=diary)

@app.route('/delete/<int:sno>')
def delete(sno):
    diary=Diary.query.filter_by(sno=sno).first()
    db.session.delete(diary)
    db.session.commit()
    return redirect('/pages')

if __name__ == "__main__":
    app.run(debug=True)