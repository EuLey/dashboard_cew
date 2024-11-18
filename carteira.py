# carteira.py
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
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

    if investimentos:  # Verifica se a lista está preenchida
        df = pd.DataFrame(investimentos)
    
        # Adicionar o filtro de ativos
        ativos_disponiveis = df['ativo'].unique()  # Lista de ativos únicos
        ativos_selecionados = st.multiselect("Filtrar por Ativos", ativos_disponiveis, default=ativos_disponiveis)

        # Filtrar o DataFrame com base nos ativos selecionados
        df_filtrado = df[df['ativo'].isin(ativos_selecionados)]
        
        # Agrupar ativos com o mesmo nome
        df_grouped = df_filtrado.groupby('ativo', as_index=False).agg({
            'quantidade': 'sum',  # Soma das quantidades
            'preco': 'mean',      # Média dos preços (pode ajustar para 'sum' se necessário)
        })
        
        # Calcular o Valor Total de cada ativo
        df_grouped['Valor Total'] = df_grouped['quantidade'] * df_grouped['preco']
        
        # Calcular o Valor Total da Carteira
        valor_total_carteira = df_grouped['Valor Total'].sum()
        
        # Calcular o percentual de cada ativo na carteira
        df_grouped['% da Carteira'] = (df_grouped['Valor Total'] / valor_total_carteira) * 100

        # Exibir o valor total da carteira
        st.write(f"Valor Total da Carteira: R$ {valor_total_carteira:.2f}")
        
        # Exibir a tabela agrupada
        st.dataframe(df_grouped[['ativo', 'quantidade', 'preco', 'Valor Total', '% da Carteira']])

        # Gerar o gráfico de pizza
        fig = px.pie(df_grouped, values='Valor Total', names='ativo', title='Distribuição da Carteira')
        st.plotly_chart(fig)
    else:
        st.write("Sua carteira está vazia. Adicione investimentos para visualizar.")