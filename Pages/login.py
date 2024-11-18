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

# Função para validar o login do usuário e retornar o user_id
def validar_login(email, senha):
    cursor = conexao.cursor()
    sql = "SELECT id, senha FROM usuarios WHERE email = %s"
    cursor.execute(sql, (email,))
    resultado = cursor.fetchone()
    cursor.close()

    if resultado:
        user_id, senha_armazenada = resultado
        if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada.encode('utf-8')):
            return user_id
    return None

# Função para verificar se o usuário está logado
def verificar_login():
    return st.session_state.get('logado', False)

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
            user_id = validar_login(input_email, input_password)
            if user_id:
                st.success("Login realizado com sucesso!")
                
                # Armazena os dados do usuário na sessão
                st.session_state['logado'] = True
                st.session_state['usuario'] = input_email
                st.session_state['user_id'] = user_id  # Armazena o ID do usuário

                # Redireciona para a página "home"
                switch_page("home")
            else:
                st.error("E-mail ou senha incorretos.")
        else:
            st.error("Por favor, preencha todos os campos.")
