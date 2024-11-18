import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from carteira import exibir_carteira_usuario  # Importe a função para exibir a carteira

# Configuração da página
st.set_page_config(
    page_icon=':moneybag:',
    page_title="Home"
)

# Título da página
st.title("Home")

# Verificação de login do usuário
if 'logado' in st.session_state and st.session_state['logado']:
    user_id = st.session_state.get('user_id')

    # Botão de logout
    if st.sidebar.button("Sair"):
        st.session_state['logado'] = False
        st.session_state.pop('user_id', None)  # Remove o ID do usuário da sessão
        st.session_state.pop('usuario', None)   # Remove o e-mail do usuário da sessão
        switch_page("login")  # Redireciona para a página de login

    # Menu de navegação na barra lateral
    menu_option = st.sidebar.radio("Navegar", ["Minha Carteira", "Análise de Mercado"])

    if menu_option == "Minha Carteira":
        exibir_carteira_usuario(user_id) 
        st.write(f"{st.session_state['usuario']}, aqui está sua carteira de investimentos.")  # Exibe a carteira do usuário logado
    elif menu_option == "Análise de Mercado":
        switch_page("dash")  # Redireciona para a view `dash.py`

else:
    switch_page("login")  # Redireciona para a página de login caso o usuário não esteja logado
    
