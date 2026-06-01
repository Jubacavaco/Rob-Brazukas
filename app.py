import streamlit as st
import requests

st.set_page_config(page_title="Robô Brazukas", layout="wide")

st.title("🤖 Painel Brazukas - Gestão de Sinais")

# --- SIDEBAR E CONFIGURAÇÕES ---
st.sidebar.header("⚙️ Configurações")
token = st.sidebar.text_input("🔑 Token Telegram", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal", type="password")

st.sidebar.header("📅 Dados do Jogo")
campeonato = st.sidebar.text_input("🏆 Campeonato")
time_casa = st.sidebar.text_input("🆚 Time Casa")
time_visitante = st.sidebar.text_input("🆚 Time Visitante")
horario = st.sidebar.text_input("⏰ Horário")

st.sidebar.header("📊 Odds")
odd_o15 = st.sidebar.number_input("Odd O1.5", 1.0)
odd_btts = st.sidebar.number_input("Odd BTTS", 1.0)
odd_o25 = st.sidebar.number_input("Odd O2.5", 1.0)

# --- LISTA DE JOGOS ---
st.subheader("📋 Dados Estatísticos")
lista_jogos = st.text_area("Cole aqui a lista de jogos:", height=150)

# --- FUNÇÃO DE MENSAGENS ---
def get_msg(tipo, camp, casa, vis, hora):
    rodape = "\n\n⚠️ Aposte com responsabilidade. Não há garantias de lucro."
    base = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n"
    
    if tipo == "LTD":
        corpo = f"🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Contra o Empate (LTD)\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada Ao vivo!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.\n* Se terminar 0 x 0 no HT, permaneça na posição LTD."
    elif tipo == "BTTS":
        corpo = f"🎯 *Mercado:* BTTS\n💥 *Prognóstico:* Ambas - SIM\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.\n* Se terminar 0 x 0 no HT, permaneça na posição Ambas Sim."
    elif tipo == "Casa Vence":
        corpo = f"🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Casa Vence\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Essa é uma entrada para FT (Full Time)."
    elif tipo == "Over 1.5":
        corpo = f"🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 1.5 FT\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.\n* Se terminar 0 x 0 no HT, permaneça no Over 1.5 FT."
    else:
        corpo = f"🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 2.5 FT\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 2 gols no HT, sugiro que saia do mercado com um pequeno lucro.\n* Essa é uma entrada para FT (Full Time)."
    
    return base + corpo + rodape

# --- LÓGICA E ESTADO ---
if "msg_preview" not in st.session_state: st.session_state.msg_preview = None

if st.button("🔍 Analisar e Gerar"):
    if not lista_jogos:
        st.error("Por favor, cole a lista de jogos.")
    else:
        # Lógica de seleção (ajuste conforme seu cálculo)
        tipo = "Over 2.5" if odd_o25 < 2.0 else "LTD"
        st.session_state.msg_preview = get_msg(tipo, campeonato, time_casa, time_visitante, horario)

if st.session_state.msg_preview:
    st.info(st.session_state.msg_preview)
    if st.button("🚀 Confirmar e Enviar"):
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": st.session_state.msg_preview, "parse_mode": "Markdown"}
        resp = requests.post(url, data=payload).json()
        if resp.get("ok"):
            st.session_state.msg_id = resp["result"]["message_id"]
            st.session_state.ultima_msg = st.session_state.msg_preview
            st.success("Enviado!")
            st.session_state.msg_preview = None

if "msg_id" in st.session_state and st.session_state.msg_id:
    c1, c2, c3 = st.columns(3)
    if c1.button("✅ GREEN"):
        requests.post(f"https://api.telegram.org/bot{token}/editMessageText", data={"chat_id": chat_id, "message_id": st.session_state.msg_id, "text": st.session_state.ultima_msg + "\n\n🔄 *Status:* ✅ GREEN!!", "parse_mode": "Markdown"})
    if c2.button("❌ RED"):
        requests.post(f"https://api.telegram.org/bot{token}/editMessageText", data={"chat_id": chat_id, "message_id": st.session_state.msg_id, "text": st.session_state.ultima_msg + "\n\n🔄 *Status:* ❌ RED!", "parse_mode": "Markdown"})
    if c3.button("🔄 DEVOLVIDA"):
        requests.post(f"https://api.telegram.org/bot{token}/editMessageText", data={"chat_id": chat_id, "message_id": st.session_state.msg_id, "text": st.session_state.ultima_msg + "\n\n🔄 *Status:* 🔄 DEVOLVIDA", "parse_mode": "Markdown"})
