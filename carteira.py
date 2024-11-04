import streamlit as st
import pandas as pd
import yfinance as yf
from db_functions import adicionar_investimento, obter_investimentos_usuario

def exibir_carteira_usuario(user_id):
    st.title("Sua Carteira de Investimentos")

    with st.form(key="form_investimento"):
        # Carregar os tickers disponíveis
        ativo_df = pd.read_csv("tickers_ibra.csv", index_col=0)
        ativo_selecionado = st.selectbox("Selecione a Empresa", options=ativo_df, help='Escolha o código da empresa')

        quantidade = st.number_input("Quantidade", min_value=1, step=1)

        # Verificar o preço atual do ativo
        if ativo_selecionado:
            ticker = f"{ativo_selecionado}.SA"  # Adicionar o sufixo para ativos da B3
            ticker_data = yf.Ticker(ticker)
            preco_data = ticker_data.history(period="1d")

            # Validar se há dados disponíveis para o ativo
            if not preco_data.empty:
                preco = preco_data['Close'].iloc[-1]  # Preço de fechamento mais recente
                st.write(f"Preço Atual do {ativo_selecionado}: R$ {preco:.2f}")
            else:
                st.write("Preço atual não disponível.")
                preco = 0.0  # Preço padrão se não houver dados

        if st.form_submit_button("Adicionar Investimento"):
            adicionar_investimento(user_id, ativo_selecionado, quantidade, preco)
            st.success("Investimento adicionado com sucesso!")
   
    # Exibir os investimentos do usuário
    st.subheader("Seus Investimentos")
    investimentos = obter_investimentos_usuario(user_id)
    for inv in investimentos:
        st.write(f"Ativo: {inv['ativo']}, Quantidade: {inv['quantidade']}, Preço: R${inv['preco']:.2f}")
