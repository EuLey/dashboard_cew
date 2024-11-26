import mysql.connector

def criar_conexao():
    return mysql.connector.connect(
        host="localhost",  # Pode ser diferente dependendo do seu servidor
        user="root",       # Seu usuário do MySQL
        database="cadastro_dash"  # Nome do banco de dados que você criou
    )

def adicionar_investimento(user_id, carteira_id, ativo, quantidade, preco):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    query = """
        INSERT INTO carteira_investimentos (user_id, carteira_id, ativo, quantidade, preco)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, carteira_id, ativo, quantidade, preco))
    conexao.commit()
    cursor.close()
    conexao.close()

def obter_investimentos_carteira(user_id, carteira_id):
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)
    query = """
        SELECT ativo, quantidade, preco
        FROM carteira_investimentos
        WHERE user_id = %s AND carteira_id = %s
    """
    cursor.execute(query, (user_id, carteira_id))
    investimentos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return investimentos

def criar_carteira(user_id, nome):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    query = "INSERT INTO carteiras (user_id, nome) VALUES (%s, %s)"
    cursor.execute(query, (user_id, nome))
    conexao.commit()
    carteira_id = cursor.lastrowid  # Obtém o ID da carteira recém-criada
    cursor.close()
    conexao.close()
    return carteira_id

def obter_carteiras_usuario(user_id):
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)
    query = "SELECT id, nome FROM carteiras WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    carteiras = cursor.fetchall()
    cursor.close()
    conexao.close()
    return carteiras
