from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
import cloudinary
import cloudinary.uploader
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta_super_segura'
app.permanent_session_lifetime = timedelta(minutes=30)  

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

USUARIO_CORRETO = os.getenv('LOGIN_USUARIO')
SENHA_CORRETA = os.getenv('LOGIN_SENHA')

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
        
        if session.get('logado'):
            nome = request.form.get('nome')
            data = request.form.get('data')
            imagem = request.files.get('imagem')

            if imagem and nome and data:
                resultado = cloudinary.uploader.upload(imagem)
                galeria.append({
                    'nome': nome,
                    'data': data,
                    'url': resultado['secure_url']
                })
                salvar_galeria(galeria)
                return redirect(url_for('galeria_view'))

        else:
            usuario = request.form.get('usuario')
            senha = request.form.get('senha')
            if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
                session.permanent = False 
                session['logado'] = True
                return redirect(url_for('index'))
            else:
                flash("Usuário ou senha incorretos.")

    return render_template('index.html')

@app.route('/galeria')
def galeria_view():
    return render_template('galeria.html', imagens=galeria)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/excluir/<int:index>', methods=['POST'])
def excluir(index):
    if not session.get('logado'):
        return redirect(url_for('index'))
    if 0 <= index < len(galeria):
        galeria.pop(index)
        salvar_galeria(galeria)
    return redirect(url_for('galeria_view'))

@app.route('/mover/<int:index>/<direcao>', methods=['POST'])
def mover(index, direcao):
    if not session.get('logado'):
        return redirect(url_for('index'))

    if direcao == 'cima' and index > 0:
        galeria[index], galeria[index - 1] = galeria[index - 1], galeria[index]
    elif direcao == 'baixo' and index < len(galeria) - 1:
        galeria[index], galeria[index + 1] = galeria[index + 1], galeria[index]
    salvar_galeria(galeria)
    return redirect(url_for('galeria_view'))

if __name__ == '__main__':
    app.run(debug=True)
