import streamlit as st
import requests

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# --- ESTADO ---
if "executado" not in st.session_state: st.session_state.executado = False

# --- SIDEBAR ---
st.sidebar.header("🤖 CONFIGURAÇÃO")
token = st.sidebar.text_input("🔑 Token:", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal:", type="password")

st.sidebar.header("📅 DADOS DO JOGO")
campeonato = st.sidebar.text_input("🏆 Campeonato:")
time_casa = st.sidebar.text_input("🆚 Time Casa:")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:")
horario = st.sidebar.text_input("⏰ Horário:")

# --- CORPO ---
st.subheader("📋 Definição de Entrada")
tipo_entrada = st.selectbox("Escolha o modelo de sinal:", 
    ["Contra o Empate (LTD)", "BTTS (Ambas Marcam)", "Casa Vence", "Over 1.5 FT", "Over 2.5 FT"])

def gerar_mensagem(tipo):
    base = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n🆚 *Jogo:* {time_casa} x {time_visitante}\n"
    rodape = "\n\n⚠️ Aposte com responsabilidade. Não há garantias de lucro."
    
    if tipo == "Contra o Empate (LTD)":
        return base + "🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Contra o Empate (LTD)\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada Ao vivo!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.\n* Se terminar 0 x 0 no HT, permaneça na posição LTD." + rodape
    elif tipo == "BTTS (Ambas Marcam)":
        return base + "🎯 *Mercado:* BTTS\n💥 *Prognóstico:* Ambas - SIM\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.\n* Se terminar 0 x 0 no HT, permaneça na posição Ambas Sim." + rodape
    elif tipo == "Casa Vence":
        return base + "🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Casa Vence\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Essa é uma entrada para FT (Full Time)." + rodape
    elif tipo == "Over 1.5 FT":
        return base + "🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 1.5 FT\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.\n* Se terminar 0 x 0 no HT, permaneça no Over 1.5 FT." + rodape
    elif tipo == "Over 2.5 FT":
        return base + "🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 2.5 FT\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 2 gols no HT, sugiro que saia do mercado com um pequeno lucro.\n* Essa é uma entrada para FT (Full Time)." + rodape

msg = gerar_mensagem(tipo_entrada)
st.code(msg)

if st.button("🚀 Enviar para o Telegram"):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
    resp = requests.get(url, params=params).json()
    if resp.get("ok"): st.success("Sinal enviado!")
    else: st.error(f"Erro: {resp.get('description')}")

# CONTROLE DE RESULTADOS
st.subheader("🎯 Controle Interno")
c1, c2, c3, c4 = st.columns(4)
if c1.button("🟢 Green"): st.success("Green registrado!")
if c2.button("🔴 Red"): st.error("Red registrado!")
if c3.button("🟡 Push"): st.warning("Push registrado!")
if c4.button("⚪ Resetar"): st.rerun()
