from flask import Flask, render_template, request, redirect, url_for
import os
import logging
from werkzeug.utils import secure_filename

# Configuração básica do logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info('Iniciando o app Flask')

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista para guardar os dados das imagens (poderia ser um banco de dados também)
galeria = []

@app.route('/', methods=['GET', 'POST'])
def index():
    logger.debug('Requisição recebida na rota /')
    if request.method == 'POST':
        nome = request.form.get('nome')
        data = request.form.get('data')
        imagem = request.files.get('imagem')

        logger.debug(f'Dados recebidos: nome={nome}, data={data}, imagem={imagem.filename if imagem else "Nenhuma"}')

        if imagem and nome and data:
            ext = imagem.filename.rsplit('.', 1)[-1]
            filename = secure_filename(f"{nome}_{data}.{ext}")
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logger.debug(f'Salvando imagem em: {caminho}')
            imagem.save(caminho)

            # Salva os dados na lista
            galeria.append({
                'nome': nome,
                'data': data,
                'arquivo': filename
            })

            logger.info(f'Imagem salva e dados adicionados à galeria: {filename}')
            return redirect(url_for('galeria_view'))  # redireciona para a galeria

    return render_template('index.html')

@app.route('/galeria')
def galeria_view():
    logger.debug('Requisição recebida na rota /galeria')
    return render_template('galeria.html', imagens=galeria)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f'Servidor iniciando na porta {port}')
    app.run(host='0.0.0.0', port=port, debug=True)
