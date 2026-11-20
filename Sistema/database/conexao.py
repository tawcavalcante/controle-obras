import sqlite3
from pathlib import Path


CAMINHO_BANCO = Path(__file__).resolve().parent / "obras.db"


def obter_conexao() -> sqlite3.Connection:
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao


def inicializar_banco() -> None:
    with obter_conexao() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS obras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                localizacao_maps TEXT NOT NULL,
                orcamento_previsto REAL NOT NULL,
                status INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS documentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                obra_id INTEGER NOT NULL,
                nome_arquivo TEXT NOT NULL,
                tipo INTEGER NOT NULL,
                FOREIGN KEY (obra_id) REFERENCES obras(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                obra_id INTEGER NOT NULL,
                tipo_mov TEXT NOT NULL,
                valor REAL NOT NULL,
                data_ocorrencia TEXT NOT NULL,
                descricao TEXT NOT NULL,
                origem_recurso TEXT,
                categoria INTEGER,
                id_comprovante INTEGER DEFAULT 0,
                FOREIGN KEY (obra_id) REFERENCES obras(id) ON DELETE CASCADE
            );
            """
        )