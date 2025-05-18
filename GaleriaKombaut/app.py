from flask import Flask, render_template, request, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

GALERIA_JSON = 'galeria.json'

def carregar_galeria():
    if os.path.exists(GALERIA_JSON):
        with open(GALERIA_JSON, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def salvar_galeria(galeria):
    with open(GALERIA_JSON, 'w') as f:
        json.dump(galeria, f, indent=4)


galeria = carregar_galeria()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        data = request.form.get('data')
        imagem = request.files.get('imagem')

        if imagem and nome and data:
            ext = imagem.filename.rsplit('.', 1)[-1]
            filename = secure_filename(f"{nome}_{data}.{ext}")
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagem.save(caminho)

            galeria.append({
                'nome': nome,
                'data': data,
                'arquivo': filename
            })

            salvar_galeria(galeria)  

            return redirect(url_for('galeria_view'))

    return render_template('index.html')

@app.route('/galeria')
def galeria_view():
    return render_template('galeria.html', imagens=galeria)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
