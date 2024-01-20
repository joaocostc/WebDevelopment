from flask import Flask, request, redirect, render_template, url_for, flash
import mysql.connector 

app = Flask (__name__)
app.secret_key = 'senha123'

@app.route('/')
def index():
    return render_template ("index.html")

@app.route('/login_aluno')
def login_aluno():
    return render_template ("login_aluno.html")

@app.route('/home_aluno', methods=['POST'])
def home_aluno():
    cpf_login = request.form['cpf_login']
    senha = request.form['senha']

    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()

    # Verifique a autenticação do aluno
    query_autenticacao = "SELECT NOME, CPF FROM joaoCosta_TB_aluno WHERE CPF = %s AND SENHA = %s"
    mycursor.execute(query_autenticacao, (cpf_login, senha))
    resultado_autenticacao = mycursor.fetchall()
    if resultado_autenticacao:
        query_disciplinas_notas = """
            SELECT d.NOME_DISCIPLINA, n.NOTA_1, n.NOTA_2, n.NOTA_3, n.NOTA_4, n.MEDIA
            FROM joaoCosta_TB_aluno a
            JOIN joaoCosta_TB_notas n ON a.ID_ALUNO = n.ID_ALUNO
            JOIN joaoCosta_TB_disciplina d ON n.ID_DISCIPLINA = d.ID_DISCIPLINA
            WHERE a.CPF = %s
        """
        mycursor.execute(query_disciplinas_notas, (cpf_login,))
        resultado_disciplinas_notas = mycursor.fetchall()
        return render_template("home_aluno.html", aluno_selecionado=resultado_autenticacao, disciplinas_notas=resultado_disciplinas_notas)
    else:
        flash('Credenciais de login incorretas. Tente novamente.', 'error')
        return redirect("/login_aluno") 

@app.route('/login_gestao')
def login_gestao():
    return render_template("login_gestao.html")

@app.route('/home_gestao', methods=['POST'])
def home_gestao():
    login = request.form['login']
    senha = request.form['senha']

    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()

    query_autenticacao = "SELECT LOGIN, SENHA FROM joaoCosta_TB_secretaria WHERE LOGIN = %s AND SENHA = %s"
    mycursor.execute(query_autenticacao, (login, senha))
    resultado_autenticacao = mycursor.fetchone()

    if resultado_autenticacao:
        return render_template("home_gestao.html")
    else:
        flash('Credenciais de login incorretas. Tente novamente.', 'error')
        return render_template("login_gestao.html")

@app.route('/cadastro_aluno')
def cadastro_aluno():
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco")
    mycursor = db.cursor()
    query = "SELECT CPF, NOME from joaoCosta_TB_aluno"
    mycursor.execute(query) #Tem todo o resultado da query
    resultado = mycursor.fetchall() #Pega todas as linhas que encontrou e coloca dentro da varáivel "resultado"
    return render_template("cadastro_aluno.html", cpfs=resultado)

@app.route('/processar_aluno', methods=['POST'])
def processar_aluno():
    cpf = request.form['cpf']
    nome = request.form['nome']
    senha = request.form['senha']

    # Conectar ao banco de dados
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()

    # Verificar se o CPF já está cadastrado
    query_verificacao = "SELECT * FROM joaoCosta_TB_aluno WHERE CPF = %s"
    mycursor.execute(query_verificacao, (cpf,))
    cpf_existente = mycursor.fetchone()

    if cpf_existente:
        flash('CPF já cadastrado. Insira outro CPF.', 'error')
        return redirect (url_for("cadastro_aluno"))

    # Se o CPF não existe, proceda com a inserção
    query_insercao = "INSERT INTO joaoCosta_TB_aluno (CPF, NOME, SENHA) VALUES (%s, %s, %s)"
    values = (cpf, nome, senha)
    mycursor.execute(query_insercao, values)
    db.commit()
    return redirect (url_for("cadastro_aluno"))

@app.route("/excluir_aluno/<cpf>") #<usuario> cria uma rota dinâmica, para cada usuário que for excluir, ele cria uma rota, no caso ele vai colocar o nome do usuário, exemplo: "/excluir_usuario/admin"
def excluir_aluno(cpf):
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "DELETE FROM joaoCosta_TB_aluno WHERE CPF = '" + cpf + "'"
    mycursor.execute(query)
    db.commit() 
    return redirect(url_for("cadastro_aluno"))

@app.route("/alterar_aluno/<cpf>")
def alterar_aluno(cpf):
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco")
    mycursor = db.cursor()
    query = "SELECT CPF, NOME, senha from joaoCosta_TB_aluno where CPF = '" + cpf + "'"
    mycursor.execute(query) #Tem todo o resultado da query
    resultado = mycursor.fetchall() #Pega todas as linhas que encontrou e coloca dentro da varáivel "resultado"
    return render_template("altera_aluno.html", cpfs=resultado)

