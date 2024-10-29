import streamlit as st
import mysql.connector
import bcrypt  
from streamlit_extras.switch_page_button import switch_page 


# Configuração da página
st.set_page_config(
    page_icon=':moneybag:',
    page_title="Cadastro"
)

st.title(":owl: Organizando suas ações!")
st.write("Insira os dados para cadastro:")

# Função para conectar ao banco de dados MySQL
def conectar_bd():
    conexao = mysql.connector.connect(
        host="localhost",  # Pode ser diferente dependendo do seu servidor
        user="root",       # Seu usuário do MySQL
        database="cadastro_dash"  # Nome do banco de dados que você criou
    )
    return conexao

# Criando a conexão
conexao = conectar_bd()

# Função para inserir dados no banco de dados
def inserir_usuario(nome, email, cpf, data_nascimento, senha):
    cursor = conexao.cursor()
    sql = "INSERT INTO usuarios (nome, email, cpf, data_nascimento, senha) VALUES (%s, %s, %s, %s, %s)"
    valores = (nome, email, cpf, data_nascimento, senha)
    cursor.execute(sql, valores)
    conexao.commit()
    cursor.close()

# Formulário de cadastro no Streamlit
form = st.form(key="cadastro", clear_on_submit=True)

with form:
    input_name = st.text_input("Nome ", placeholder="Insira seu nome completo")
    input_email = st.text_input("E-mail ", placeholder="Insira seu e-mail")
    input_cpf = st.text_input("CPF ", placeholder="Insira seu CPF")
    input_date = st.text_input("Data de nascimento ", placeholder="DD/MM/YYYY")
    input_password = st.text_input("Senha ", placeholder="Insira sua senha", type="password")

    botao_submit = form.form_submit_button("Confirmar")

# Se o formulário for enviado, insere os dados no banco de dados
if botao_submit:
    # Validação simples antes de inserir
    if input_name and input_email and input_cpf and input_date and input_password:
        # Criptografando a senha antes de salvar no banco
        hashed_password = bcrypt.hashpw(input_password.encode('utf-8'), bcrypt.gensalt())

        # Inserindo o usuário com a senha criptografada
        inserir_usuario(input_name, input_email, input_cpf, input_date, hashed_password)

        st.success("Usuário cadastrado com sucesso!")
        switch_page("login")
    else:
        st.error("Por favor, preencha todos os campos!")
