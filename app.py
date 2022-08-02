from flask import Flask, render_template, request, url_for, redirect,session

app = Flask(__name__)

app = Flask(__name__,template_folder='template')

data = ["https://duniapendidikan.co.id/wp-content/uploads/2018/12/rakyat-bali.jpg",
      "https://tatkala.co/wp-content/uploads/2021/01/mardi-yasa.-satua-bali.png",
      "https://seringjalan.com/wp-content/uploads/2021/04/Cerita-Manik-Angkeran-816x577.jpg"]

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/satwa_nav')
def satwa_nav():
  return render_template("leftbar.html")

@app.route('/satwa_card/<no>/<image>', methods=['GET'])
def satwa_card(no,image):
  return render_template("card_satwa.html", no = no, image = data[int(image)])

@app.route('/satwa_reading')
def satwa_reading():
  return render_template("reading_satwa.html")

if __name__=='__main__':
    app.run(debug=True,port = 5000,host='0.0.0.0')