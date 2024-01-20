from flask import Flask, render_template, request

app = Flask (__name__)

@app.route('/') #Por padrão, qualquer rota utiliza o método "GET"
def index():
    return render_template("index.html", titulo="Página inicial!")

@app.route('/login', methods= ['POST']) #Como na página HTML ultilizamos o método "POST", devemos utilizar o "POST" como método da rota
def login():
    login_user = request.form['login'] #Esse "login" é do atributo name do input que solicita o login para o usuário
    senha = request.form['senha'] # Nome do componente lá no form do HTML. Pega os dados da requisição
    if login_user == "admin" and senha == "123":
        return 'Logou'
    else:
        return render_template("index.html", titulo="Usuário ou senha inválidos") # Caso os dados estejam inválidos, o usuário é redirecionado para a página index, porém a tag <h1> da página é alterada para "Usuário ou senha inválidos"
    
@app.route('/clientes')
def clientes():
    return render_template("pagina_clientes.html", titulo_clientes="Página de Clientes!")

app.run()