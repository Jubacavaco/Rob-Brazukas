import streamlit as st
import requests
import re
import json
import os

# Configuração da página
st.set_page_config(page_title="Sistema Brazukas", layout="wide")

# Arquivo para salvar os dados
DB_FILE = "dados_sistema.json"

def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def salvar_dados(dados):
    with open(DB_FILE, "w") as f:
        json.dump(dados, f)

# Carrega os dados persistentes
if "db" not in st.session_state:
    st.session_state.db = carregar_dados()

# Título Estilizado
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🤖 Sistema Brazukas Top Tisp</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configurações")
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    texto_limpo = re.sub(r'\d{2}\.\d{2}\.\d{2}', '', texto)
    numeros = re.findall(r'\b[0-9]\b', texto_limpo)
    gols = [int(n) for n in numeros]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 65, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Recupera dados salvos, se existirem
        d = st.session_state.db.get(titulo, {})
        
        c1, c2 = st.columns(2)
        camp = c1.text_input(f"Campeonato", value=d.get("camp", ""), key=f"c_{titulo}")
        hora = c2.text_input(f"Horário", value=d.get("hora", ""), key=f"h_{titulo}")
        
        casa = st.text_input(f"Time Casa", value=d.get("casa", ""), key=f"ca_{titulo}")
        vis = st.text_input(f"Time Visitante", value=d.get("vis", ""), key=f"v_{titulo}")
        placar = st.text_input(f"Placar Final", value=d.get("placar", ""), key=f"p_{titulo}")
        lista = st.text_area(f"Lista de jogos", value=d.get("lista", ""), key=f"l_{titulo}", height=100)
        
        # Botão Analisar
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}", use_container_width=True):
            p = calcular_probabilidade(lista)
            st.session_state.db[titulo] = {"camp": camp, "hora": hora, "casa": casa, "vis": vis, "placar": placar, "lista": lista, "prob": p}
            salvar_dados(st.session_state.db)
            st.rerun()
        
        # Se temos probabilidade, exibe resultados
        if titulo in st.session_state.db and "prob" in st.session_state.db[titulo]:
            p = st.session_state.db[titulo]["prob"]
            st.markdown("---")
            
            # Formata a mensagem e salva no banco
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* Over 1.5/2.5\n📈 *Probabilidade:* {round(p,1)}%\n⏰ *Horário:* {hora}\n\n⚠️ Aposte com responsabilidade."
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR PARA TELEGRAM", key=f"en_{titulo}", type="primary", use_container_width=True):
                payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
                r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
                if r.get("ok"): 
                    st.session_state.db[titulo]["msg_id"] = r["result"]["message_id"]
                    st.session_state.db[titulo]["msg_text"] = msg
                    salvar_dados(st.session_state.db)
                    st.rerun()

        # Botões de controle
        if "msg_id" in st.session_state.db.get(titulo, {}):
            st.markdown("---")
            col_b1, col_b2, col_b3 = st.columns(3)
            
            def editar_telegram(status, status_visual):
                msg_id = st.session_state.db[titulo]["msg_id"]
                orig_msg = st.session_state.db[titulo]["msg_text"]
                new_msg = f"{orig_msg}\n\n⚽ *Placar Final:* {placar
