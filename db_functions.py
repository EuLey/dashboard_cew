# db_functions.py
import mysql.connector

def conectar_bd():
    # Função para conectar ao banco de dados MySQL
    return mysql.connector.connect(host="localhost", user="root", database="cadastro_dash")

def adicionar_investimento(user_id, ativo, quantidade, preco):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    sql = "INSERT INTO carteira_investimentos (user_id, ativo, quantidade, preco) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (user_id, ativo, quantidade, preco))
    conexao.commit()
    cursor.close()
    conexao.close()

def obter_investimentos_usuario(user_id):
    conexao = conectar_bd()
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT ativo, quantidade, preco FROM carteira_investimentos WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    investimentos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return investimentos
