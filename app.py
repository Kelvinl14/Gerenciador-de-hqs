import streamlit as st
from db_hqs import database
from datetime import date


# Cria a tabela de HQs se não existir
database.criar_tabelas()
database.criar_admin_inicial()

# Configurações da página
st.set_page_config(page_title="Gerenciador de HQ", layout="wide")

# Sessão
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Tela LOGIN / CADASTRO
def login_screen():
    st.title("Gerenciador de HQ - Login")


    st.subheader("Já possui uma conta? Faça login!")
    username = st.text_input("Usuário", key="login_user")
    password = st.text_input("Senha", type="password", key="login_pwd")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Entrar"):
            user = database.validar_usuario(username.strip(), password)
            if user:
                st.session_state.logado = True
                st.session_state.user = user["username"]
                st.session_state.is_admin = user["is_admin"]
                database.inserir_log(user["username"], "login")
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    with col2:
        if st.button("Cadastrar"):
            st.session_state.show_registration = True
            st.rerun()

# Inicializar session states para os campos
if "new_username" not in st.session_state:
    st.session_state.new_username = ""
if "new_password" not in st.session_state:
    st.session_state.new_password = ""
def registration_screen():
    st.title("Cadastro")
    new_username = st.text_input("Escolha um usuário", value=st.session_state.new_username, key="new_user_input")
    new_password = st.text_input("Escolha uma senha", type="password", value=st.session_state.new_password, key="new_pass_input")

    bnt1, bnt2 = st.columns([0.3, 1.7])

    with bnt1:
        if st.button("Cadastrar"):
            validar_user = database.validar_username(new_username)

            if not validar_user:
                database.criar_usuario(new_username.strip(), new_password.strip())
                st.toast("Usuário cadastrado com sucesso!", icon="✅", duration=3)

                # LIMPAR CAMPOS
                st.session_state.new_username = ""
                st.session_state.new_password = ""

                st.session_state.show_registration = False
            else:
                st.toast("Erro ao cadastrar. O usuário já existe.", icon="❌", duration=3)

    with bnt2:
        if st.button("Voltar ao Login"):
            st.session_state.show_registration = False
            st.rerun()

if not st.session_state.logado:
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False

    if st.session_state.show_registration:
        registration_screen()
    else:
        login_screen()
    st.stop()

# if not st.session_state.logado:
#     login_screen()
#     st.stop()

with st.sidebar:
    st.write(f"Logado como: **{st.session_state.user}**")
    if st.session_state.is_admin:
        st.write("**(Administrador)**")
        st.success("Você tem privilégios de administrador.", icon="🛡️")
    if st.button("Logout"):
        database.inserir_log(st.session_state.user or "desconhecido", "logout")
        st.session_state.logado = False
        st.session_state.user = None
        st.session_state.is_admin = False
        st.rerun()



# Função para salvar HQ
def salvar_hq(titulo, data, author, editora):
    database.inserir_hq(titulo, data, author, editora)
    st.success(f'HQ "{titulo}" salva com sucesso!', icon="✅")

#Lista de HQs
def load_hqs():
    try:
        data = database.listar_hqs()
        if not data:
            st.info("Nenhuma HQ encontrada no banco de dados.", icon="ℹ️")
            return []

        hqs_data = [
            {
                "id": hq[0],
                "titulo": hq[1],
                "autor": hq[2],
                "ano": hq[3],
                "editora": hq[4]
            }
                for hq in data
        ]
        return hqs_data
    except Exception as e:
        st.error(f"Erro ao carregar HQs: {e}")
        return []

# Título e Subtítulo
st.title("Gerenciador de HQ")
st.subheader(f"Bem-vindo, {st.session_state.user} ao Gerenciador de HQ!")

# Abas de Navegação
tab1, tab2, tab3, tab4 = st.tabs(["Adicionar HQ", "Atualizar HQ", "Excluir HQ", "Coleções"])
with tab1:
    st.header("Adicionar Nova HQ")

    # Formulário
    with st.form("form_hq"):
        st.write("Digite suas HQs")

        #inputs
        titulo = st.text_input("Titulo", placeholder="Digite sua hq")
        autor = st.text_input("Autor", placeholder="Digite o autor da hq")
        ano = st.date_input("Ano de Lançamento", max_value=date.today(), min_value=date(1900, 1, 1))
        editora = st.text_input("Editora", placeholder="Digite a editora da hq")

        submitted = st.form_submit_button("Enviar HQ")
        if submitted:
            if titulo and autor:
                # salvar_hq(titulo, autor, ano, editora)
                database.inserir_hq(titulo.strip(), autor.strip(), ano, editora.strip())
                database.inserir_log(st.session_state.user or "desconhecido", f'Adicionou a HQ "{titulo.strip()}"')
                st.info("Formulário enviado com sucesso!", icon="ℹ️")
            else:
                st.warning("Preencha pelo menos o título e o autor.", icon="⚠️")

