import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Video yüklemeleri için klasör ayarı
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'avi'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Geçici veri tabanları (Sistem her yeniden başladığında sıfırlanır, test için idealdir)
twitler = [
    {"id": 1, "kullanici": "CaganEge", "icerik": "Yex Platformu artık canlıda!", "kategori": "eğlence"},
    {"id": 2, "kullanici": "YexBot", "icerik": "Korku, eğlence, aksiyon ve yaz burada!", "kategori": "korku"}
]

videolar = []
genel_chat = [{"kullanici": "Sistem", "mesaj": "Yex Genel Chat Odasına Hoş Geldiniz!"}]
ozel_chatler = {} # İki kişilik mesajlaşmalar için

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# TAMİR EDİLEN BÖLÜM: HEAD hatasını engelleyen ve Render kontrolünü çözen ana sayfa rotası
@app.route('/', methods=['GET', 'HEAD'])
def ana_sayfa():
    if request.method == 'HEAD':
        return '', 200
    return render_template('index.html', twitler=twitler, videolar=videolar, genel_chat=genel_chat)

@app.route('/twit-ekle', methods=['POST'])
def twit_ekle():
    kullanici = request.form.get('kullanici', 'Anonim')
    icerik = request.form.get('icerik')
    kategori = request.form.get('kategori', 'eğlence')
    if icerik:
        twitler.insert(0, {"id": len(twitler)+1, "kullanici": kullanici, "icerik": icerik, "kategori": kategori})
    return redirect(url_for('ana_sayfa'))

@app.route('/video-yukle', methods=['POST'])
def video_yukle():
    if 'video_dosya' not in request.files:
        return redirect(url_for('ana_sayfa'))
    file = request.files['video_dosya']
    baslik = request.form.get('video_baslik', 'Başlıksız Video')
    kategori = request.form.get('video_kategori', 'eğlence')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        videolar.insert(0, {
            "baslik": baslik,
            "url": f"/static/uploads/{filename}",
            "kategori": kategori,
            "yukleyen": "Kullanıcı"
        })
    return redirect(url_for('ana_sayfa'))

@app.route('/genel-mesaj-gonder', methods=['POST'])
def genel_mesaj_gonder():
    kullanici = request.form.get('kullanici', 'Anonim')
    mesaj = request.form.get('mesaj')
    if mesaj:
        genel_chat.append({"kullanici": kullanici, "mesaj": mesaj})
    return redirect(url_for('ana_sayfa'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
