from flask import Flask, render_template, request, redirect, url_for, flash
import os
import yt_dlp

app = Flask(__name__)
app.secret_key = 'secret-key'

# Diretório para salvar os vídeos baixados
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        resolution = request.form.get("resolution")

        if not url:
            flash("Por favor, insira a URL do vídeo.")
            return redirect(url_for("index"))

        try:
            # Configurações para baixar apenas streams progressivos
            ydl_opts = {
                'format': f'best[height<={resolution[:-1]}][acodec!=none][vcodec!=none]/mp4',
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'noplaylist': True,  # Evita baixar playlists inteiras
                'postprocessors': []  # Não utiliza o FFmpeg
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            flash("Vídeo baixado com sucesso!")
        except Exception as e:
            flash(f"Erro ao baixar o vídeo: {str(e)}")
    
    return render_template("index.html")

@app.route("/clear", methods=["POST"])
def clear():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