with tab2:
    st.header("Atualizar as HQs")

    hqs_data = database.listar_hqs()
    if not hqs_data:
        st.info("Nenhuma HQ disponível para atualização.", icon="ℹ️")
    else:
        opcoes = {f'{hq["id"]} - {hq["titulo"]}': hq for hq in hqs_data}
        escolha = st.selectbox("Selecione a HQ para atualizar:", list(opcoes.keys()))

        hq_selecionada = opcoes[escolha]

        with st.form("form_editar_hq"):
            novo_titulo = st.text_input("Titulo", value=hq_selecionada["titulo"])
            novo_autor = st.text_input("Autor", value=hq_selecionada["autor"])
            novo_ano = st.date_input("Ano de Lançamento", value=date.fromisoformat(hq_selecionada["ano"]))
            nova_editora = st.text_input("Editora", value=hq_selecionada["editora"])

            atualizar_submitted = st.form_submit_button("Atualizar HQ")
            if atualizar_submitted:
                database.atualizar_hq(hq_selecionada["id"], novo_titulo, novo_autor, novo_ano, nova_editora)
                st.success(f'HQ "{novo_titulo}" atualizada com sucesso!', icon="✅")

with tab3:
    st.subheader("Excluir HQ")

    hqs_data = database.listar_hqs()
    if not hqs_data:
        st.info("Nenhuma HQ disponível para exclusão.")
    else:
        opcoes = {f'{hq["id"]} - {hq["titulo"]}': hq for hq in hqs_data}
        escolha = st.selectbox("Selecione a HQ para excluir:", list(opcoes.keys()))
        hq_sel = opcoes[escolha]

        st.warning(f"Tem certeza que deseja excluir **{hq_sel['titulo']}**?", icon="⚠️")

        if st.button("Excluir HQ", type="primary"):
            database.excluir_hq(hq_sel["id"])
            st.success(f'HQ **"{hq_sel["titulo"]}"** foi excluída com sucesso!', icon="🗑️")
            st.rerun()  # Atualiza a página automaticamente

with tab4:
    st.subheader("Minhas Coleções")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Criar Nova Coleção")
        with st.form("form_colecao"):
            nome_colecao = st.text_input("Nome da Coleção", placeholder="Digite o nome da coleção")
            descricao_colecao = st.text_area("Descrição", placeholder="Descreva a coleção")

            criar_submitted = st.form_submit_button("Criar Coleção")
            if criar_submitted:
                user = None

                users = database.listar_usuarios()
                usuario_obj = next((u for u in users if u["username"] == st.session_state.user), None)

                if usuario_obj:
                    user = usuario_obj["id"]

                if nome_colecao:
                    database.criar_colecao(nome_colecao.strip(), descricao_colecao.strip(), user)
                    database.inserir_log(st.session_state.user or "desconhecido", f'Criou a coleção "{nome_colecao.strip()}"')
                    st.success(f'Coleção "{nome_colecao}" criada com sucesso!', icon="✅")
                else:
                    st.warning("O nome da coleção é obrigatório.", icon="⚠️")
    with col2:
        st.subheader("Gerenciar coleções")
        colecoes = database.listar_colecoes()
        if not colecoes:
            st.info("Nenhuma coleção.")
        else:
            escolha = st.selectbox("Selecione coleção", [f'{c["id"]} - {c["nome"]}' for c in colecoes])
            col_id = int(escolha.split(" - ")[0])
            colecao = next((c for c in colecoes if c["id"] == col_id), None)
            if colecao:
                st.write("Coleção:", colecao["nome"])
                st.write("Descrição:", colecao["descricao"])
                st.markdown("**HQs da coleção**")
                hqs_colecao = database.listar_hqs_da_colecao(colecao["id"])
                if hqs_colecao:
                    st.table(hqs_colecao)
                else:
                    st.info("Sem HQs nessa coleção.")
                st.markdown("Adicionar HQ na coleção")
                hqs_all = database.listar_hqs()
                if hqs_all:
                    escolha_hq = st.selectbox("HQ", [f'{h["id"]} - {h["titulo"]}' for h in hqs_all],
                                              key=f"hc_{colecao['id']}")
                    if st.button("Adicionar HQ à coleção"):
                        hq_id = int(escolha_hq.split(" - ")[0])
                        database.adicionar_hq_colecao(hq_id, colecao["id"])
                        database.inserir_log(st.session_state.user or "desconhecido", f"adicionou_hq_{hq_id}_na_colecao_{colecao['id']}")
                        st.success("HQ adicionada à coleção!")
                        st.rerun()
                else:
                    st.info("Cadastre HQs primeiro.")

# Seção de listagem
st.subheader("📖 Lista de HQs")
if st.button("🔄 Recarregar HQs"):
    hqs_data = database.listar_hqs()
    if hqs_data:
        st.table(hqs_data)
else:
    hqs_data = database.listar_hqs()
    if hqs_data:
        st.table(hqs_data)