@app.route("/gravar_aluno", methods=['POST'])
def gravar_aluno():
    cpf = request.form['cpf']
    cpf_anterior = request.form['cpf_anterior']
    nome = request.form['nome']
    senha = request.form['senha']
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "UPDATE joaoCosta_TB_aluno SET CPF = '" + cpf + "', NOME = '" + nome + "', SENHA = '" + senha + "' WHERE CPF = '" + cpf_anterior +"'"
    mycursor.execute(query)
    db.commit()
    return redirect (url_for("cadastro_aluno"))

@app.route('/cadastro_secretaria')
def cadastro_secretaria():
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco")
    mycursor = db.cursor()
    query = "SELECT CPF, NOME, EMAIL, LOGIN, SENHA from joaoCosta_TB_secretaria"
    mycursor.execute(query) #Tem todo o resultado da query
    resultado = mycursor.fetchall() #Pega todas as linhas que encontrou e coloca dentro da varáivel "resultado"
    return render_template("cadastro_secretaria.html", cpfs=resultado)

@app.route('/processar_secretaria', methods=['POST'])
def processar_secretaria():
    cpf = request.form['cpf']
    nome = request.form['nome']
    email = request.form['email']
    login = request.form['login']
    senha = request.form['senha']

    # Função para verificar se o CPF já existe
    def cpf_exists(cpf):
        db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com",
                                     user="aluno_fatec", password="aluno_fatec", database="meu_banco")
        mycursor = db.cursor()
        query = "SELECT CPF FROM joaoCosta_TB_secretaria WHERE CPF = %s"
        value = (cpf,)
        mycursor.execute(query, value)
        result = mycursor.fetchone()
        return result is not None

    # Verifica se o CPF já existe no banco de dados
    if cpf_exists(cpf):
        flash('CPF já cadastrado. Insira outro CPF.', 'error')
        return redirect (url_for("cadastro_secretaria"))

    # Se o CPF não existe, insere o novo registro
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com",
                                 user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "INSERT INTO joaoCosta_TB_secretaria (CPF, NOME, EMAIL, LOGIN, SENHA) VALUES (%s, %s, %s, %s, %s)"
    values = (cpf, nome, email, login, senha)
    mycursor.execute(query, values)
    db.commit()
    return redirect(url_for("cadastro_secretaria"))

@app.route("/excluir_secretaria/<cpf>") #<usuario> cria uma rota dinâmica, para cada usuário que for excluir, ele cria uma rota, no caso ele vai colocar o nome do usuário, exemplo: "/excluir_usuario/admin"
def excluir_secretaria(cpf):
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "DELETE FROM joaoCosta_TB_secretaria WHERE CPF = '" + cpf + "'"
    mycursor.execute(query)
    db.commit() 
    return redirect(url_for("cadastro_secretaria"))

@app.route("/alterar_secretaria/<cpf>")
def alterar_secretaria(cpf):
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco")
    mycursor = db.cursor()
    query = "SELECT CPF, NOME, EMAIL, LOGIN, SENHA from joaoCosta_TB_secretaria where CPF = '" + cpf + "'"
    mycursor.execute(query) #Tem todo o resultado da query
    resultado = mycursor.fetchall() #Pega todas as linhas que encontrou e coloca dentro da varáivel "resultado"
    return render_template("altera_secretaria.html", cpfs=resultado)

@app.route("/gravar_secretaria", methods=['POST'])
def gravar_secretaria():
    cpf = request.form['cpf']
    cpf_anterior = request.form['cpf_anterior']
    nome = request.form['nome']
    email = request.form['email']
    login = request.form['login']
    senha = request.form['senha']
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "UPDATE joaoCosta_TB_secretaria SET CPF = '" + cpf + "', NOME = '" + nome + "', EMAIL = '" + email + "', LOGIN = '" + login + "', SENHA= '" + senha + "' WHERE CPF = '" + cpf_anterior +"'"
    mycursor.execute(query)
    db.commit()
    return redirect (url_for("cadastro_secretaria"))

@app.route('/cadastro_disciplina')
def cadastro_disciplina():
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco")
    mycursor = db.cursor()
    query = "SELECT ID_DISCIPLINA, NOME_DISCIPLINA from joaoCosta_TB_disciplina"
    mycursor.execute(query) #Tem todo o resultado da query
    resultado = mycursor.fetchall() #Pega todas as linhas que encontrou e coloca dentro da varáivel "resultado"
    return render_template("cadastro_disciplina.html", disciplinas=resultado)

