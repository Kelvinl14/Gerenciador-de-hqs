import sqlite3
from datetime import datetime
import bcrypt

DB_FILE = 'hqs.db'

def criar_conexao():
    conexao = sqlite3.connect(DB_FILE)
    return conexao

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def criar_tabelas():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    # Tabela de usuários (autenticação)
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0
            );
        """
    )

    # Tabela de HQs
    cursor.execute(
        """ 
            CREATE TABLE IF NOT EXISTS hqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                ano INTEGER,
                editora TEXT
            );
        """
    )

    # Tabela de coleções
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS colecoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES users (id)
            );
        """
    )

    # Tabela de associação HQ-Coleção
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS hq_colecao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hq_id INTEGER,
                colecao_id INTEGER,
                FOREIGN KEY (hq_id) REFERENCES hqs (id),
                FOREIGN KEY (colecao_id) REFERENCES colecoes (id)
            );
        """
    )

    # Tabela de empréstimos
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hq_id INTEGER NOT NULL,
                pessoa TEXT NOT NULL,
                data_emprestimo TEXT NOT NULL,
                data_devolucao TEXT,
                FOREIGN KEY(hq_id) REFERENCES hqs(id)
            );
        """)

    # Tabela de logs
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT,
                acao TEXT,
                data TEXT
            );
        """)

    conexao.commit()
    conexao.close()

def inserir_hq(titulo: str, autor: str, ano: str = None, editora: str = None):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
            INSERT INTO hqs (titulo, autor, ano, editora)
            VALUES (?, ?, ?, ?);
        """,
        (titulo, autor, ano, editora)
    )
    conexao.commit()
    conexao.close()

def atualizar_hq(id: int, titulo: str, autor: str, ano: str, editora: str):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
            UPDATE hqs
            SET titulo = ?, autor = ?, ano = ?, editora = ?
            WHERE id = ?;
        """,
        (titulo, autor, ano, editora, id)
    )
    conexao.commit()
    conexao.close()

def excluir_hq(id: int):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
            DELETE FROM hqs
            WHERE id = ?;
        """,
        (id,)
    )
    conexao.commit()
    conexao.close()

def listar_hqs():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT id, titulo, autor, ano, editora FROM hqs ORDER BY id;
        """
    )
    hqs = cursor.fetchall()
    conexao.close()
    return [
        {
            "id": hq[0],
            "titulo": hq[1],
            "autor": hq[2],
            "ano": hq[3],
            "editora": hq[4]
        } for hq in hqs
    ]

def criar_usuario(username: str, password: str, is_admin: bool = False) -> bool:
    conexao = criar_conexao()
    cursor = conexao.cursor()

    try:
        hashed_password = hash_password(password)
        cursor.execute(
            """
                INSERT INTO users (username, password, is_admin)
                VALUES (?, ?, ?);
            """,
            (username, hashed_password, 1 if is_admin else 0)
        )
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conexao.close()

def validar_username(username: str) -> bool:
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT id FROM users
            WHERE username = ?;
        """,
        (username,)
    )
    usuario = cursor.fetchone()
    conexao.close()
    return usuario is not None

def validar_usuario(username, password):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT id, username, password, is_admin FROM users
            WHERE username = ?;
        """,
        (username,)
    )
    usuario = cursor.fetchone()
    conexao.close()
    if usuario and check_password(password, usuario[2]):
        return {
            "id": usuario[0],
            "username": usuario[1],
            "is_admin": bool(usuario[3])
        }
    return None

def listar_usuarios():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT id, username, is_admin FROM users;
        """
    )
    usuarios = cursor.fetchall()
    conexao.close()
    return [
        {
            "id": usuario[0],
            "username": usuario[1],
            "is_admin": bool(usuario[2])
        }
        for usuario in usuarios
    ]

def excluir_usuario(id: int) -> None:
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
            DELETE FROM users
            WHERE id = ?;
        """,
        (id,)
    )
    conexao.commit()
    conexao.close()

def criar_admin_inicial():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT * FROM users
            WHERE is_admin = 1;
        """
    )
    admin_existente = cursor.fetchone()
    if not admin_existente:
        criar_usuario("admin", "admin123", is_admin=True)
    conexao.close()


