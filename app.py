import email
from operator import or_
from flask import Flask, render_template, request, url_for, redirect,session
from flask_sqlalchemy import SQLAlchemy
import json 
from static.py.peringkasan_satwa import Sumarize_Bahasa_Bali
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app = Flask(__name__,template_folder='template')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(directory,name_file):
  if name_file not in request.files:
    return False
  file = request.files[name_file]
  if file.filename == '':
    return False
  if file and allowed_file(file.filename):
    app.config['UPLOAD_FOLDER'] = directory
    filename = secure_filename(file.filename)
    formatfile=filename.split('.')
    newfilename=str(uuid.uuid4().hex)+'.'+formatfile[1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename),os.path.join(app.config['UPLOAD_FOLDER'], newfilename))
    return newfilename

class Author(db.Model):
  id_auth = db.Column(db.Integer,db.Sequence('seq_reg_id', start=1, increment=1), primary_key = True)
  username = db.Column(db.String(50), index = True, unique = True)
  nama_lengkap = db.Column(db.String(150), index = True, unique = False)
  email = db.Column(db.String(150), index = True, unique = True)
  password = db.Column(db.String(150), index = True, unique = False)
  gambar = db.Column(db.String(150), index = True, unique = False)
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
      "gambar":s.satwa_gambar,
      "ringkas":s.satwa_ringkas
    }
    no+=1
  return render_template("index.html", satwaData = str(json.dumps(satwa_dict)))

@app.route('/satwa/<id_satwa>')
def satwa(id_satwa):
  satwa = Satwa.query.get(id_satwa)
  return render_template("read_page.html",satwa = satwa)

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

@app.route('/satwa_writing/<id>')
def satwa_writing(id):
  satwa = Satwa.query.filter(Satwa.penulis_id == id).all()
  satwa_dict = {}
  no = 0
  for s in satwa:
    satwa_dict[no] = {
      "id":s.id_satwa,
      "judul":s.satwa_judul,
      "text":s.satwa_text,
      "gambar":s.satwa_gambar,
      "ringkas":s.satwa_ringkas
    }
    no+=1
  return render_template("component/writing_satwa.html", my_satwaData = str(json.dumps(satwa_dict)))

#Function
@app.route('/sign_in',methods=['POST'])
def sign_in():
  username=request.form['user_in']
  password=request.form['pass_in']
  auth = Author.query.filter(Author.username == username).first()
  if auth is None:
    return "1"
  elif auth.password == password:
    return str(json.dumps(auth.as_dict()))
  else:
    return "2"

@app.route('/sign_up',methods=['POST'])
def sign_up():
  username    = request.form['user_up']
  email       = request.form['email_up']
  naleng      = request.form['naleng_up']
  re_password = request.form['repass_up']
  password    = request.form['pass_up']

  if username == "" or email == "" or naleng == "" or password == "" or re_password == "":
    return "4"
  elif password != re_password:
    return "2"
  elif Author.query.filter(Author.username == username).first() is not None:
    return "1"
  elif Author.query.filter(Author.email == username).first() is not None:
    return "3"

  author = Author(username = username , nama_lengkap = naleng, email = email, password = password, gambar = "default.jpg")
  db.session.add(author)
  db.session.commit()

  auth = Author.query.filter(Author.username == username).first()
  return str(json.dumps(auth.as_dict()))

@app.route('/submit_satwa',methods=['POST'])
def submit_satwa():
  judul=request.form['judul_satwa']
  text=request.form['text_satwa']
  kategori=request.form['kategori_satwa']
  penulis = request.form['penulis_satwa']
  
  gambar=upload_image("static/image/satwa_cover","img_satwa")
  satwa_ringkas = Sumarize_Bahasa_Bali(judul,text).sumarize()

  if judul == "" or text == "":
    return "1"
  if not gambar:
    return "2"

  satwa = Satwa(satwa_judul = judul , satwa_text = text, satwa_ringkas = satwa_ringkas, satwa_gambar = gambar, penulis_id = penulis)
  db.session.add(satwa)
  db.session.commit()

  satwa = Satwa.query.filter(Satwa.penulis_id == penulis).all()
  satwa_dict = {}
  no = 0
  for s in satwa:
    satwa_dict[no] = {
      "id":s.id_satwa,
      "judul":s.satwa_judul,
      "text":s.satwa_text,
      "gambar":s.satwa_gambar,
      "ringkas":s.satwa_ringkas
    }
    no+=1
  return str(json.dumps(satwa_dict))
  
@app.route('/update_satwa',methods=['POST'])
def update_satwa():
  judul=request.form['judul_satwa']
  text=request.form['text_satwa']
  kategori=request.form['kategori_satwa']
  id_satwa=request.form['id_satwa']
  penulis = request.form['penulis_satwa']
  satwa_ringkas = Sumarize_Bahasa_Bali(judul,text).sumarize()
  satwa = Satwa.query.get(id_satwa)
  try:
    gambar=upload_image("static/image/satwa_cover","img_satwa")
    if not gambar:
      gambar = satwa.satwa_gambar
  except:
    gambar = satwa.satwa_gambar
  print(gambar)
  
  if judul == "" or text == "":
    return "1"

  satwa.satwa_judul = judul
  satwa.satwa_text = text
  satwa.satwa_ringkas = satwa_ringkas
  satwa.satwa_gambar = gambar
  db.session.commit()

  satwa = Satwa.query.filter(Satwa.penulis_id == penulis).all()
  satwa_dict = {}
  no = 0
  for s in satwa:
    satwa_dict[no] = {
      "id":s.id_satwa,
      "judul":s.satwa_judul,
      "text":s.satwa_text,
      "gambar":s.satwa_gambar,
      "ringkas":s.satwa_ringkas
    }
    no+=1
  return json.dumps(satwa_dict)

@app.route('/delete_satwa',methods=['POST'])
def delete_satwa():
  id_satwa=request.form['id_satwa']
  penulis = request.form['penulis_satwa']

  db.session.delete(Satwa.query.get(id_satwa))
  db.session.commit()

  satwa = Satwa.query.filter(Satwa.penulis_id == penulis).all()
  satwa_dict = {}
  no = 0
  for s in satwa:
    satwa_dict[no] = {
      "id":s.id_satwa,
      "judul":s.satwa_judul,
      "text":s.satwa_text,
      "gambar":s.satwa_gambar,
      "ringkas":s.satwa_ringkas
    }
    no+=1
  return json.dumps(satwa_dict)

@app.route('/search_satwa/<id>/<query>',methods=['GET'])
def search_satwa(id,query):
  query = "%"+query+"%"
  if(id == "none"):
    satwa = Satwa.query.filter(or_(Satwa.satwa_text.like(query), Satwa.satwa_judul.like(query))).all()
  else:
    satwa = Satwa.query.filter(Satwa.penulis_id == id , or_(Satwa.satwa_text.like(query), Satwa.satwa_judul.like(query))).all()
  print(query)
  satwa_dict = {}
  no = 0
  for s in satwa:
    satwa_dict[no] = {
      "id":s.id_satwa,
      "judul":s.satwa_judul,
      "text":s.satwa_text,
      "gambar":s.satwa_gambar,
      "ringkas":s.satwa_ringkas
    }
    no+=1
  return json.dumps(satwa_dict)

if __name__=='__main__':
    app.run()