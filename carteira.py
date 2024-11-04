# carteira.py
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid
from db_functions import adicionar_investimento, obter_investimentos_usuario

def exibir_carteira_usuario(user_id):
    st.title("Sua Carteira de Investimentos")

    with st.form(key="form_investimento"):
        
        ativo_df = pd.read_csv("tickers_ibra.csv", index_col=0)
        ativo_selecionado = st.selectbox("Selecione a Empresa", options=ativo_df, help='Escolha o código da empresa')
        ticker = f"{ativo_selecionado}" 
        
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        preco = st.number_input("Preço por Unidade", min_value=0.0, step=0.01)
        if st.form_submit_button("Adicionar Investimento"):
            adicionar_investimento(user_id, ticker, quantidade, preco)
            st.success("Investimento adicionado com sucesso!")
    
    st.subheader("Seus Investimentos")
    investimentos = obter_investimentos_usuario(user_id)
    for inv in investimentos:
        st.write(f"Ativo: {inv['ativo']}, Quantidade: {inv['quantidade']}, Preço: R${inv['preco']:.2f}")