def inserir_log(usuario: str, acao: str):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    data = datetime.utcnow().isoformat()
    cursor.execute(
        """
            INSERT INTO logs (usuario, acao, data)
            VALUES (?, ?, ?);
        """,
        (usuario, acao, data)
    )
    conexao.commit()
    conexao.close()

def listar_logs(limit: int = 100):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT id, usuario, acao, data FROM logs ORDER BY data DESC LIMIT ?;
        """,
        (limit,)
    )
    logs = cursor.fetchall()
    conexao.close()
    return [
        {
            "id": log[0],
            "usuario": log[1],
            "acao": log[2],
            "data": log[3]
        }
        for log in logs
    ]

def criar_colecao(nome: str, descricao: str, usuario_id: int = None):
    con = criar_conexao()
    cur = con.cursor()
    cur.execute("INSERT INTO colecoes (nome, descricao, usuario_id) VALUES (?, ?, ?)",
                (nome, descricao, usuario_id))
    con.commit()
    con.close()

def listar_colecoes(usuario_id: int = None):
    con = criar_conexao()
    cur = con.cursor()
    if usuario_id:
        cur.execute("SELECT id, nome, descricao, usuario_id FROM colecoes WHERE usuario_id = ?", (usuario_id,))
    else:
        cur.execute("SELECT id, nome, descricao, usuario_id FROM colecoes")
    rows = cur.fetchall()
    con.close()
    return [{"id": r[0], "nome": r[1], "descricao": r[2], "usuario_id": r[3]} for r in rows]

def adicionar_hq_colecao(hq_id: int, colecao_id: int):
    con = criar_conexao()
    cur = con.cursor()
    cur.execute("INSERT INTO hq_colecao (hq_id, colecao_id) VALUES (?, ?)", (hq_id, colecao_id))
    con.commit()
    con.close()

def listar_hqs_da_colecao(colecao_id: int):
    con = criar_conexao()
    cur = con.cursor()
    cur.execute("""
        SELECT h.id, h.titulo, h.autor, h.ano, h.editora
        FROM hqs h
        JOIN hq_colecao hc ON hc.hq_id = h.id
        WHERE hc.colecao_id = ?
    """, (colecao_id,))
    rows = cur.fetchall()
    con.close()
    return [{"id": r[0], "titulo": r[1], "autor": r[2], "ano": r[3], "editora": r[4]} for r in rows]

# ------------------------
# Empréstimos
# ------------------------
def emprestar_hq(hq_id: int, pessoa: str):
    con = criar_conexao()
    cur = con.cursor()
    data = datetime.utcnow().isoformat()
    cur.execute("INSERT INTO emprestimos (hq_id, pessoa, data_emprestimo) VALUES (?, ?, ?)",
                (hq_id, pessoa, data))
    con.commit()
    con.close()

def devolver_hq(emprestimo_id: int):
    con = criar_conexao()
    cur = con.cursor()
    data = datetime.utcnow().isoformat()
    cur.execute("UPDATE emprestimos SET data_devolucao = ? WHERE id = ?", (data, emprestimo_id))
    con.commit()
    con.close()

def listar_emprestimos(ativos_only: bool = False):
    con = criar_conexao()
    cur = con.cursor()
    if ativos_only:
        cur.execute("""
            SELECT e.id, e.hq_id, h.titulo, e.pessoa, e.data_emprestimo, e.data_devolucao
            FROM emprestimos e
            JOIN hqs h ON h.id = e.hq_id
            WHERE e.data_devolucao IS NULL
            ORDER BY e.id DESC
        """)
    else:
        cur.execute("""
            SELECT e.id, e.hq_id, h.titulo, e.pessoa, e.data_emprestimo, e.data_devolucao
            FROM emprestimos e
            JOIN hqs h ON h.id = e.hq_id
            ORDER BY e.id DESC
        """)
    rows = cur.fetchall()
    con.close()
    return [
        {"id": r[0], "hq_id": r[1], "titulo": r[2], "pessoa": r[3], "data_emprestimo": r[4], "data_devolucao": r[5]}
        for r in rows
    ]