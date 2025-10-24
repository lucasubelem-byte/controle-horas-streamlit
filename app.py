import streamlit as st
from datetime import datetime
import json
import os
import plotly.express as px

# ===== Configurações da página =====
st.set_page_config(
    page_title="Controle de Horas",
    layout="wide",
    page_icon="⏱",
)

# ===== Estilo escuro personalizado =====
st.markdown("""
    <style>
    body { background-color: #0E1117; color: #FAFAFA; }
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    h1, h2, h3, h4, h5, h6, label, p, div { color: #FAFAFA !important; }
    .stRadio > div{flex-direction:row !important;}
    .css-1v0mbdj, .st-emotion-cache-1v0mbdj {background-color: #262730 !important;}
    </style>
""", unsafe_allow_html=True)

# ===== Senha mestra =====
senha_mestra = "1b1m"

# ===== Arquivo JSON =====
ARQUIVO_DADOS = "dados.json"

# Carregar dados
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

def salvar_dados():
    with open(ARQUIVO_DADOS, "w") as f:
        json.dump(usuarios, f, indent=4)

# ===== Funções =====
def remover_horas_admin():
    st.subheader("➖ Remover horas")
    senha = st.text_input("Senha mestra:", type="password", key="senha_rem_admin")
    if senha == senha_mestra:
        nome = st.selectbox("Escolha o usuário:", list(usuarios.keys()))
        if usuarios[nome]["horas"]:
            qtd = st.number_input(
                "Quantas horas deseja remover?",
                min_value=1,
                max_value=sum(usuarios[nome]["horas"]),
                key=f"qtd_rem_admin_{nome}"
            )
            if st.button("Remover horas", key=f"btn_rem_admin_{nome}"):
                total_horas = sum(usuarios[nome]["horas"])
                if qtd <= total_horas:
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
                    st.error("Não há horas suficientes para remover.")
        else:
            st.warning("Esse usuário não possui horas a remover.")
    elif senha:
        st.error("Senha mestra incorreta!")

def ver_horas():
    st.subheader("📊 Horas devidas por usuário")

    nomes = []
    horas_totais = []
    for nome, dados in usuarios.items():
        total = sum(dados["horas"])
        nomes.append(nome)
        horas_totais.append(total)

    # ===== Gráfico Interativo (barras mais finas) =====
    fig = px.bar(
        x=nomes,
        y=horas_totais,
        text=horas_totais,
        color=horas_totais,
        color_continuous_scale="reds",
        title="Horas Totais Devidas por Usuário",
        labels={"x": "Usuário", "y": "Total de Horas"},
    )

    fig.update_traces(
        textposition="outside",
        width=0.3  # 🔹 Barras mais finas
    )

    fig.update_layout(
        xaxis_tickangle=-30,
        template="plotly_dark",
        height=500,
        title_font_size=22,
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===== Lista detalhada =====
    st.markdown("---")
    for nome, dados in usuarios.items():
        with st.expander(f"👤 {nome} — {sum(dados['horas'])} horas"):
            if dados["faltas"]:
                for dia, h in zip(dados["faltas"], dados["horas"]):
                    st.write(f"📅 {dia}: {h} horas")
            else:
                st.write("Nenhuma falta registrada.")

def admin_panel():
    st.subheader("🛠️ Painel Admin")
    senha = st.text_input("Senha mestra:", type="password", key="senha_admin")
    if senha == senha_mestra:
        opcao = st.selectbox(
            "Selecione a operação:",
            ["➕ Adicionar horas", "➖ Remover horas", "👤 Adicionar usuário", "🗑️ Remover usuário"],
        )

        if opcao == "➕ Adicionar horas":
            nome = st.selectbox("Escolha o usuário:", list(usuarios.keys()))
            dia = st.date_input("Escolha o dia", key=f"add_admin_{nome}")
            dia_str = dia.strftime("%d/%m/%Y")
            if st.button("Adicionar", key=f"btn_add_admin_{nome}"):
                if dia_str not in usuarios[nome]["faltas"]:
                    valor = 5 if dia.weekday() < 5 else 4
                    usuarios[nome]["horas"].append(valor)
                    usuarios[nome]["faltas"].append(dia_str)
                    salvar_dados()
                    st.success(f"{valor} horas adicionadas para {nome} em {dia_str}")
                else:
                    st.warning("Essa data já foi registrada.")

        elif opcao == "➖ Remover horas":
            remover_horas_admin()

        elif opcao == "👤 Adicionar usuário":
            nome_novo = st.text_input("Nome do novo usuário")
            senha_inicial = st.text_input("Senha inicial")
            if st.button("Adicionar"):
                if nome_novo not in usuarios:
                    usuarios[nome_novo] = {"senha": senha_inicial, "horas": [], "faltas": []}
                    salvar_dados()
                    st.success(f"Usuário {nome_novo} adicionado!")
                else:
                    st.error("Usuário já existe.")

        elif opcao == "🗑️ Remover usuário":
            nome_remover = st.selectbox("Escolha o usuário para remover:", list(usuarios.keys()))
            if st.button("Remover"):
                usuarios.pop(nome_remover)
                salvar_dados()
                st.success(f"Usuário {nome_remover} removido!")

    elif senha:
        st.error("Senha mestra incorreta!")

# ===== Interface Principal =====
st.title("⏱️ Controle de Horas Devidas")

acao = st.radio(
    "Escolha uma ação:",
    ["📊 Ver horas", "🛠️ Admin"],
    horizontal=True
)

if acao == "📊 Ver horas":
    ver_horas()
else:
    admin_panel()
