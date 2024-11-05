# carteira.py
import streamlit as st
import pandas as pd
import yfinance as yf
from db_functions import adicionar_investimento, obter_investimentos_usuario

def exibir_carteira_usuario(user_id):
    st.title("Sua Carteira de Investimentos")

    with st.form(key="form_investimento"):
        # Seleção do ativo
        ativo_df = pd.read_csv("tickers_ibra.csv", index_col=0)
        ativo_selecionado = st.selectbox("Selecione a Empresa", options=ativo_df, help='Escolha o código da empresa')
        
        if ativo_selecionado:
            # Obtém o preço atual do ativo
            ticker_data = yf.Ticker(f"{ativo_selecionado}.SA")
            preco = ticker_data.history(period="1d")['Close'].iloc[-1]  # Preço de fechamento mais recente
            st.write(f"Preço Atual de {ativo_selecionado}: R$ {preco:.2f}")
        else:
            preco = 0.0

        # Seleção da quantidade
        quantidade = st.number_input("Quantidade", min_value=1, step=1)

        # Calcula o valor total com base na quantidade selecionada
        valor_total = preco * quantidade
        st.write(f"Valor Total do Investimento: R$ {valor_total:.2f}")

        # Adiciona o investimento ao banco de dados
        if st.form_submit_button("Adicionar Investimento"):
            adicionar_investimento(user_id, ativo_selecionado, quantidade, preco)
            st.success("Investimento adicionado com sucesso!")
    
    # Exibe a lista de investimentos
    st.subheader("Seus Investimentos")
    investimentos = obter_investimentos_usuario(user_id)
    for inv in investimentos:
        st.write(f"Ativo: {inv['ativo']}, Quantidade: {inv['quantidade']}, Preço: R$ {inv['preco']:.2f}")
