from dotenv import load_dotenv
load_dotenv()  

from flask import Flask, render_template, request, redirect, url_for
import os
import json
import cloudinary
import cloudinary.uploader

app = Flask(__name__)  


cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)


print("Cloudinary config:")
print("cloud_name =", cloudinary.config().cloud_name)
print("api_key =", cloudinary.config().api_key)
print("api_secret =", cloudinary.config().api_secret)

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

        print("Recebido nome:", nome, "data:", data, "imagem:", imagem)  # DEBUG

        if imagem and nome and data:
            
            resultado = cloudinary.uploader.upload(imagem)
            print("Upload Cloudinary resultado:", resultado)  # DEBUG

            galeria.append({
                'nome': nome,
                'data': data,
                'url': resultado['secure_url']
            })

            salvar_galeria(galeria)
            return redirect(url_for('galeria_view'))

    return render_template('index.html')

@app.route('/galeria')
def galeria_view():
    return render_template('galeria.html', imagens=galeria)

if __name__ == '__main__':
    app.run(debug=True)