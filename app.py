from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

posts = [
    {
        "id": 1,
        "username": "GeceAvcisi",
        "group": "Korku",
        "title": "FNAF Evrenindeki Gizemli Parazit",
        "content": "Dun gece oyunu oynarken ekranda garip bir glitch belirdi. Sizce bu yeni bir easter egg mi?",
    },
    {
        "id": 2,
        "username": "GamerEge",
        "group": "Eglence",
        "title": "En Komik Korku Capsleri",
        "content": "Korku filmi izlerken arkadan komik muzik acinca filmin hicbir havasi kalmiyor, deneyin derim!",
    },
]


@app.route("/")
def index():
    selected_group = request.args.get("group")
    if selected_group:
        filtered_posts = [p for p in posts if p["group"] == selected_group]
    else:
        filtered_posts = posts

    html_template = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>YEX - Korku & Eglence</title>
        <style>
            body { background-color: #0b0c10; color: #c5c6c7; font-family: sans-serif; margin: 0; padding: 20px; }
            header { text-align: center; border-bottom: 2px solid #1f2833; padding-bottom: 20px; }
            h1 { color: #66fcf1; font-size: 3rem; letter-spacing: 5px; margin: 0; text-shadow: 2px 2px #ff0055; }
            .subtitle { color: #45a29e; }
            .nav-buttons { margin: 20px 0; text-align: center; }
            .btn { background-color: #1f2833; color: #66fcf1; border: 1px solid #45a29e; padding: 10px 20px; margin: 5px; cursor: pointer; text-decoration: none; display: inline-block; border-radius: 5px; }
            .btn:hover { background-color: #45a29e; color: #0b0c10; }
            .btn-korku { border-color: #ff0055; color: #ff0055; }
            .btn-korku:hover { background-color: #ff0055; color: #fff; }
            .container { max-width: 800px; margin: 0 auto; }
            .post-card { background-color: #1f2833; border-radius: 8px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #45a29e; }
            .post-card.Korku { border-left-color: #ff0055; }
            .group-badge { font-size: 0.8rem; padding: 3px 8px; border-radius: 3px; background-color: #0b0c10; }
            .form-section { background-color: #1f2833; padding: 20px; border-radius: 8px; margin-top: 30px; }
            input, textarea, select { width: 100%; padding: 10px; margin: 10px 0; background-color: #0b0c10; border: 1px solid #45a29e; color: #fff; box-sizing: border-box; }
            input[type="submit"] { background-color: #66fcf1; color: #0b0c10; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>
        <header>
            <h1>YEX</h1>
            <p class="subtitle">Korku ve Eglencenin Yeni Gruplar Platformu</p>
        </header>
        <div class="container">
            <div class="nav-buttons">
                <a href="/" class="btn">Tum Gonderiler</a>
                <a href="/?group=Korku" class="btn btn-korku">Korku Grubu</a>
                <a href="/?group=Eglence" class="btn">Eglence Grubu</a>
            </div>
            <h2>Paylasimlar</h2>
            {% for post in posts %}
            <div class="post-card {{ post.group }}">
                <h3>{{ post.title }} <span class="group-badge">{{ post.group }}</span></h3>
                <p>{{ post.content }}</p>
                <small>Paylasan: <strong>@{{ post.username }}</strong></small>
            </div>
            {% endfor %}
            <div class="form-section">
                <h3>Yex'te Yeni Paylasim Yap</h3>
                <form action="/add_post" method="post">
                    <input type="text" name="username" placeholder="Kullanici Adin" required>
                    <input type="text" name="title" placeholder="Gonderi Basligi" required>
                    <select name="group">
                        <option value="Korku">Korku</option>
                        <option value="Eglence">Eglence</option>
                    </select>
                    <textarea name="content" rows="4" placeholder="Icerik yaz..." required></textarea>
                    <input type="submit" value="Yex'te Paylas">
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, posts=filtered_posts)


@app.route("/add_post", methods=["POST"])
def add_post():
    username = request.form.get("username")
    title = request.form.get("title")
    group = request.form.get("group")
    content = request.form.get("content")

    new_post = {
        "id": len(posts) + 1,
        "username": username,
        "group": group,
        "title": title,
        "content": content,
    }

    posts.append(new_post)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
