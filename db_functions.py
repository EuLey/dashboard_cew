# db_functions.py
import mysql.connector
from datetime import date
import yfinance as yf

def conectar_bd():
    # Função para conectar ao banco de dados MySQL
    return mysql.connector.connect(host="localhost", user="root", database="cadastro_dash")

def adicionar_investimento(user_id, ativo, quantidade, preco, data=None):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    if data is None:
        data = date.today()  # Data atual como padrão
    sql = "INSERT INTO carteira_investimentos (user_id, ativo, quantidade, preco, data) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (user_id, ativo, quantidade, preco, data))
    conexao.commit()
    cursor.close()
    conexao.close()


def obter_investimentos_usuario(user_id):
    conexao = conectar_bd()
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT ativo, quantidade, preco, data FROM carteira_investimentos WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    investimentos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return investimentos





