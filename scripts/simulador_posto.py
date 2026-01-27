import sqlite3
import os
from datetime import datetime, timedelta
import random

# Caminho onde o banco será criado (dentro da pasta data do projeto)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'abastece.db')

def inicializar_banco():
    # Garante que a pasta data existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Criação da tabela de exemplo (baseada no sistema real)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            pista INTEGER,
            veiculo_tag TEXT,
            valor REAL,
            status TEXT
        )
    ''')

    # Limpa dados antigos para o teste
    cursor.execute('DELETE FROM transacoes')

    # Gera 10 transações aleatórias para hoje
    status_opcoes = ['CONCLUIDO', 'EM_ABERTO', 'FALHA']
    agora = datetime.now()

    for i in range(10):
        data_transacao = agora - timedelta(minutes=random.randint(1, 120))
        pista = random.randint(1, 4)
        tag = f"TAG-{random.randint(1000, 9999)}"
        valor = round(random.uniform(50.0, 350.0), 2)
        status = random.choice(status_opcoes)

        cursor.execute('''
            INSERT INTO transacoes (timestamp, pista, veiculo_tag, valor, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (data_transacao, pista, tag, valor, status))

    conn.commit()
    conn.close()
    print(f"✅ Banco de dados simulado criado em: {DB_PATH}")
    print(f"📊 10 transações inseridas com sucesso.")

if __name__ == "__main__":
    inicializar_banco()