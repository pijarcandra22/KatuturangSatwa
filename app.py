import pandas as pd
import numpy as np
from operator import or_
from flask import Flask, render_template, request, url_for, redirect,session
from flask_sqlalchemy import SQLAlchemy
import json 
from gensim import corpora, models
from static.py.KatuturangSatwa_Function import Sumarize_Bahasa_Bali
from static.py.KatuturangSatwa_Function import CaracterDetection_Bahasa_Bali
from static.py.KatuturangSatwa_Function import TopicModeling_Bahasa_Bali
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app = Flask(__name__,template_folder='template')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
GetCarName = CaracterDetection_Bahasa_Bali()
GetCategory = TopicModeling_Bahasa_Bali()
GetLDA = models.ldamodel.LdaModel.load("ldaModel")
GetCorpus = corpora.Dictionary.load('ldaModel.id2word')

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

def uploadManual():
  for filename in os.listdir("db"):
    with open(os.path.join("db", filename), 'r', encoding="utf8") as f:
      judul = filename.replace(".txt", "")
      text  = f.read()
      satwa_ringkas = Sumarize_Bahasa_Bali(judul,text).sumarize()
      satwa_tokoh = GetCarName.ner_name(text)
      satwa = Satwa(satwa_judul = judul , satwa_text = text, satwa_ringkas = satwa_ringkas, satwa_gambar = 'default.jpg', penulis_id = '1', satwa_tokoh = satwa_tokoh)
      db.session.add(satwa)
      db.session.commit()

def manual_generate_category():
  satwa = Satwa.query.all()
  satwa_dict = {'Id':[],"Judul":[],"RealText":[],"Steeming":[]}
  for s in satwa:
    satwa_dict['Id'].append(s.id_satwa)
    satwa_dict['Judul'].append(s.satwa_judul)
    satwa_dict['RealText'].append(s.satwa_text)
    satwa_dict['Steeming'].append(GetCategory.Preprocessing(s.satwa_text))

  df = pd.DataFrame.from_dict(satwa_dict)

  data = df.Steeming.values.tolist()
  GetCategory.TrainModel(data)
  df = GetCategory.format_topics_sentences(df)
  df.to_csv('HasilSementara.csv')

  GetCategory.ldamodel.save("ldaModel")
  print("done")

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
  satwa_kategori = db.Column(db.String(500), index = True, unique = False)
  penulis_id = db.Column(db.Integer, db.ForeignKey('author.id_auth'))

  def __repr__(self):
    return '<Judul %r>' % self.satwa_judul
  
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Kategori(db.Model):
  id_kategori = db.Column(db.Integer,db.Sequence('seq_reg_id', start=1, increment=1), primary_key = True)
  nama_kategori = db.Column(db.String(500), index = True, unique = False)
  gambar_kategori = db.Column(db.String(500), index = True, unique = False)
  banyak_akses = db.Column(db.Integer, index = True, unique = False)
  id_satwa_example = db.Column(db.Integer, index = True, unique = False)

  def __repr__(self):
    return '<Judul %r>' % self.nama_kategori
  
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
      "ringkas":s.satwa_ringkas,
      "tokoh":s.satwa_tokoh,
      "kategori":s.satwa_kategori
    }
    no+=1

  kat = Kategori.query.all()
  kat_satwa = {}
  no = 0
  for k in kat:
    kat_satwa[no] = {
      "id":k.id_kategori,
      "kategori":k.nama_kategori,
      "gambar_kat":k.gambar_kategori,
      "id_satwa":k.id_satwa_example
    }
    no+=1
  return render_template("index.html", satwaData = str(json.dumps(satwa_dict)), kategori = json.dumps(kat_satwa))

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
  try:
    tokoh = satwa.satwa_tokoh.split(";")
  except:
    tokoh = []    
  return render_template("component/card_satwa.html", satwa = satwa, no = no, tokoh = tokoh)

@app.route('/satwa_reading')
def satwa_reading():
  satwa = Satwa.query.get(1)
  return render_template("component/reading_satwa.html", satwa = satwa)

@app.route('/satwa_writing/<id>', methods=['GET'])
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
      "ringkas":s.satwa_ringkas,
      "tokoh":s.satwa_tokoh,
      "kategori":s.satwa_kategori
    }
    no+=1
  return render_template("component/writing_satwa.html", my_satwaData = str(json.dumps(satwa_dict)))