@app.route('/processar_disciplina', methods=['POST'])
def processar_disciplina():
    nome_disciplina = request.form['nome_disciplina']
    nome_disciplina.upper()
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query_verificar_disciplina = "SELECT NOME_DISCIPLINA FROM joaoCosta_TB_disciplina WHERE NOME_DISCIPLINA = %s"
    mycursor.execute(query_verificar_disciplina, (nome_disciplina,))
    disciplina_existente = mycursor.fetchone()
    if disciplina_existente:
        flash('Disciplina já Cadastrada. Insira outra disciplina.', 'error')
        return redirect (url_for("cadastro_disciplina"))
    query_inserir_disciplina = "INSERT INTO joaoCosta_TB_disciplina (NOME_DISCIPLINA) VALUES (%s)"
    values = (nome_disciplina,)
    mycursor.execute(query_inserir_disciplina, values)
    db.commit()
    return redirect(url_for("cadastro_disciplina"))

@app.route("/excluir_disciplina/<disciplina>") 
def excluir_disciplina(disciplina):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    print(disciplina)
    query_verificar_notas = "SELECT ID_NOTAS FROM joaoCosta_TB_notas n JOIN joaoCosta_TB_disciplina d ON n.ID_DISCIPLINA = d.ID_DISCIPLINA WHERE d.NOME_DISCIPLINA = %s"
    mycursor.execute(query_verificar_notas, (disciplina,))
    notas_associadas = mycursor.fetchall()
    query_excluir_disciplina = "DELETE FROM joaoCosta_TB_disciplina WHERE ID_DISCIPLINA = %s"
    mycursor.execute(query_excluir_disciplina, (disciplina,))
    db.commit()
    return redirect(url_for("cadastro_disciplina"))

@app.route("/alterar_disciplina/<disciplina>")
def alterar_disciplina(disciplina):
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco")
    mycursor = db.cursor()
    query = "SELECT NOME_DISCIPLINA FROM joaoCosta_TB_disciplina where ID_DISCIPLINA = '" + disciplina + "'"
    mycursor.execute(query) #Tem todo o resultado da query
    resultado = mycursor.fetchall() #Pega todas as linhas que encontrou e coloca dentro da varáivel "resultado"
    return render_template("altera_disciplina.html", disciplinas=resultado)

@app.route("/gravar_disciplina", methods=['POST'])
def gravar_disciplina():
    disciplina = request.form['nome_disciplina']
    disciplina_anterior = request.form['disciplina_anterior']
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "UPDATE joaoCosta_TB_disciplina SET NOME_DISCIPLINA = '" + disciplina + "' WHERE NOME_DISCIPLINA = '" + disciplina_anterior + "'"
    mycursor.execute(query)
    db.commit()
    return redirect (url_for("cadastro_disciplina"))

def calcular_media(nota_1, nota_2, nota_3, nota_4):
    notas = [float(nota_1), float(nota_2), float(nota_3), float(nota_4)]
    media = sum(notas) / len(notas)
    return media

@app.route('/cadastro_nota')
def cadastro_nota():
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()

    # Consulta para obter nomes de alunos
    query_aluno = "SELECT NOME FROM joaoCosta_TB_aluno"
    mycursor.execute(query_aluno)
    alunos = mycursor.fetchall()

    # Consulta para obter nomes de disciplinas
    query_disciplina = "SELECT NOME_DISCIPLINA FROM joaoCosta_TB_disciplina"
    mycursor.execute(query_disciplina)
    disciplinas = mycursor.fetchall()

    # Consulta principal
    query = """SELECT 
        joaoCosta_TB_aluno.NOME AS NOME_ALUNO, 
        joaoCosta_TB_aluno.CPF AS CPF_ALUNO,
        joaoCosta_TB_notas.ID_NOTAS,
        joaoCosta_TB_notas.ID_ALUNO, 
        joaoCosta_TB_notas.NOTA_1, 
        joaoCosta_TB_notas.NOTA_2, 
        joaoCosta_TB_notas.NOTA_3, 
        joaoCosta_TB_notas.NOTA_4,
        joaoCosta_TB_notas.MEDIA,
        joaoCosta_TB_disciplina.NOME_DISCIPLINA,
        joaoCosta_TB_notas.ID_DISCIPLINA
        FROM 
        joaoCosta_TB_aluno
        JOIN 
        joaoCosta_TB_notas ON joaoCosta_TB_aluno.ID_ALUNO = joaoCosta_TB_notas.ID_ALUNO
        JOIN
        joaoCosta_TB_disciplina ON joaoCosta_TB_notas.ID_DISCIPLINA = joaoCosta_TB_disciplina.ID_DISCIPLINA
        ORDER BY 
        joaoCosta_TB_notas.DATA_INSERCAO"""
    
    mycursor.execute(query)
    resultado = mycursor.fetchall()

    return render_template("cadastro_nota.html", alunos=alunos, disciplinas=disciplinas, notas=resultado)

