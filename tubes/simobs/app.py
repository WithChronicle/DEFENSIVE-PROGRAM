from flask import Flask, render_template, request, redirect, session
import sqlite3, random, time, smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "secret123"


# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        email TEXT,
        no_hp TEXT,
        password TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS booking(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        motor TEXT,
        keluhan TEXT,
        status TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# ================= EMAIL OTP =================
def kirim_otp_email(penerima, otp):
    pengirim = "exynoz26@gmail.com"
    password = "isvl fkwl faqh zwlr"

    subject = "Kode OTP SIMOBS"

    body = f"""
    <h2>SIMOBS</h2>
    <p>Kode OTP kamu:</p>
    <h1 style='color:#ffb800'>{otp}</h1>
    <p>Berlaku 60 detik</p>
    """

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = pengirim
    msg['To'] = penerima

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(pengirim, password)
        server.sendmail(pengirim, penerima, msg.as_string())
        server.quit()
        print("OTP berhasil dikirim")
    except Exception as e:
        print("ERROR EMAIL:", e)

# ================= ROUTES =================

@app.route('/')
def home():
    return redirect('/login')

# ---------- REGISTER ----------
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/do_register', methods=['POST'])
def do_register():
    nama = request.form['nama']
    email = request.form['email']
    no_hp = request.form['no_hp']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (nama,email,no_hp,password) VALUES (?,?,?,?)",
              (nama,email,no_hp,password))
    conn.commit()
    conn.close()

    return redirect('/login')

# ---------- LOGIN ----------
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_input = request.form['user']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("""
    SELECT * FROM users 
    WHERE (email=? OR no_hp=?) AND password=?
    """,(user_input,user_input,password))

    user = c.fetchone()
    conn.close()

    if user:
        otp = str(random.randint(100000,999999))
        session['otp'] = otp
        session['otp_time'] = time.time()
        session['temp_user'] = user[1]
        session['email'] = user[2]

        print("EMAIL TUJUAN:", user[2])
        print("OTP:", otp)

        kirim_otp_email(user[2], otp)

        return redirect('/otp')

    return "Login gagal"

# ---------- OTP ----------
@app.route('/otp')
def otp():
    return render_template('otp.html')

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if time.time() - session.get('otp_time',0) > 60:
        return "OTP kadaluarsa"

    if request.form['otp'] == session.get('otp'):
        session['user'] = session['temp_user']
        return redirect('/dashboard')

    return "OTP salah"

@app.route('/resend_otp')
def resend_otp():
    otp = str(random.randint(100000,999999))
    session['otp'] = otp
    session['otp_time'] = time.time()

    kirim_otp_email(session['email'], otp)
    return redirect('/otp')

# ---------- DASHBOARD ----------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', nama=session.get('user'))

# ---------- BOOKING ----------
@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/do_booking', methods=['POST'])
def do_booking():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO booking (user,motor,keluhan,status) VALUES (?,?,?,?)",
              (session['user'],request.form['motor'],request.form['keluhan'],"Proses"))

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# ---------- RIWAYAT ----------
@app.route('/riwayat')
def riwayat():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM booking WHERE user=?", (session['user'],))
    data = c.fetchall()
    conn.close()

    return render_template('riwayat.html', data=data)

# ---------- STATUS ----------
@app.route('/status')
def status():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM booking WHERE user=? ORDER BY id DESC LIMIT 1",(session['user'],))
    data = c.fetchone()
    conn.close()

    return render_template('status.html', data=data)

# ---------- SPAREPART ----------
@app.route('/sparepart')
def sparepart():
    return render_template('sparepart.html')

@app.route('/oli')
def oli():
    return render_template('oli.html')

# ---------- PROFILE ----------
@app.route('/profile')
def profile():
    return render_template('profile.html', nama=session.get('user'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)