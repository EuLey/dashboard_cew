import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import locale
from db_functions import adicionar_investimento, obter_investimentos_usuario

# Configurar a localização para Português (Brasil)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def exibir_carteira_usuario(user_id):
    st.title("Sua Carteira de Investimentos")

    # Formulário de adição de investimentos
    with st.form(key="form_investimento"):
        ativo_df = pd.read_csv("tickers_ibra.csv", index_col=0)
        ativo_selecionado = st.selectbox("Selecione a Empresa", options=ativo_df, help='Escolha o código da empresa')
        
        if ativo_selecionado:
            ticker_data = yf.Ticker(f"{ativo_selecionado}.SA")
            preco = ticker_data.history(period="1d")['Close'].iloc[-1]
            st.write(f"Preço Atual de {ativo_selecionado}: R$ {preco:.2f}")
        else:
            preco = 0.0

        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        valor_total = preco * quantidade
        st.write(f"Valor Total do Investimento: R$ {valor_total:.2f}")

        if st.form_submit_button("Adicionar Investimento"):
            adicionar_investimento(user_id, ativo_selecionado, quantidade, preco)
            st.success("Investimento adicionado com sucesso!")
    
    # Exibir os investimentos
    st.subheader("Seus Investimentos")
    investimentos = obter_investimentos_usuario(user_id)

    if investimentos:
        df = pd.DataFrame(investimentos)
        ativos_disponiveis = df['ativo'].unique()
        ativos_selecionados = st.multiselect("Filtrar por Ativos", ativos_disponiveis, default=ativos_disponiveis)

        # Filtro de data com formato brasileiro
        st.subheader("Filtro de Rentabilidade por Período")
        data_inicio = st.date_input("Data Inicial", value=pd.Timestamp.today() - pd.Timedelta(days=30)).strftime('%d/%m/%Y')
        data_fim = st.date_input("Data Final", value=pd.Timestamp.today()).strftime('%d/%m/%Y')

        # Converter as datas para o formato ISO (necessário para cálculos e API)
        data_inicio_iso = pd.to_datetime(data_inicio, format='%d/%m/%Y')
        data_fim_iso = pd.to_datetime(data_fim, format='%d/%m/%Y')

        if data_inicio_iso > data_fim_iso:
            st.error("A data inicial não pode ser maior que a data final!")
            return

        df_filtrado = df[df['ativo'].isin(ativos_selecionados)]
        df_grouped = df_filtrado.groupby('ativo', as_index=False).agg({'quantidade': 'sum', 'preco': 'mean'})

        def calcular_rentabilidade(ativo):
            ticker = yf.Ticker(f"{ativo}.SA")
            preco_inicio_df = ticker.history(start=data_inicio_iso, end=data_inicio_iso + pd.Timedelta(days=1))
            preco_fim_df = ticker.history(start=data_fim_iso, end=data_fim_iso + pd.Timedelta(days=1))

            if preco_inicio_df.empty or preco_fim_df.empty:
                return None, None

            preco_inicio = preco_inicio_df['Close'].iloc[-1]
            preco_fim = preco_fim_df['Close'].iloc[-1]
            return preco_inicio, preco_fim

        df_grouped[['Preço Início', 'Preço Fim']] = df_grouped['ativo'].apply(
            lambda ativo: pd.Series(calcular_rentabilidade(ativo))
        )

        df_grouped = df_grouped.dropna(subset=['Preço Início', 'Preço Fim'])
        df_grouped['Rentabilidade (%)'] = ((df_grouped['Preço Fim'] - df_grouped['Preço Início']) / df_grouped['Preço Início']) * 100

        valor_total_carteira = df_grouped['quantidade'].sum() * df_grouped['preco'].mean()
        df_grouped['Valor Total'] = df_grouped['quantidade'] * df_grouped['preco']
        df_grouped['% da Carteira'] = (df_grouped['Valor Total'] / valor_total_carteira) * 100

        st.write(f"Valor Total da Carteira: R$ {valor_total_carteira:.2f}")
        st.dataframe(df_grouped[['ativo', 'quantidade', 'preco', 'Preço Início', 'Preço Fim', 'Rentabilidade (%)', 'Valor Total', '% da Carteira']])

        fig = px.pie(df_grouped, values='Valor Total', names='ativo', title='Distribuição da Carteira')
        st.plotly_chart(fig)
    else:
        st.write("Sua carteira está vazia. Adicione investimentos para visualizar.")
