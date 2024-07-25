from app import conectar_banco


def criar_tabela():
    conn = conectar_banco()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mes TEXT NOT NULL,
                    valor REAL NOT NULL,
                    descricao TEXT)''')
    conn.commit()
    conn.close()