@app.route('/admin_satwa/<id>', methods=['GET'])
def admin_satwa(id):
  kat = Kategori.query.all()
  kat_satwa = {}
  no = 0
  for k in kat:
    kat_satwa[no] = {
      "id":k.id_kategori,
      "kategori":k.nama_kategori,
      "gambar_kat":k.gambar_kategori,
      "id_satwa":k.id_satwa_example
    }
    no+=1
  return render_template("admin.html", kategori = str(json.dumps(kat_satwa)),)

@app.route('/box_category/<id>', methods=['GET'])
def box_category(id):
  ket = Kategori.query.get(id)
  satwa = Satwa.query.get(ket.id_satwa_example)
  if satwa is None:
    gambar_satwa = 'default.jpg'
  else:
    gambar_satwa = satwa.satwa_gambar
  return render_template("component/category_satwa.html", kategori = ket,gambar_satwa=gambar_satwa)

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

@app.route('/update_account',methods=['POST'])
def update_account():
  id=request.form['id']
  username=request.form['username']
  naleng=request.form['naleng']
  email=request.form['email']

  auth = Author.query.get(id)
  try:
    gambar=upload_image("static/image/author_image","img_update")
    if not gambar:
      gambar = auth.gambar
    else:
      if auth.gambar != 'default.jpg':
        os.remove("static/image/author_image/"+auth.gambar)
  except:
    gambar = auth.gambar
  print(gambar)
  
  if username == "" or naleng == "" or email == "":
    return "1"

  auth.username = username
  auth.nama_lengkap = naleng
  auth.email = email
  auth.gambar = gambar
  db.session.commit()

  auth = Author.query.filter(Author.username == username).first()
  return str(json.dumps(auth.as_dict()))

@app.route('/submit_satwa',methods=['POST'])
def submit_satwa():
  judul=request.form['judul_satwa']
  text=request.form['text_satwa']
  kategori=request.form['kategori_satwa']
  penulis = request.form['penulis_satwa']
  
  data = GetCategory.Preprocessing(text)
  data = list(GetCategory.sent_to_words(list(data)))
  corpus = [GetCorpus.doc2bow(doc) for doc in list(data)]
  output = GetLDA[corpus]
  row = output[0] if GetLDA.per_word_topics else output
  topics = sorted(row[0], key=lambda x:x[1], reverse=True)
  kat = Kategori.query.get(topics[0][0]+1)

  gambar=upload_image("static/image/satwa_cover","img_satwa")
  satwa_ringkas = Sumarize_Bahasa_Bali(judul,text).sumarize()
  satwa_tokoh = GetCarName.ner_name(text)

  if judul == "" or text == "":
    return "1"
  if not gambar:
    return "2"

  if kategori is None:
    satwa.satwa_kategori = "!" + str(kat.nama_kategori).lower()
  elif not str(kat.nama_kategori).lower() in kategori.lower():
    satwa.satwa_kategori = kategori + ",!" + str(kat.nama_kategori).lower()

  satwa = Satwa(satwa_judul = judul , satwa_text = text, satwa_ringkas = satwa_ringkas, satwa_gambar = gambar, penulis_id = penulis, satwa_tokoh = satwa_tokoh, satwa_kategori = satwa_kategori)
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
      "ringkas":s.satwa_ringkas,
      "tokoh":s.satwa_tokoh,
      "kategori":s.satwa_kategori
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

  data = GetCategory.Preprocessing(text)
  data = list(GetCategory.sent_to_words(list(data)))
  corpus = [GetCorpus.doc2bow(doc) for doc in list(data)]
  output = GetLDA[corpus]
  row = output[0] if GetLDA.per_word_topics else output
  topics = sorted(row[0], key=lambda x:x[1], reverse=True)
  kat = Kategori.query.get(topics[0][0]+1)

  satwa_ringkas = Sumarize_Bahasa_Bali(judul,text).sumarize()
  satwa_tokoh = GetCarName.ner_name(text)
  satwa = Satwa.query.get(id_satwa)
  
  try:
    gambar=upload_image("static/image/satwa_cover","img_satwa")
    if not gambar:
      gambar = satwa.satwa_gambar
    else:
      if satwa.satwa_gambar != 'default.jpg':
        os.remove("static/image/author_image/"+ satwa.satwa_gambar)
  except:
    gambar = satwa.satwa_gambar
  print(gambar)
  
  if judul == "" or text == "":
    return "1"

  if kategori is None:
    satwa.satwa_kategori = "!" + str(kat.nama_kategori).lower()
  elif not str(kat.nama_kategori).lower() in kategori.lower():
    satwa.satwa_kategori = kategori + ",!" + str(kat.nama_kategori).lower()

  satwa.satwa_judul = judul
  satwa.satwa_text = text
  satwa.satwa_ringkas = satwa_ringkas
  satwa.satwa_gambar = gambar
  satwa.satwa_tokoh = satwa_tokoh
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
      "ringkas":s.satwa_ringkas,
      "tokoh":s.satwa_tokoh,
      "kategori":s.satwa_kategori
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
      "ringkas":s.satwa_ringkas,
      "tokoh":s.satwa_tokoh,
      "kategori":s.satwa_kategori
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
      "ringkas":s.satwa_ringkas,
      "tokoh":s.satwa_tokoh,
      "kategori":s.satwa_kategori
    }
    no+=1
  return json.dumps(satwa_dict)

