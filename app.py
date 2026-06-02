import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"
RODAPE = "\n\n🔞 Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    # Chaves fixas por jogo para garantir independência
    key_camp = f"c_{titulo}"
    key_casa = f"ca_{titulo}"
    key_vis = f"v_{titulo}"
    key_analisar = f"an_{titulo}"

    camp = st.text_input("Campeonato", key=key_camp)
    casa = st.text_input("Casa", key=key_casa)
    vis = st.text_input("Visitante", key=key_vis)

    # Botão de análise
    if st.button("📊 ANALISAR", key=key_analisar):
        st.session_state[f"ativo_{titulo}"] = True
        st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis}

    # Se estiver ativo, mostra o restante
    if st.session_state.get(f"ativo_{titulo}"):
        d = st.session_state.get(f"dados_{titulo}", {})
        
        if titulo == "JOGO_D":
            hora = st.text_input("Horário", key=f"h_{titulo}")
            linha = st.text_input("Linha Canto", key=f"lin_{titulo}")
            st.write(f"💡 **Recomendação:** Over {linha} (Cantos)")
            
            if st.button("🚀 ENVIAR ALERTA", key=f"enviar_{titulo}"):
                msg = f"🏆 {d['camp']}\n⚔️ {d['casa']} x {d['vis']}\n🎯 Mercado: Cantos (Over {linha})\n🕒 {hora}\n{RODAPE}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                st.session_state[f"msg_{titulo}"] = msg
        else:
            st.write("🔥 **Mercado Pegando Fogo: 90%**")
            if st.button("🚀 ENVIAR ALERTA", key=f"enviar_{titulo}"):
                msg = f"🏆 {d['camp']}\n⚔️ {d['casa']} x {d['vis']}\n🎯 Mercado: Over Gols\n📈 Probs: 90%{RODAPE}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                st.session_state[f"msg_{titulo}"] = msg

        # Botões de Controle (MOMENTO, GREEN/RED) - Apenas se já enviado
        if f"id_{titulo}" in st.session_state:
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("MOMENTO", key=f"m_{titulo}"): st.write("Enviando Momento...")
            if c2.button("HT", key=f"ht_{titulo}"): st.write("Enviando HT...")
            if c3.button("FINAL", key=f"f_{titulo}"): st.write("Enviando Final...")
            if c4.button("RED", key=f"r_{titulo}"): st.write("Enviando Red...")

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
