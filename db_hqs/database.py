import  sqlite3

def criar_conexao():
    conexao = sqlite3.connect('hqs.db')
    return conexao

def criar_tabela():
    conexao = criar_conexao()
    cursor = conexao.cursor()
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
    conexao.commit()
    conexao.close()

def inserir_hq(titulo, autor, ano, editora):
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
    print("HQ inserida com sucesso!")

def atualizar_hq(id, titulo, autor, ano, editora):
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

def excluir_hq(id):
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
            SELECT * FROM hqs;
        """
    )
    hqs = cursor.fetchall()
    conexao.close()
    return hqs