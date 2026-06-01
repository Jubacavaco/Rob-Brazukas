import streamlit as st
import requests
import re
import json
import os

st.set_page_config(page_title="Sistema Brazukas", layout="wide")

DB_FILE = "dados_brazukas.json"

# Função para garantir leitura/escrita consistente
def carregar_dados():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def salvar_dados(dados):
    with open(DB_FILE, "w") as f:
        json.dump(dados, f)

# Inicializa o estado com dados do ficheiro
if "db" not in st.session_state:
    st.session_state.db = carregar_dados()

st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🤖 Sistema Brazukas Top Tisp</h1>", unsafe_allow_html=True)

# Sidebar
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\b[0-9]\b', re.sub(r'\d{2}\.\d{2}\.\d{2}', '', texto))
    gols = [int(n) for n in numeros]
    return min((sum(gols) / len(gols)) * 65, 100) if len(gols) >= 2 else 0

def renderizar_bloco(titulo):
    with st.container():
        st.subheader(f"🏟️ {titulo}")
        
        # Garante que temos um dicionário para este jogo
        if titulo not in st.session_state.db:
            st.session_state.db[titulo] = {"camp":"","hora":"","casa":"","vis":"","placar":"","lista":"","prob":0}
        
        d = st.session_state.db[titulo]
        
        c1, c2 = st.columns(2)
        d["camp"] = c1.text_input("Campeonato", value=d.get("camp", ""), key=f"c_{titulo}")
        d["hora"] = c2.text_input("Horário", value=d.get("hora", ""), key=f"h_{titulo}")
        d["casa"] = st.text_input("Casa", value=d.get("casa", ""), key=f"ca_{titulo}")
        d["vis"] = st.text_input("Visitante", value=d.get("vis", ""), key=f"v_{titulo}")
        d["placar"] = st.text_input("Placar Final", value=d.get("placar", ""), key=f"p_{titulo}")
        d["lista"] = st.text_area("Lista", value=d.get("lista", ""), key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            d["prob"] = calcular_probabilidade(d["lista"])
            salvar_dados(st.session_state.db)
            st.rerun()
            
        if d.get("prob", 0) > 0:
            p_val = st.text_input("Ajustar Probabilidade", value=str(round(d["prob"], 1)), key=f"inp_{titulo}")
            msg = f"🏆 {d['camp']} | {d['casa']} x {d['vis']} | {p_val}%"
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}"):
                r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                                  data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}).json()
                if r.get("ok"):
                    d["id"] = r["result"]["message_id"]
                    d["msg"] = msg
                    salvar_dados(st.session_state.db)
                    st.rerun()

        if "id" in d:
            st.success(f"Enviado! ID: {d['id']}")
            b1, b2, b3 = st.columns(3)
            def editar(status, txt):
                requests.post(f"https://api.telegram.org/bot{token}/editMessageText", 
                              data={"chat_id": chat_id, "message_id": d["id"], "text": f"{d['msg']}\n\n{txt}", "parse_mode": "Markdown"})
            
            if b1.button("✅ GREEN", key=f"g_{titulo}"): editar("GREEN", "🎉💰 ✅ **GREENZAÇOOO!!!** 💰🎉")
            if b2.button("❌ RED", key=f"r_{titulo}"): editar("RED", "🔴 ❌ **RED!** ❌ 🔴")
            if b3.button("🔄 DEV", key=f"d_{titulo}"): editar("DEV", "🔄 *Jogo Devolvido* 🔄")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
