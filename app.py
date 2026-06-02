import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")

# --- Funções Base ---
def enviar_ou_editar(nome, msg):
    try:
        url_base = f"https://api.telegram.org/bot8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
        payload = {"chat_id": "-1003925163611", "text": msg}
        if f"msg_id_{nome}" in st.session_state:
            payload["message_id"] = st.session_state[f"msg_id_{nome}"]
            requests.post(f"{url_base}/editMessageText", json=payload)
        else:
            resp = requests.post(f"{url_base}/sendMessage", json=payload).json()
            if resp.get("ok"):
                st.session_state[f"msg_id_{nome}"] = resp["result"]["message_id"]
    except Exception as e:
        st.error(f"Erro Telegram: {e}")

# --- Interface Jogo Normal ---
def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    
    # Inputs
    camp = st.text_input("Campeonato", key=f"c_{nome}")
    casa = st.text_input("Casa", key=f"ca_{nome}")
    vis = st.text_input("Visitante", key=f"vi_{nome}")
    ht = st.text_input("Placar HT", key=f"ht_{nome}")
    ft = st.text_input("Placar FT", key=f"ft_{nome}")
    
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"dados_{nome}"] = {"camp": camp, "casa": casa, "vis": vis, "ht": ht, "ft": ft}
        st.success("Análise feita!")

    # Ações
    if f"dados_{nome}" in st.session_state:
        d = st.session_state[f"dados_{nome}"]
        if st.button("🚀 ENVIAR", key=f"env_{nome}"):
            msg = f"🚨 Alerta 🚨\n\n🏆 {d['camp']}\n🆚 {d['casa']} x {d['vis']}"
            enviar_ou_editar(nome, msg)
        
        col1, col2 = st.columns(2)
        if col1.button("✅ HT GREEN", key=f"htg_{nome}"): enviar_ou_editar(nome, f"✅ HT GREEN: {d['ht']}")
        if col2.button("❌ RED", key=f"red_{nome}"): enviar_ou_editar(nome, f"❌ RED: {d['ft']}")

# --- Layout Final ---
c1, c2, c3, c4 = st.columns(4)
with c1: jogo_normal("JOGO_A")
with c2: jogo_normal("JOGO_B")
with c3: jogo_normal("JOGO_C")
with c4: st.subheader("JOGO_D") # Mantenha seu JOGO_D aqui
