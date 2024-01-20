from flask import Flask, redirect, render_template, request, url_for
import mysql.connector #Conectar com o mySQL

app = Flask (__name__)

@app.route('/')
def index():
    return render_template ("index.html", titulo = "Bem-Vindo!")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/pagina_inicial', methods=['POST'])
def logar():
    login_user = request.form['login']
    senha = request.form['senha']
    if login_user == "admin" and senha == "123":
        return render_template('pagina_inicial.html', titulo="Página Principal!")
    else:
        return render_template('login.html') 
    
@app.route('/cadastro_usuario')
def cadastrar_usuario():
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco")
    mycursor = db.cursor()
    query = "select usuario, email from joaoCosta_TB_user"
    mycursor.execute(query) #Tem todo o resultado da query
    resultado = mycursor.fetchall() #Pega todas as linhas que encontrou e coloca dentro da varáivel "resultado"
    return render_template("cadastro_usuario.html", titulo='Cadastrar Usuário', usuarios=resultado)

@app.route('/cadastro_cliente')
def cadastrar_cliente():
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec",database= "meu_banco")
    mycursor = db.cursor()
    query = "select cpf, nome, email, endereco, bairro, cep, cidade from joaoCosta_TB_client"
    mycursor.execute(query) #Tem todo o resultado da query
    resultado = mycursor.fetchall() #Pega todas as linhas que encontrou e coloca dentro da varáivel "resultado"
    return render_template('cadastro_cliente.html', titulo='Cadastrar Cliente', cpfs=resultado)

@app.route('/processar_usuario', methods=['POST'])
def inserir_cadastro():
    usuario = request.form['usuario']
    senha = request.form['senha']
    email = request.form['email']
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "INSERT INTO joaoCosta_TB_user (usuario, senha, email) VALUES (%s, %s, %s)" #Variável de texto de um comando SQL que vai executar dentro do Banco de Dados (vai criar uma tabela chamada clientes e vai inserir os atributos usuario e senha)
    values = (usuario, senha, email)
    mycursor.execute(query, values)
    db.commit()
    return redirect (url_for("cadastrar_usuario"))

@app.route('/processar_cliente', methods=['POST'])
def inserir_cliente():
    cpf = request.form['cpf']
    nome = request.form['nome']
    email = request.form['email']
    endereco = request.form['endereco']
    bairro = request.form['bairro']
    cep = request.form['cep']
    cidade = request.form['cidade']
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "INSERT INTO joaoCosta_TB_client (cpf, nome, email, endereco, bairro, cep, cidade) VALUES (%s, %s, %s, %s, %s, %s, %s)" #Variável de texto de um comando SQL que vai executar dentro do Banco de Dados (vai criar uma tabela chamada clientes e vai inserir os atributos usuario e senha)
    values = (cpf, nome, email, endereco, bairro, cep, cidade)
    mycursor.execute(query, values)
    db.commit()
    return redirect (url_for("cadastrar_cliente"))

@app.route("/excluir_usuario/<usuario>") #<usuario> cria uma rota dinâmica, para cada usuário que for excluir, ele cria uma rota, no caso ele vai colocar o nome do usuário, exemplo: "/excluir_usuario/admin"
def excluir_usuario(usuario):
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "delete FROM joaoCosta_TB_user WHERE usuario = '" + usuario + "'"
    mycursor.execute(query)
    db.commit() 
    return redirect(url_for("cadastrar_usuario"))

@app.route("/alterar_usuario/<user>")
def alterar_usuario(user):
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco")
    mycursor = db.cursor()
    query = "select usuario, email, senha from joaoCosta_TB_user where usuario = '" + user + "'"
    mycursor.execute(query) #Tem todo o resultado da query
    resultado = mycursor.fetchall() #Pega todas as linhas que encontrou e coloca dentro da varáivel "resultado"
    return render_template("altera_user.html", usuarios=resultado)

@app.route("/gravar_alteracao_usuario", methods=['POST'])
def gravar_usuario():
    usuario = request.form['usuario']
    usuario_anterior = request.form['usuario_anterior']
    senha = request.form['senha']
    email = request.form['email']
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "UPDATE joaoCosta_TB_user SET usuario = '" + usuario + "', senha = '" + senha + "', email = '" + email + "' WHERE usuario = '" + usuario_anterior +"'"
    mycursor.execute(query)
    db.commit()
    return redirect (url_for("cadastrar_usuario"))
    
@app.route("/excluir_cliente/<cliente>") #<usuario> cria uma rota dinâmica, para cada usuário que for excluir, ele cria uma rota, no caso ele vai colocar o nome do usuário, exemplo: "/excluir_usuario/admin"
def excluir_cliente(cliente):
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "DELETE FROM joaoCosta_TB_client WHERE cpf = '" + cliente + "'"
    mycursor.execute(query)
    db.commit() 
    return redirect(url_for("cadastrar_cliente"))

@app.route("/alterar_cliente/<cliente>")
def alterar_cliente(cliente):
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco")
    mycursor = db.cursor()
    query = "select cpf, nome, email, endereco, bairro, cep, cidade from joaoCosta_TB_client where cpf = '" + cliente + "'"
    mycursor.execute(query) #Tem todo o resultado da query
    resultado = mycursor.fetchall() #Pega todas as linhas que encontrou e coloca dentro da varáivel "resultado"
    return render_template("altera_client.html", cliente=resultado)

@app.route("/gravar_alteracao_cliente", methods=['POST'])
def gravar_cliente():
    cpf = request.form['cpf']
    cpf_anterior = request.form['cpf_anterior']
    nome = request.form['nome']
    email = request.form['email']
    endereco = request.form['endereco']
    bairro = request.form['bairro']
    cep = request.form['cep']
    cidade = request.form['cidade']
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "UPDATE joaoCosta_TB_client SET cpf = %s, nome = %s, email = %s, endereco = %s, bairro = %s, cep = %s, cidade = %s  WHERE cpf = %s"
    values = (cpf, nome, email, endereco, bairro, cep, cidade, cpf_anterior)
    mycursor.execute(query, values)
    db.commit()
    return redirect (url_for("cadastrar_cliente"))

app.run()