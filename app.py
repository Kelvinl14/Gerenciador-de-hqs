import streamlit as st
from db_hqs import database
from datetime import date


# Cria a tabela de HQs se não existir
database.criar_tabela()

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

# Configurações da página
st.set_page_config(page_title="Gerenciador de HQ", layout="wide")
st.title("Gerenciador de HQ")
st.subheader("Bem-vindo ao Gerenciador de HQ!")

# Abas de Navegação
tab1, tab2, tab3 = st.tabs(["Adicionar HQ", "Atualizar HQ", "Excluir HQ"])
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
                salvar_hq(titulo, autor, ano, editora)
                st.info("Formulário enviado com sucesso!", icon="ℹ️")
            else:
                st.warning("Preencha pelo menos o título e o autor.", icon="⚠️")

with tab2:
    st.header("Atualizar as HQs")

    hqs_data = load_hqs()
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

    hqs_data = load_hqs()
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


# Seção de listagem
st.subheader("📖 Lista de HQs")
if st.button("🔄 Recarregar HQs"):
    hqs_data = load_hqs()
    if hqs_data:
        st.table(hqs_data)
else:
    hqs_data = load_hqs()
    if hqs_data:
        st.table(hqs_data)