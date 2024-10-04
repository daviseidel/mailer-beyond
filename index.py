from flask import Flask
import smtplib
import json
from jinja2 import Template
from email.message import EmailMessage
from flask import request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SMTP_SERVER = 'mail.spacemail.com'  
SMTP_PORT = 465
EMAIL_ADDRESS = 'contato@beyondcorp.co' 
SMTP_ADDRESS = 'Beyond Corp. <contato@beyondcorp.co>' 
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

## FUNÇÕES AUXILIARES

def load_template(template_path):
    with open(template_path, 'r') as file:
        template = Template(file.read())
    return template

def send_email(to_address, subject, html_content):
    msg = EmailMessage()
    msg['From'] = SMTP_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content('This is an HTML email. Please use an email client that supports HTML to view this message.')
    msg.add_alternative(html_content, subtype='html')
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        #server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print(f"Email sent to {to_address}")

## ROTAS

@app.route('/api')
def index():
    return 'Opa', 200

# /api/send?email=EMAIL&nome=NOME?codigo=CODIGO
@app.route('/api/send')
def send(): 
    email = request.args.get('email')
    nome = request.args.get('nome')
    codigo = request.args.get('codigo')

    template = load_template('api/res-emb.html')
    html_content = template.render(name=nome, code=codigo)
    send_email(email, 'Você foi aceito como Embaixador Beyond!', html_content)
    return 'Email enviado!', 200

# /api/create?nome=NOME?codigo=CODIGO
@app.route('/api/create')
def create(): 
    nome = request.args.get('nome')
    codigo = request.args.get('codigo')

    template = load_template('api/res-emb.html')
    html_content = template.render(name=nome, code=codigo)
    send_email('daviseidel.brandao@gmail.com', f"Crie o código {codigo} para {nome}", html_content)
    return 'Email enviado!', 200


