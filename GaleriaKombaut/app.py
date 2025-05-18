from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista para guardar os dados das imagens (poderia ser um banco de dados também)
galeria = []

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

            # Salva os dados na lista
            galeria.append({
                'nome': nome,
                'data': data,
                'arquivo': filename
            })

            return redirect(url_for('galeria_view'))  # redireciona para a galeria

    return render_template('index.html')

@app.route('/galeria')
def galeria_view():
    return render_template('galeria.html', imagens=galeria)

if __name__ == '__main__':
    app.run(debug=True)