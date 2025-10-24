import streamlit as st
import json
import os
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Controle de Horas", layout="wide")

# ===== Senha mestra =====
senha_mestra = "1b1m"

# ===== Arquivo JSON =====
ARQUIVO_DADOS = "dados.json"

# Carregar dados do JSON
if os.path.exists(ARQUIVO_DADOS):
    with open(ARQUIVO_DADOS, "r") as f:
        usuarios = json.load(f)
else:
    usuarios = {
        "Lucas Uva": {"senha": "lu123", "horas": [], "faltas": []},
        "Luis": {"senha": "lu1", "horas": [], "faltas": []},
        "Matheus": {"senha": "ma123", "horas": [], "faltas": []},
        "Raphaela": {"senha": "ra123", "horas": [], "faltas": []},
        "Ralf": {"senha": "ra1", "horas": [], "faltas": []},
        "Julia": {"senha": "ju1", "horas": [], "faltas": []},
        "Withyna": {"senha": "wi1", "horas": [], "faltas": []},
        "Melissa": {"senha": "me1", "horas": [], "faltas": []},
        "Ana": {"senha": "an1", "horas": [], "faltas": []},
        "Leandro": {"senha": "le1", "horas": [], "faltas": []},
    }

# Função para salvar JSON
def salvar_dados():
    with open(ARQUIVO_DADOS, "w") as f:
        json.dump(usuarios, f, indent=4)

# ===== Funções =====
def ver_horas():
    st.subheader("📊 Horas devidas por usuário")
    dados_grafico = {nome: sum(info["horas"]) for nome, info in usuarios.items()}

    if any(dados_grafico.values()):
        fig = px.bar(
            x=list(dados_grafico.keys()),
            y=list(dados_grafico.values()),
            text=list(dados_grafico.values()),
            color=list(dados_grafico.values()),
            color_continuous_scale="bluered",
            title="Horas Devidas (Interativo)",
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            xaxis_title="Usuário",
            yaxis_title="Horas",
            plot_bgcolor="#f8f9fa",
            paper_bgcolor="#f8f9fa",
            font=dict(size=14),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum usuário possui horas registradas.")

    # Exibir detalhes individuais
    st.markdown("### 🗓 Detalhes por pessoa")
    for nome, dados in usuarios.items():
        total = sum(dados["horas"])
        with st.expander(f"{nome} - **{total} horas**"):
            if dados["faltas"]:
                for dia, h in zip(dados["faltas"], dados["horas"]):
                    st.write(f"📅 {dia} → {h} horas")
            else:
                st.write("Nenhuma falta registrada.")

def admin_panel():
    st.subheader("🔒 Painel do Administrador")
    senha = st.text_input("Senha mestra:", type="password", key="senha_admin")
    if senha == senha_mestra:
        op = st.selectbox(
            "Escolha uma operação:",
            ["Adicionar horas", "Remover horas", "Adicionar usuário", "Remover usuário", "Alterar senha"],
        )

        # ========== Adicionar horas ==========
        if op == "Adicionar horas":
            nome = st.selectbox("Escolha o usuário:", list(usuarios.keys()))
            dia = st.date_input("Escolha o dia da falta", key=f"data_add_{nome}")
            horas = st.number_input("Quantas horas deseja adicionar?", min_value=1, step=1)
            if st.button("Adicionar horas"):
                dia_str = dia.strftime("%d/%m/%Y")
                if dia_str not in usuarios[nome]["faltas"]:
                    usuarios[nome]["horas"].append(horas)
                    usuarios[nome]["faltas"].append(dia_str)
                    salvar_dados()
                    st.success(f"{horas} horas adicionadas para {nome} em {dia_str}")
                else:
                    st.warning("Essa data já foi registrada.")

        # ========== Remover horas ==========
        elif op == "Remover horas":
            nome = st.selectbox("Escolha o usuário:", list(usuarios.keys()))
            total_horas = sum(usuarios[nome]["horas"])
            if total_horas > 0:
                qtd = st.number_input(
                    "Quantas horas deseja remover?",
                    min_value=1,
                    max_value=total_horas,
                    step=1,
                    key=f"remover_{nome}",
                )
                if st.button("Remover horas"):
                    horas_restantes = qtd
                    while horas_restantes > 0 and usuarios[nome]["horas"]:
                        if usuarios[nome]["horas"][-1] <= horas_restantes:
                            horas_restantes -= usuarios[nome]["horas"][-1]
                            usuarios[nome]["horas"].pop()
                            usuarios[nome]["faltas"].pop()
                        else:
                            usuarios[nome]["horas"][-1] -= horas_restantes
                            horas_restantes = 0
                    salvar_dados()
                    st.success(f"{qtd} horas removidas de {nome}")
            else:
                st.warning("Esse usuário não possui horas a remover.")

        # ========== Adicionar usuário ==========
        elif op == "Adicionar usuário":
            nome_novo = st.text_input("Nome do novo usuário")
            senha_inicial = st.text_input("Senha inicial")
            if st.button("Adicionar"):
                if nome_novo not in usuarios:
                    usuarios[nome_novo] = {"senha": senha_inicial, "horas": [], "faltas": []}
                    salvar_dados()
                    st.success(f"Usuário {nome_novo} adicionado!")
                else:
                    st.error("Usuário já existe.")

        # ========== Remover usuário ==========
        elif op == "Remover usuário":
            nome_remover = st.selectbox("Escolha o usuário para remover:", list(usuarios.keys()))
            if st.button("Remover"):
                usuarios.pop(nome_remover)
                salvar_dados()
                st.success(f"Usuário {nome_remover} removido!")

        # ========== Alterar senha ==========
        elif op == "Alterar senha":
            nome_alt = st.selectbox("Escolha o usuário:", list(usuarios.keys()))
            nova_senha = st.text_input("Nova senha")
            if st.button("Alterar senha"):
                usuarios[nome_alt]["senha"] = nova_senha
                salvar_dados()
                st.success(f"Senha de {nome_alt} alterada!")
    elif senha:
        st.error("Senha mestra incorreta!")

# ===== Interface Principal =====
st.title("⏱ Controle de Horas Devidas")

aba = st.sidebar.radio("Navegação", ["Ver horas", "Admin"])

if aba == "Ver horas":
    ver_horas()
else:
    admin_panel()