@app.route('/generate_category',methods=['GET'])
def generate_category():
  satwa = Satwa.query.all()
  satwa_dict = {'Id':[],"Judul":[],"RealText":[],"Steeming":[]}
  for s in satwa:
    satwa_dict['Id'].append(s.id_satwa)
    satwa_dict['Judul'].append(s.satwa_judul)
    satwa_dict['RealText'].append(s.satwa_text)
    satwa_dict['Steeming'].append(GetCategory.Preprocessing(s.satwa_text))

  df = pd.DataFrame.from_dict(satwa_dict)

  data = df.Steeming.values.tolist()
  GetCategory.TrainModel(data)
  df = GetCategory.format_topics_sentences(df)
  df.to_csv('HasilSementara.csv')

  GetCategory.ldamodel.save("ldaModel")

  topic_dict = {}
  no = 0    
  for idx, topic in GetCategory.ldamodel.print_topics(-1):
    topic_dict[no] = {
      "topic":idx,
      "words":topic
    }
    no+=1
  
  return json.dumps(topic_dict)

@app.route('/category_update',methods=['POST'])
def category_update():
  print("Hai")
  topik = json.loads(request.form['dataTopic'])
  hasilSementara = pd.read_csv("HasilSementara.csv")

  for t in topik.values():
    idx, word = t.values()
    kat = Kategori.query.filter(Kategori.nama_kategori == word.lower()).first()
    if kat is None:
      kat = Kategori(nama_kategori = word.lower(), gambar_kategori= 'default.jpg')
      db.session.add(kat)
      db.session.commit()
    print(idx,word)
    hasilSementara['Topic_Keywords'].mask(hasilSementara["Dominant_Topic"] == idx, word, inplace=True)

  for i in range(0,len(hasilSementara)):
    s = hasilSementara.loc[i]
    satwa = Satwa.query.get(str(s.Id))
    print(satwa)
    if satwa.satwa_kategori is None:
      satwa.satwa_kategori = "!" + hasilSementara.loc[i].Topic_Keywords.lower()
    elif hasilSementara.loc[i].Topic_Keywords.lower() not in satwa.satwa_kategori:
      satwa.satwa_kategori += ",!" + hasilSementara.loc[i].Topic_Keywords.lower()
    db.session.commit()    

  print(hasilSementara['Topic_Keywords'].head())
  kat = Kategori.query.all()
  kat_satwa = {}
  no = 0
  for k in kat:
    kat_satwa[no] = {
      "id":k.id_kategori,
      "kategori":k.nama_kategori,
      "gambar_kat":k.gambar_kategori,
      "id_satwa":k.id_satwa_example
    }
    no+=1
  return json.dumps(kat_satwa)

@app.route('/category_single_update',methods=['POST'])
def category_single_update():
  id=request.form['id_cat']
  kategori=request.form['nama_cat']
  id_satwa=request.form['radio_cat']

  print(kategori)
  cat = Kategori.query.get(id)
  try:
    gambar=upload_image("static/image/kategori","img_cat")
    if not gambar:
      gambar = cat.gambar_kategori
    else:
      if cat.gambar_kategori != 'default.jpg':
        os.remove("static/image/kategori/"+cat.gambar_kategori)
  except:
    gambar = cat.gambar_kategori
  print(gambar)
  
  if kategori == "" or id_satwa == "":
    return "1"

  cat.nama_kategori = kategori
  cat.id_satwa_example = id_satwa
  cat.gambar_kategori = gambar
  db.session.commit()

  kat = Kategori.query.all()
  kat_satwa = {}
  no = 0
  for k in kat:
    kat_satwa[no] = {
      "id":k.id_kategori,
      "kategori":k.nama_kategori,
      "gambar_kat":k.gambar_kategori,
      "id_satwa":k.id_satwa_example
    }
    no+=1
  return json.dumps(kat_satwa)

if __name__=='__main__':
    app.run()