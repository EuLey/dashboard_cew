import streamlit as st
import mysql.connector
import bcrypt
from streamlit_extras.switch_page_button import switch_page 


# Função para conectar ao banco de dados MySQL
def conectar_bd():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        database="cadastro_dash"
    )
    return conexao

conexao = conectar_bd()

# Função para validar o login do usuário
def validar_login(email, senha):
    cursor = conexao.cursor()
    sql = "SELECT senha FROM usuarios WHERE email = %s"
    cursor.execute(sql, (email,))
    resultado = cursor.fetchone()
    cursor.close()

    if resultado:
        senha_armazenada = resultado[0]
        if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada.encode('utf-8')):
            return True
    return False

# Função para verificar se o usuário está logado
def verificar_login():
    if 'logado' in st.session_state and st.session_state['logado']:
        return True
    return False

# Se o usuário já estiver logado, redireciona para a home
if verificar_login():
    switch_page("home") 
else:
    # Formulário de login
    st.title("Login")
    form = st.form(key="login_form", clear_on_submit=True)

    with form:
        input_email = st.text_input("E-mail", placeholder="Insira seu e-mail")
        input_password = st.text_input("Senha", placeholder="Insira sua senha", type="password")
        botao_login = form.form_submit_button("Login")

    # Se o formulário de login for enviado
    if botao_login:
        if input_email and input_password:
            if validar_login(input_email, input_password):
                st.success("Login realizado com sucesso!")
                st.session_state['logado'] = True
                st.session_state['usuario'] = input_email

                # Simular redirecionamento para home.py usando parâmetros na URL
                st.experimental_set_query_params(page="home")
                switch_page("home") 
            else:
                st.error("E-mail ou senha incorretos.")
        else:
            st.error("Por favor, preencha todos os campos.")
