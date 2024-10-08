import streamlit as st


st.set_page_config(
    page_icon= ':moneybag:'
)

st.title("Home")

# Verificar se o usuário está logado
if 'logado' in st.session_state and st.session_state['logado']:
    st.title("Bem-vindo à sua página inicial!")
    st.write(f"Olá, {st.session_state['usuario']}, você está logado.")

    if st.button("Sair"):
        st.session_state['logado'] = False
        st.session_state['usuario'] = None

        # Redirecionar para a página de login
        st.experimental_set_query_params(page="login")
else:
    # Se não estiver logado, redireciona para a página de login
    st.experimental_set_query_params(page="login")
