import streamlit as st

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Controle de Horas", page_icon="⏰", layout="centered")

# --- DADOS INICIAIS ---
if "horas_devidas" not in st.session_state:
    st.session_state.horas_devidas = {
        "Lucas Uva": 0,
        "Luis": 0,
        "Matheus": 0,
        "Raphaela": 0,
        "Ralf": 0,
        "Julia": 0,
        "Withyna": 0,
        "Melissa": 0,
        "Ana": 0,
        "Leandro": 0
        "meusovo" : 0
    }

dias_semana = {
    "segunda": 5,
    "terça": 5,
    "quarta": 5,
    "quinta": 5,
    "sexta": 5,
    "sábado": 4
}

SENHA_REMOVER = "senha123"  # 🔒 Altere aqui se quiser outra senha


# --- FUNÇÕES ---
def adicionar_horas(nome, dia):
    st.session_state.horas_devidas[nome] += dias_semana[dia]

def remover_horas(nome, horas):
    st.session_state.horas_devidas[nome] = max(0, st.session_state.horas_devidas[nome] - horas)


# --- INTERFACE ---
st.title("⏰ Sistema de Controle de Horas Devidas")
st.write("Escolha uma das opções abaixo:")

menu = st.radio("Menu", ["Adicionar horas", "Ver total de horas", "Remover horas"])

# --- ADICIONAR HORAS ---
if menu == "Adicionar horas":
    st.subheader("➕ Adicionar horas")
    nome = st.selectbox("Escolha o nome:", list(st.session_state.horas_devidas.keys()))
    dia = st.selectbox("Escolha o dia da semana:", list(dias_semana.keys()))
    if st.button("Adicionar"):
        adicionar_horas(nome, dia)
        st.success(f"{nome} teve adicionadas {dias_semana[dia]}h ({dia}). Total: {st.session_state.horas_devidas[nome]}h.")

# --- VER TOTAL ---
elif menu == "Ver total de horas":
    st.subheader("📊 Total de horas devidas")
    for nome, total in st.session_state.horas_devidas.items():
        st.write(f"**{nome}:** {total} horas")

# --- REMOVER HORAS ---
elif menu == "Remover horas":
    st.subheader("🔐 Remover horas (acesso restrito)")
    senha = st.text_input("Digite a senha:", type="password")

    if senha == SENHA_REMOVER:
        nome = st.selectbox("Escolha o nome:", list(st.session_state.horas_devidas.keys()))
        horas = st.number_input("Quantas horas deseja remover?", min_value=1, step=1)
        if st.button("Remover horas"):
            remover_horas(nome, horas)
            st.success(f"Removidas {horas}h de {nome}. Total atual: {st.session_state.horas_devidas[nome]}h.")
    elif senha:
        st.error("Senha incorreta! Tente novamente.")
