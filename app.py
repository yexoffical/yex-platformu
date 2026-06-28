import os
from flask import Flask, render_template, request, redirect, url_for

ŞU_AN_Kİ_KLASÖR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_KLASÖRÜ = os.path.join(ŞU_AN_Kİ_KLASÖR, 'templates')
STATIC_KLASÖRÜ = os.path.join(ŞU_AN_Kİ_KLASÖR, 'static')

app = Flask(__name__, template_folder=TEMPLATES_KLASÖRÜ, static_folder=STATIC_KLASÖRÜ)

os.makedirs(os.path.join(STATIC_KLASÖRÜ, 'uploads'), exist_ok=True)

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
    try:
        return render_template('index.html', twitler=twitler, videolar=videolar, genel_chat=genel_chat)
    except Exception as e:
        return f"Arayüz yüklenirken hata oluştu! Lütfen 'templates/index.html' dosyanızı kontrol edin. Hata: {str(e)}", 500

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