@app.route('/processar_nota', methods=['POST'])
def processar_nota():
    aluno_selecionado = request.form['aluno']
    disciplina_selecionada = request.form['disciplina']
    
    # Convertendo as notas para float
    nota_1 = float(request.form['nota_1'])
    nota_2 = float(request.form['nota_2'])
    nota_3 = float(request.form['nota_3'])
    nota_4 = float(request.form['nota_4'])
    
    media = calcular_media(nota_1, nota_2, nota_3, nota_4)

    # Verificar se as notas estão no intervalo permitido
    if not (0 <= nota_1 <= 10) or not (0 <= nota_2 <= 10) or not (0 <= nota_3 <= 10) or not (0 <= nota_4 <= 10):
        flash('Notas devem estar entre 0 e 10.', 'error')
        return redirect(url_for("cadastro_nota"))
    # Conectar ao banco de dados
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()

    # Obter o ID da disciplina
    query_disciplina = "SELECT ID_DISCIPLINA FROM joaoCosta_TB_disciplina WHERE NOME_DISCIPLINA = %s"
    mycursor.execute(query_disciplina, (disciplina_selecionada,))
    result_disciplina = mycursor.fetchone()
    id_disciplina = result_disciplina[0] if result_disciplina else None

    # Obter o ID do aluno
    query_aluno = "SELECT ID_ALUNO FROM joaoCosta_TB_aluno WHERE NOME = %s"
    mycursor.execute(query_aluno, (aluno_selecionado,))
    result_aluno = mycursor.fetchone()
    id_aluno = result_aluno[0] if result_aluno else None

    # Verificar se a disciplina já foi cadastrada para o aluno
    query_verificar_disciplina = "SELECT ID_NOTAS FROM joaoCosta_TB_notas WHERE ID_ALUNO = %s AND ID_DISCIPLINA = %s"
    mycursor.execute(query_verificar_disciplina, (id_aluno, id_disciplina))
    result_verificar_disciplina = mycursor.fetchone()


    if result_verificar_disciplina:
        # Disciplina já cadastrada para o aluno, você pode lidar com isso aqui (ex: exibir uma mensagem de erro)
        flash('Notas para essa Disciplina já foram cadastradas para esse aluno, verifique os dados.', 'error')
        return redirect(url_for("cadastro_nota"))

    # Inserir a nota no banco de dados
    query_inserir_nota = "INSERT INTO joaoCosta_TB_notas (ID_ALUNO, ID_DISCIPLINA, NOTA_1, NOTA_2, NOTA_3, NOTA_4, MEDIA) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (id_aluno, id_disciplina, nota_1, nota_2, nota_3, nota_4, media)
    mycursor.execute(query_inserir_nota, values)
    # Commitar a transação e fechar a conexão
    db.commit()
    db.close()

    return redirect(url_for("cadastro_nota"))

@app.route("/excluir_nota/<int:notas>") 
def excluir_nota(notas):
    db = mysql.connector.connect(host= "mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database= "meu_banco") #Cria uma conexão com o Banco de Dados
    mycursor = db.cursor() #Agora nesse Banco eu quero executar um comando dentro dele
    query = "DELETE FROM joaoCosta_TB_notas WHERE ID_NOTAS = %s"
    mycursor.execute(query, (notas,))
    db.commit() 
    return redirect(url_for("cadastro_nota"))

@app.route("/alterar_nota/<int:notas>")
def alterar_nota(notas):
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "SELECT ID_NOTAS, NOTA_1, NOTA_2, NOTA_3, NOTA_4 FROM joaoCosta_TB_notas WHERE ID_NOTAS = %s"
    mycursor.execute(query, (notas,))
    resultado = mycursor.fetchall()
    return render_template("altera_nota.html", notas=resultado, id_notas=notas)

@app.route("/gravar_nota", methods=['POST'])
def gravar_nota():
    captura_id_notas = request.form['id_notas']
    nota_1 = float(request.form['nota_1'])
    nota_2 = float(request.form['nota_2'])
    nota_3 = float(request.form['nota_3'])
    nota_4 = float(request.form['nota_4'])
    db = mysql.connector.connect(host="mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com", user="aluno_fatec", password="aluno_fatec", database="meu_banco")
    mycursor = db.cursor()
    query = "UPDATE joaoCosta_TB_notas SET NOTA_1 = %s, NOTA_2 = %s, NOTA_3 = %s, NOTA_4 = %s WHERE ID_NOTAS = %s"
    values = (nota_1, nota_2, nota_3, nota_4, captura_id_notas)
    mycursor.execute(query, values)
    db.commit()
    return redirect(url_for("cadastro_nota"))

app.run()