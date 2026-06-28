import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Klasör yapılandırması
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Geçici veri tabanları
twitler = [
    {"id": 1, "kullanici": "CaganEge", "icerik": "Yex Platformu artık canlıda!", "kategori": "eğlence"},
    {"id": 2, "kullanici": "YexBot", "icerik": "Korku, eğlence, aksiyon ve yaz burada!", "kategori": "korku"}
]
videolar = []
genel_chat = [{"kullanici": "Sistem", "mesaj": "Yex Genel Chat Odasına Hoş Geldiniz!"}]

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

@app.route('/genel-mesaj-gonder', methods=['POST'])
def genel_mesaj_gonder():
    kullanici = request.form.get('kullanici', 'Anonim')
    mesaj = request.form.get('mesaj')
    if mesaj:
        genel_chat.append({"kullanici": kullanici, "mesaj": mesaj})
    return redirect(url_for('ana_sayfa'))

# Bulut sunucuları için port ayarını dinamik alıyoruz
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
