from flask import Flask, render_template, request, url_for, redirect,session
from flask_sqlalchemy import SQLAlchemy
import json 

app = Flask(__name__)
app = Flask(__name__,template_folder='template')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

data = ["https://duniapendidikan.co.id/wp-content/uploads/2018/12/rakyat-bali.jpg",
      "https://tatkala.co/wp-content/uploads/2021/01/mardi-yasa.-satua-bali.png",
      "https://seringjalan.com/wp-content/uploads/2021/04/Cerita-Manik-Angkeran-816x577.jpg"]

class Author(db.Model):
  id_auth = db.Column(db.Integer,db.Sequence('seq_reg_id', start=1, increment=1), primary_key = True)
  username = db.Column(db.String(50), index = True, unique = True)
  nama_lengkap = db.Column(db.String(150), index = True, unique = False)
  email = db.Column(db.String(150), index = True, unique = True)
  password = db.Column(db.String(150), index = True, unique = False)
  satwa = db.relationship('Satwa', backref='author', lazy='dynamic')

  def __repr__(self):
    return '<Author %r>' % self.nama_lengkap
  
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Satwa(db.Model):
  id_satwa = db.Column(db.Integer,db.Sequence('seq_reg_id', start=1, increment=1), primary_key = True)
  satwa_judul = db.Column(db.String(150), index = True, unique = False)
  satwa_text = db.Column(db.String(50000), index = True, unique = False)
  satwa_ringkas = db.Column(db.String(500), index = True, unique = False)
  satwa_tokoh = db.Column(db.String(150), index = True, unique = False)
  satwa_gambar = db.Column(db.String(500), index = True, unique = False)
  penulis_id = db.Column(db.Integer, db.ForeignKey('author.id_auth'))

  def __repr__(self):
    return '<Judul %r>' % self.satwa_judul
  
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

#Routing
@app.route('/')
def index():
  satwa = Satwa.query.all()
  satwa_dict = {}
  no = 0
  for s in satwa:
    satwa_dict[no] = {
      "id":s.id_satwa,
      "judul":s.satwa_judul,
      "text":s.satwa_text,
      "gambar":s.satwa_gambar
    }
    no+=1
  return render_template("index.html", satwaData = str(json.dumps(satwa_dict)))

@app.route('/satwa/<id_satwa>')
def satwa(id_satwa):
  return render_template("read_page.html")

@app.route('/satwa_nav')
def satwa_nav():
  return render_template("component/leftbar.html")

@app.route('/form_sign')
def form_sign():
  return render_template("component/form_sign.html")

@app.route('/satwa_card/<no>/<id>', methods=['GET'])
def satwa_card(no,id):
  satwa = Satwa.query.get(id)
  return render_template("component/card_satwa.html", satwa = satwa, no = no)

@app.route('/satwa_reading')
def satwa_reading():
  satwa = Satwa.query.get(1)
  return render_template("component/reading_satwa.html", satwa = satwa)

#Function
@app.route('/sign_in',methods=['POST'])
def sign_in():
  username=request.form['user_in']
  password=request.form['pass_in']
  auth = Author.query.get(username)
  if auth is None:
    return "1"
  elif auth.password == password:
    return str(json.dumps(auth.as_dict()))
  else:
    return "2"

if __name__=='__main__':
    app.run()