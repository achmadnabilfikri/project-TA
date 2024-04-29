from flask import Flask, render_template, request, redirect, url_for, session, flash

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
import psycopg2
import psycopg2.extras
import datetime

app = Flask(__name__)
app.secret_key = 'madarauchiha'

# postgres connection parameter
DB_HOST = 'localhost'
DB_NAME = 'sikasicov'
DB_USER = 'postgres'
DB_PASSWORD = 'madarauchiha'

# Function to connect to PostgreSQL database
def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn



dic = {0 : 'Normal',  
       1 : 'Covid-19'
        }

model = load_model('cnn_with_mobilenet_netwrok_after_fine_tuning.h5')

model.make_predict_function()


def predict_label(img_path):
	i = image.load_img(img_path, target_size=(224,224))
	i = image.img_to_array(i)/255.0

	i = i.reshape(1, 224,224,3)
	p = model.predict(i)  
	predicted_class_index = p.argmax(axis=-1)  
	return dic[predicted_class_index[0]]




@app.route("/")
def login():
	image = '../static/OIP.jpg'
	return render_template('login.php', image = image, clear_form=True)


@app.route("/login", methods=['POST'])
def login_handler():
	username = request.form['username']
	password = request.form['password']

	conn = connect_db()
	cur = conn.cursor()
	cur.execute("SELECT user_id FROM users WHERE username = %s AND password = %s", (username, password))
	user_id = cur.fetchone()
	cur.close()
	conn.close()

	if user_id is not None:
		session['username'] = username
		return redirect('/welcome')

	else:
		flash("username atau password salah.", 'invalid')
		return render_template('login.php', message='Invalid username or password')

# Route for welcome page
@app.route('/welcome')
def welcome():
	image = '../static/OIP.jpg'

	if 'username' in session:
		return render_template('welcome.php', username=session['username'], image = image)
	else:
		return redirect('/', clear_form=True)

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')



@app.route("/classification", methods=['GET', 'POST'])
def classification():
	return render_template("classification.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':        
		id_pasien = request.form['id_pasien']
		nama = request.form['nama']
		umur = request.form['umur']
		alamat = request.form['alamat']
		image_file = request.files['my_image']

		 
		conn = connect_db()  
		cur = conn.cursor()
		cur.execute("SELECT COUNT(*) FROM patients WHERE id_pasien = %s", (id_pasien,))
		existing_id = cur.fetchone()[0]

		if existing_id > 0:
			flash("id_pasien sudah ada , silahkan pilih id lainnya.", 'error')
			return redirect('/classification')  


        
		img_path = "static/" + image_file.filename
		image_file.save(img_path)

        
		prediction = predict_label(img_path)  

        
		conn = connect_db()  
		cur = conn.cursor()
		cur.execute("INSERT INTO patients (id_pasien, nama, umur, alamat, gambar, hasil_klasifikasi) VALUES (%s, %s, %s, %s, %s, %s)", (id_pasien, nama, umur, alamat, img_path, prediction))
		conn.commit()

        
		cur.execute("SELECT id_pasien, nama, umur, alamat, gambar, hasil_klasifikasi FROM patients ORDER BY id_pasien DESC LIMIT 1 ")
		patients = cur.fetchall()

		cur.close()
		conn.close()

        
	return render_template("classification.html", patients=patients)

@app.route("/data", methods = ['GET', 'POST'])
def data():
	conn = connect_db()
	cur = conn.cursor()
	cur.execute("SELECT id_pasien, nama, umur, alamat, gambar, hasil_klasifikasi FROM patients")
	patients = cur.fetchall()

	cur.close()
	conn.close()
	return render_template("data.html", patients = patients)

@app.route("/edit/<id_pasien>", methods=['POST','GET'] )
def edit(id_pasien):
	conn = connect_db()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("SELECT * FROM patients where id_pasien = {0}".format(id_pasien))
	patients = cur.fetchall()
	cur.close()
	conn.close()
	print(patients[0])

	return render_template('update.html', patients = patients[0])

@app.route("/update/<id_pasien>", methods=['POST'])
def update(id_pasien):
	if request.method == 'POST':
		nama = request.form['nama']
		umur = request.form['umur']
		alamat = request.form['alamat']
		gambar = request.form['gambar']

		conn = connect_db()
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("""UPDATE patients SET nama=%s, umur=%s, alamat=%s, gambar=%s WHERE id_pasien=%s""", 
					(nama, umur, alamat, gambar, id_pasien))
		conn.commit()

		flash('pasien berhasil diupdate', 'berhasil')
		return redirect('/data')	


@app.route("/delete/<string:id_pasien>", methods=["POST", "GET"])
def delete(id_pasien):
	conn=connect_db()
	cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute('DELETE FROM patients WHERE id_pasien = {0}'.format(id_pasien))
	conn.commit()
	flash("data pasien berhasil dihapus")
	return redirect("/data")

if __name__ =='__main__':
	app.run(debug = True)