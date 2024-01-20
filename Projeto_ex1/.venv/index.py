
from flask import Flask, render_template # O "render_template" importa a biblioteca para renderizar arquivos ".html". Já o "Flask" importa a bliblioteca do microframework flask

app = Flask(__name__) #Instancia do flask dentro da variável app

@app.route('/') #criar uma rota (somente a "/" equivale a raiz do site, por exemplo: www.uol.com.br)
def pag_cli_ativos(): #Função que retorna "Hello, World!"
    return render_template('aula1.html', titulo="Minha Página!") #Vinculado a rota criada acima

@app.route('/outrarota') #criar uma rota
def pag_cli2(): #Função que retorna "Hello, World!"
    return "<h1>Outra rota</h1>."\
        "<p>Olha a tag HTML de parágrafo aqui.</p>"\
        "<img src = 'https://picsum.photos/200/300'>"


app.run() #Emula um servidor 
