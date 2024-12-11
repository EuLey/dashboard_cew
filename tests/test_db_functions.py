import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db_functions import criar_carteira, adicionar_investimento, obter_investimentos_carteira

# Mock do banco de dados para testes
@pytest.fixture
def mock_db(monkeypatch):
    # Substitui a função de conexão com o banco por um mock
    def fake_criar_conexao():
        class FakeCursor:
            def __init__(self):
                self.lastrowid = 1  # Simula o ID retornado após o insert

            def execute(self, query, params=None):
                print(f"Query executada: {query}, Params: {params}")

            def fetchall(self):
                # Retorna dados simulados para os testes
                return [{"id": 1, "nome": "Carteira Teste", "ativo": "PETR4", "quantidade": 10, "preco": 30.50}]

            def fetchone(self):
                # Retorna um único registro simulado
                return {"id": 1, "nome": "Carteira Teste"}

            def close(self):
                pass

        class FakeConnection:
            def cursor(self, dictionary=False):
                return FakeCursor()

            def commit(self):
                pass

            def close(self):
                pass

        return FakeConnection()

    monkeypatch.setattr("db_functions.criar_conexao", fake_criar_conexao)

# Testa a criação de uma carteira
def test_criar_carteira(mock_db):
    user_id = 1
    nome = "Carteira Teste"
    carteira_id = criar_carteira(user_id, nome)
    assert carteira_id == 1  # Simula que o ID retornado é 1

# Testa a adição de um investimento
def test_adicionar_investimento(mock_db):
    user_id = 1
    carteira_id = 1
    ativo = "PETR4"
    quantidade = 10
    preco = 30.50
    adicionar_investimento(user_id, carteira_id, ativo, quantidade, preco)

# Testa a recuperação de investimentos
def test_obter_investimentos_carteira(mock_db):
    user_id = 1
    carteira_id = 1
    investimentos = obter_investimentos_carteira(user_id, carteira_id)
    assert len(investimentos) > 0
    assert investimentos[0]["ativo"] == "PETR4"
    assert investimentos[0]["quantidade"] == 10
    assert investimentos[0]["preco"] == 30.50
