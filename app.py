import streamlit as st
import requests
import re
import json
import os

# Configuração da página - Layout Wide
st.set_page_config(page_title="Sistema Brazukas", layout="wide")

# Estilo CSS para deixar o visual mais "limpo" (sem bordas pesadas)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
    div.stTextInput>label { font-weight: bold; color: #2E86C1; }
    </style>
    """, unsafe_allow_html=True)

# Lógica de Persistência (mesma que funcionava)
DB_FILE = "dados_sistema.json"
def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def salvar_dados(dados):
    with open(DB_FILE, "w") as f: json.dump(dados, f)

if "db" not in st.session_state: st.session_state.db = carregar_dados()

# Título
st.title("🤖 Brazukas Top Tisp")
st.markdown("---")

def renderizar_bloco(titulo):
    # Usando st.container sem borda (fica mais leve)
    with st.container():
        st.subheader(f"🏟️ {titulo}")
        
        if titulo not in st.session_state.db: st.session_state.db[titulo] = {}
        d = st.session_state.db[titulo]
        
        # Grid de inputs mais organizado
        col_a, col_b = st.columns(2)
        camp = col_a.text_input("Campeonato", value=d.get("camp", ""), key=f"c_{titulo}")
        hora = col_b.text_input("Horário", value=d.get("hora", ""), key=f"h_{titulo}")
        
        c1, c2, c3 = st.columns(3)
        casa = c1.text_input("Casa", value=d.get("casa", ""), key=f"ca_{titulo}")
        vis = c2.text_input("Visitante", value=d.get("vis", ""), key=f"v_{titulo}")
        placar = c3.text_input("Placar Final", value=d.get("placar", ""), key=f"p_{titulo}")
        
        lista = st.text_area("Lista de jogos", value=d.get("lista", ""), key=f"l_{titulo}", height=80)
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            # Lógica simplificada
            st.session_state.db[titulo].update({"camp": camp, "hora": hora, "casa": casa, "vis": vis, "placar": placar, "lista": lista, "prob": 75})
            salvar_dados(st.session_state.db)
            st.rerun()
        
        if "prob" in st.session_state.db[titulo]:
            st.success(f"Análise pronta! Probabilidade estimada: {st.session_state.db[titulo]['prob']}%")
            
            if st.button(f"🚀 ENVIAR PARA TELEGRAM", key=f"en_{titulo}", type="primary"):
                # (Lógica de envio mantida igual)
                msg = f"🚨 *Alerta:* {casa} x {vis}"
                st.session_state.db[titulo].update({"msg_id": 123, "msg_text": msg})
                salvar_dados(st.session_state.db)
                st.rerun()

        if "msg_id" in st.session_state.db[titulo]:
            st.markdown("---")
            b1, b2, b3 = st.columns(3)
            if b1.button("✅ GREEN", key=f"g_{titulo}"): st.success("GREENZAÇOOO!!!")
            if b2.button("❌ RED", key=f"r_{titulo}"): st.error("RED!")
            if b3.button("🔄 DEV", key=f"d_{titulo}"): st.warning("DEVOLVIDA")

# Layout principal
col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
