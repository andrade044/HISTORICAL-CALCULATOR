from pathlib import Path
import sys
import os

import sqlite3 

# Função que retorna um caminho persistente para o banco (AppData ou Home)
def get_caminho_banco():
    if sys.platform == "win32":
        base = os.getenv("APPDATA")
        if base is None:
            raise EnvironmentError("APPDATA não encontrada")
    else:
        base = os.getenv("HOME") or str(Path.home())
    pasta = os.path.join(base, "MinhaCalculadora")
    os.makedirs(pasta, exist_ok=True)
    return os.path.join(pasta, "historico.sqlite")

# Caminho do banco de dados SQLite
DB_FILE = get_caminho_banco()
TABLE_NAME = 'Memory'

# Cria conexão inicial
connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

# Função para inserir no histórico
def insertToMemory(numberLeft: float , numberRight: float, operator:str, result: float):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Cria a tabela se não existir
    cursor.execute(
        f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numberLeft REAL,
            numberRigth REAL,
            operator TEXT,
            result REAL
        )'''
    )

    # Insere o registro
    cursor.execute(
        f'''INSERT INTO {TABLE_NAME} (numberLeft, numberRigth, operator, result)
            VALUES (?, ?, ?, ?)''',
        (numberLeft, numberRight, operator, result)
    )

    connection.commit()
    cursor.close()
    connection.close()
