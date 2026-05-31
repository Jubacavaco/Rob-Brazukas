import streamlit as st
import requests

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# --- ESTADO (Memória) ---
if "msg_id" not in st.session_state: st.session_state.msg_id = None
if "msg_atual" not in st.session_state: st.session_state.msg_atual = ""

# --- SIDEBAR ---
st.sidebar.header("🤖 CONFIGURAÇÃO")
token = st.sidebar.text_input("🔑 Token:", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal:", type="password")

st.sidebar.header("📅 DADOS DO JOGO")
campeonato = st.sidebar.text_input("🏆 Campeonato:")
time_casa = st.sidebar.text_input("🆚 Time Casa:")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:")
horario = st.sidebar.text_input("⏰ Horário:")

# --- SELEÇÃO DO MODELO ---
st.subheader("📋 Definição de Entrada")
tipo_entrada = st.selectbox("Escolha o modelo:", 
    ["Contra o Empate (LTD)", "BTTS (Ambas Marcam)", "Casa Vence", "Over 1.5 FT", "Over 2.5 FT"])

def gerar_mensagem(tipo, status=""):
    base = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n🆚 *Jogo:* {time_casa} x {time_visitante}\n"
    rodape = f"\n\n⚽ *Status:* {status}\n\n⚠️ Aposte com responsabilidade."
    
    corpo = ""
    if tipo == "Contra o Empate (LTD)": corpo = "🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Contra o Empate (LTD)\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada Ao vivo!"
    elif tipo == "BTTS (Ambas Marcam)": corpo = "🎯 *Mercado:* BTTS\n💥 *Prognóstico:* Ambas - SIM\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!"
    elif tipo == "Casa Vence": corpo = "🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Casa Vence\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!"
    elif tipo == "Over 1.5 FT": corpo = "🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 1.5 FT\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!"
    elif tipo == "Over 2.5 FT": corpo = "🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 2.5 FT\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!"
    
    return base + corpo + rodape

st.session_state.msg_atual = gerar_mensagem(tipo_entrada, "Pendente")
st.code(st.session_state.msg_atual)

# --- AÇÃO: ENVIAR ---
if st.button("🚀 Enviar Sinal"):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": st.session_state.msg_atual, "parse_mode": "Markdown"}
    resp = requests.get(url, params=params).json()
    if resp.get("ok"):
        st.session_state.msg_id = resp["result"]["message_id"]
        st.success("Sinal enviado!")
    else: st.error(f"Erro: {resp.get('description')}")

# --- AÇÃO: EDITAR STATUS ---
if st.session_state.msg_id:
    st.subheader("🎯 Registrar Resultado (Atualiza no Telegram)")
    c1, c2, c3 = st.columns(3)
    
    def atualizar_telegram(status):
        nova_msg = gerar_mensagem(tipo_entrada, status)
        url = f"https://api.telegram.org/bot{token}/editMessageText"
        params = {"chat_id": chat_id, "message_id": st.session_state.msg_id, "text": nova_msg, "parse_mode": "Markdown"}
        requests.get(url, params=params)
        st.rerun()

    if c1.button("🟢 Green"): atualizar_telegram("✅ GREEN")
    if c2.button("🔴 Red"): atualizar_telegram("❌ RED")
    if c3.button("🟡 Push"): atualizar_telegram("⚪ PUSH")
