import streamlit as st
import requests
import re
import json
import os

st.set_page_config(page_title="Sistema Brazukas", layout="wide")

# CSS para um visual moderno
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { border-radius: 10px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "dados_brazukas.json"

def carregar_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def salvar_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

if "db" not in st.session_state:
    st.session_state.db = carregar_db()

st.markdown("<h1 style='text-align: center;'>🤖 Sistema Brazukas Top Tips</h1>", unsafe_allow_html=True)
st.write("---")

with st.sidebar:
    st.header("⚙️ Configurações")
    token = st.text_input("Token Telegram", type="password")
    chat_id = st.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    texto_limpo = re.sub(r'\d{2}\.\d{2}\.\d{2}', '', texto)
    numeros = re.findall(r'\b[0-9]\b', texto_limpo)
    gols = [int(n) for n in numeros]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 65, 100)

def renderizar_bloco(titulo):
    with st.container():
        st.subheader(f"🏟️ {titulo}")
        
        if titulo not in st.session_state.db:
            st.session_state.db[titulo] = {}
        d = st.session_state.db[titulo]
        
        c1, c2 = st.columns(2)
        camp = c1.text_input("Campeonato", value=d.get("camp", ""), key=f"c_{titulo}")
        hora = c2.text_input("Horário", value=d.get("hora", ""), key=f"h_{titulo}")
        
        col_c, col_v, col_p = st.columns(3)
        casa = col_c.text_input("Casa", value=d.get("casa", ""), key=f"ca_{titulo}")
        vis = col_v.text_input("Visitante", value=d.get("vis", ""), key=f"v_{titulo}")
        placar = col_p.text_input("Placar", value=d.get("placar", ""), key=f"p_{titulo}")
        
        lista = st.text_area("Lista de jogos", value=d.get("lista", ""), key=f"l_{titulo}", height=80)
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}", use_container_width=True):
            p = calcular_probabilidade(lista)
            st.session_state.db[titulo].update({
                "camp": camp, "hora": hora, "casa": casa, "vis": vis, 
                "placar": placar, "lista": lista, "prob": p
            })
            salvar_db(st.session_state.db)
            st.rerun()
        
        if "prob" in st.session_state.db[titulo]:
            p = st.session_state.db[titulo]["prob"]
            st.markdown("---")
            st.write("📊 **Análise de Mercados:**")
            
            # Cálculo das porcentagens de cada mercado
            v15 = min(p + 5, 100)
            v25 = min(p, 100)
            vBTTS = min(p + 2, 100)
            vLTD = min(100 - p, 100)
            
            # Exibir gráficos com números
            cols = st.columns(4)
            cols[0].write(f"Over 1.5: **{v15:.0f}%**")
            cols[0].progress(v15/100)
            cols[1].write(f"Over 2.5: **{v25:.0f}%**")
            cols[1].progress(v25/100)
            cols[2].write(f"BTTS: **{vBTTS:.0f}%**")
            cols[2].progress(vBTTS/100)
            cols[3].write(f"LTD: **{vLTD:.0f}%**")
            cols[3].progress(vLTD/100)
            
            mercado_escolhido = st.selectbox("Definir Mercado de Envio", 
                                            ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], 
                                            key=f"sel_{titulo}")
            
            # Lógica automática
            if mercado_escolhido == "Automático":
                if p >= 70: mercado_final = "Over 1.5 FT"
                elif p >= 50: mercado_final = "Ambas Marcam (BTTS)"
                else: mercado_final = "LTD"
            else:
                mercado_final = mercado_escolhido
            
            prob_val = st.text_input("Ajustar Prob (%)", value=str(round(p, 1)), key=f"inp_{titulo}")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {mercado_final}\n📈 *Probabilidade:* {prob_val}%\n⏰ *Horário:* {hora}\n\n⚠️ Aposte com responsabilidade."
            
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR PARA TELEGRAM", key=f"en_{titulo}", type="primary", use_container_width=True):
                payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
                r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
                if r.get("ok"): 
                    st.session_state.db[titulo].update({"id": r["result"]["message_id"], "msg": msg})
                    salvar_db(st.session_state.db)
                    st.rerun()

        if "id" in st.session_state.db[titulo]:
            st.markdown("---")
            b1, b2, b3 = st.columns(3)
            def editar_telegram(status, status_visual):
                msg_id = st.session_state.db[titulo]["id"]
                original_msg = st.session_state.db[titulo]["msg"]
                new_msg = f"{original_msg}\n\n⚽ *Placar Final:* {placar}\n\n{status_visual}"
                requests.post(f"https://api.telegram.org/bot{token}/editMessageText", 
                              data={"chat_id": chat_id, "message_id": msg_id, "text": new_msg, "parse_mode": "Markdown"})
                st.success("Atualizado!")
            
            if b1.button("✅ GREEN", key=f"g_{titulo}"): editar_telegram("GREEN", "🎉💰 ✅ **GREENZAÇOOO!!!** 💰🎉")
            if b2.button("❌ RED", key=f"r_{titulo}"): editar_telegram("RED", "🔴 ❌ **RED!** ❌ 🔴")
            if b3.button("🔄 DEV", key=f"d_{titulo}"): editar_telegram("DEVOLVIDA", "🔄 *Jogo Devolvido* 🔄")

col_a, col_b = st.columns(2)
with col_a: renderizar_bloco("JOGO_A")
with col_b: renderizar_bloco("JOGO_B")
