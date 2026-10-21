import sqlite3
import os
from datetime import datetime, timedelta
import random

# Caminho do banco: prioriza a env var DB_PATH (usada pelo container);
# sem ela, mantém o comportamento original (pasta data/ do projeto)
DB_PATH = os.environ.get(
    "DB_PATH",
    os.path.join(os.path.dirname(__file__), '..', 'data', 'abastece.db')
)

# Semente fixa (#80): sem ela cada banco gerado sai diferente do anterior e
# os números de referência da #67 (10 transações, R$ 803,85 em vendas, 4
# equipamentos, 15 arquivos) não se reproduzem em outra máquina nem em clone
# limpo. O carimbo de tempo continua sendo "agora" de propósito — o que fica
# determinístico é o conjunto de transações e o total.
#
# A semente 154622 foi escolhida por busca: 10 transações com 5 CONCLUIDO
# (somando R$ 803,85), 2 EM_ABERTO e 3 FALHA. O card "Vendas Hoje" da tela
# mostra a soma só das CONCLUIDO — por isso o alvo da busca foi essa soma.
SEED = int(os.environ.get("SIMULADOR_SEED", "154622"))

# Quantas transações de dias anteriores o banco simulado guarda (#81).
#
# Sem elas, o recorte por dia do card "Vendas Hoje" é invisível no produto:
# o banco só teria o movimento de hoje, então o card mostraria o mesmo valor
# com ou sem o filtro — e uma regressão futura passaria despercebida. Foi
# exatamente assim que o #81 sobreviveu: com o banco de referência, o bug
# não aparecia.
#
# As transações de hoje continuam exatamente as mesmas (mesma semente, mesma
# ordem de geração): a referência da #67 não muda.
HISTORICO = int(os.environ.get("SIMULADOR_HISTORICO", "6"))

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
    #
    # O carimbo de tempo vai como texto: o adaptador padrão de datetime do
    # sqlite3 foi deprecado na 3.12, e str(datetime) escreve exatamente o
    # mesmo formato ('YYYY-MM-DD HH:MM:SS.ffffff').
    status_opcoes = ['CONCLUIDO', 'EM_ABERTO', 'FALHA']
    agora = datetime.now()

    random.seed(SEED)

    for i in range(10):
        data_transacao = agora - timedelta(minutes=random.randint(1, 120))
        pista = random.randint(1, 4)
        tag = f"TAG-{random.randint(1000, 9999)}"
        valor = round(random.uniform(50.0, 350.0), 2)
        status = random.choice(status_opcoes)

        cursor.execute('''
            INSERT INTO transacoes (timestamp, pista, veiculo_tag, valor, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (str(data_transacao), pista, tag, valor, status))

    # Gera o histórico: transações de 1 a 7 dias atrás (#81)
    #
    # Subtrair no mínimo 1 dia e mais 1 hora garante que nenhuma delas caia
    # no dia de hoje, mesmo que o simulador rode perto da meia-noite.
    for i in range(HISTORICO):
        data_transacao = agora - timedelta(
            days=random.randint(1, 7),
            hours=random.randint(1, 23),
            minutes=random.randint(0, 59),
        )
        pista = random.randint(1, 4)
        tag = f"TAG-{random.randint(1000, 9999)}"
        valor = round(random.uniform(50.0, 350.0), 2)
        status = random.choice(status_opcoes)

        cursor.execute('''
            INSERT INTO transacoes (timestamp, pista, veiculo_tag, valor, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (str(data_transacao), pista, tag, valor, status))

    conn.commit()
    conn.close()
    print(f"✅ Banco de dados simulado criado em: {DB_PATH}")
    print(f"📊 10 transações de hoje + {HISTORICO} de dias anteriores inseridas com sucesso.")

if __name__ == "__main__":
    inicializar_banco()