# 📚 Gerenciador de HQs

Um pequeno **sistema de gerenciamento de HQs (histórias em quadrinhos)** desenvolvido em **Python**, utilizando **SQLite** como banco de dados local e **Streamlit** para criação de uma interface gráfica simples e interativa.

---

## 🚀 Funcionalidades

✅ Adicionar novas HQs ao banco de dados  
✅ Listar todas as HQs cadastradas  
✅ Atualizar informações de HQs existentes  
✅ Excluir HQs  
✅ Interface intuitiva com abas de navegação no Streamlit  

---

## 🧠 Tecnologias Utilizadas

| Tecnologia | Função |
|-------------|--------|
| **Python 3** | Linguagem principal do projeto |
| **SQLite3** | Banco de dados leve e local |
| **Streamlit** | Criação da interface web interativa |
| **Datetime** | Manipulação de datas de lançamento |

---

## 🗂️ Estrutura do Projeto

```plaintext
Gerenciador_de_HQ/
│
├── db_hqs/
│ ├── init.py
│ └── database.py # Funções para conexão e manipulação do banco SQLite
│
├── app.py # Aplicação principal com a interface Streamlit
├── requirements.txt # Dependências do projeto
└── README.md # Este arquivo
```


---

## 🧩 Estrutura do Banco de Dados

O sistema utiliza um banco **SQLite** com uma tabela chamada `hqs`.

Cada HQ contém:

- id: Identificador único
- titulo: Nome da HQ
- autor: Autor da HQ
- ano: Data de lançamento (ou apenas o ano)
- editora: Nome da editora

---

## 🖥️ Interface Streamlit

A interface possui três abas principais:

---

### 🆕 Adicionar HQ

- Formulário para inserir título, autor, ano e editora.
- Botão para salvar a HQ no banco.

### 🔁 Editar HQ

- Seleção de uma HQ existente.
- Edição dos campos desejados.
- Atualização dos dados no banco.

### 🗑️ Excluir HQ

- Lista de HQs existentes.
- Botão para remover a HQ selecionada.

--- 

## ⚙️ Como Executar o Projeto

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seuusuario/gerenciador-hqs.git
cd gerenciador-hqs
```

### 2️⃣ Criar ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux / macOS
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Executar a aplicação

```bash
streamlit run app.py
```

---
