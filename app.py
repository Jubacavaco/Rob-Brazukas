import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"
RODAPE = "\n\n🔞 Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

# Função para enviar/editar no Telegram
def telegram_api(method, data):
    return requests.post(f"https://api.telegram.org/bot{TOKEN}/{method}", data=data).json()

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    # Inputs (Armazenados no session_state para não apagar)
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    
    if titulo == "JOGO_D":
        hora, cc, cv = st.text_input("Horário", key=f"h_{titulo}"), st.number_input("Cantos Casa", key=f"cc_{titulo}"), st.number_input("Cantos Vis", key=f"cv_{titulo}")
        ou, linha, ent = st.selectbox("Selecione", ["Over", "Under"], key=f"ou_{titulo}"), st.text_input("Linha Canto", key=f"lin_{titulo}"), st.text_input("Entrada", key=f"en_{titulo}")
        
        if st.button("📊 ANALISAR JOGO D", key=f"an_{titulo}"):
            st.session_state[f"ativo_{titulo}"] = True
            
        if st.session_state.get(f"ativo_{titulo}"):
            st.write(f"💡 **Recomendação:** {ou} {linha} (Cantos)")
            if st.button("🚀 ENVIAR ALERTA", key=f"bt_enviar_{titulo}"):
                msg = f"🏆 Campeonato: {camp}\n⚔️ Confronto: {casa} x {vis}\n🎯 Mercado: Cantos ({ou} {linha})\n💎 Entrada: {ent}\n🕒 Horário: {hora}\n{RODAPE}"
                res = telegram_api("sendMessage", {"chat_id": CHAT_ID, "text": msg})
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg

        if f"id_{titulo}" in st.session_state:
            def ed_d(status):
                info = f"\n\n---\n🏠 Casa: {int(cc)}\n✈️ Vis: {int(cv)}\n📊 Total: {int(cc+cv)}"
                txt = f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}{info}\n\n{status}\n{RODAPE}"
                telegram_api("editMessageText", {"chat_id": CHAT_ID, "message_id": st.session_state[f"id_{titulo}"], "text": txt})
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("MOMENTO", key=f"m_{titulo}"): ed_d("INFO")
            if c2.button("HT", key=f"ht_{titulo}"): ed_d("✅ GREEN HT ✅")
            if c3.button("HT 2", key=f"ht2_{titulo}"): ed_d("❌ RED HT ❌")
            if c4.button("FINAL", key=f"fin_{titulo}"): ed_d("✅ GREEN FINAL ✅")

    else: # Jogos A, B, C
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        if st.button("📊 ANALISAR", key=f"an_{titulo}"):
            st.session_state[f"ativo_{titulo}"] = True
            
        if st.session_state.get(f"ativo_{titulo}"):
            st.write("🔥 **Mercado Pegando Fogo: 90%**")
            if st.button("🚀 ENVIAR ALERTA", key=f"bt_enviar_{titulo}"):
                msg = f"🏆 Campeonato: {camp}\n⚔️ Confronto: {casa} x {vis}\n🎯 Mercado: Over Gols\n💎 Entrada: O1.5 FT\n🕒 Horário: 15:00\n{RODAPE}"
                res = telegram_api("sendMessage", {"chat_id": CHAT_ID, "text": msg})
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg
            
            if f"id_{titulo}" in st.session_state:
                def ed_abc(status, txt_extra):
                    txt = f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}\n\n---\n⚽ {txt_extra}\n\n{status}\n{RODAPE}"
                    telegram_api("editMessageText", {"chat_id": CHAT_ID, "message_id": st.session_state[f"id_{titulo}"], "text": txt})
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("MOMENTO", key=f"m_{titulo}"): ed_abc("INFO", "Jogo em andamento")
                if c2.button("HT", key=f"ht_{titulo}"): ed_abc("⚪ EM ANDAMENTO ⚪", "HT: Ok")
                if c3.button("FINAL", key=f"f_{titulo}"): ed_abc("✅ GREEN GIGANTE ✅", "Final: Green")
                if c4.button("RED", key=f"r_{titulo}"): ed_abc("❌ RED ❌", "Final: Red")

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
