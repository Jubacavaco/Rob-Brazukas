import streamlit as st
import requests

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🤖 Painel Brazukas - Gestão de Sinais")

# --- CONFIGURAÇÃO (OCULTA) ---
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

# --- MODELOS ---
def get_msg(tipo, camp, casa, vis, hora):
    base = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n"
    rodape = "\n\n⚠️ Aposte com responsabilidade. Não há garantias de lucro."
    # ... (mesma função do código anterior) ...
    if tipo == "LTD": corpo = "🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Contra o Empate (LTD)\n⏰ *Horário:* " + hora + "\n\n📌 Entrada recomendada Ao vivo!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.\n* Se terminar 0 x 0 no HT, permaneça na posição LTD."
    elif tipo == "BTTS": corpo = "🎯 *Mercado:* BTTS\n💥 *Prognóstico:* Ambas - SIM\n⏰ *Horário:* " + hora + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.\n* Se terminar 0 x 0 no HT, permaneça na posição Ambas Sim."
    elif tipo == "Casa Vence": corpo = "🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Casa Vence\n⏰ *Horário:* " + hora + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Essa é uma entrada para FT (Full Time)."
    elif tipo == "Over 1.5": corpo = "🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 1.5 FT\n⏰ *Horário:* " + hora + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.\n* Se terminar 0 x 0 no HT, permaneça no Over 1.5 FT."
    elif tipo == "Over 2.5": corpo = "🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 2.5 FT\n⏰ *Horário:* " + hora + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 2 gols no HT, sugiro que saia do mercado com um pequeno lucro.\n* Essa é uma entrada para FT (Full Time)."
    return base + corpo + rodape

# --- LÓGICA DE PRÉ-VISUALIZAÇÃO ---
if "msg_preview" not in st.session_state: st.session_state.msg_preview = None

if st.button("🔍 Gerar Pré-visualização"):
    # Sua lógica de decisão
    if odd_o25 < 2.0: tipo = "Over 2.5"
    elif odd_btts < 1.9: tipo = "BTTS"
    else: tipo = "LTD"
    st.session_state.msg_preview = get_msg(tipo, campeonato, time_casa, time_visitante, horario)

if st.session_state.msg_preview:
    st.subheader("📝 Pré-visualização do Sinal:")
    st.info(st.session_state.msg_preview)
    
    if st.button("🚀 Confirmar e Enviar para Telegram"):
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": st.session_state.msg_preview, "parse_mode": "Markdown"}
        resp = requests.post(url, data=payload).json()
        if resp.get("ok"):
            st.session_state.msg_id = resp["result"]["message_id"]
            st.session_state.ultima_msg = st.session_state.msg_preview
            st.success("Enviado com sucesso!")
            st.session_state.msg_preview = None # Limpa após enviar

# --- ATUALIZAÇÃO ---
if "msg_id" in st.session_state and st.session_state.msg_id:
    # ... (mesmo código de botões Green/Red/Devolvida anterior)
