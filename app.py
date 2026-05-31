import streamlit as st
import requests

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# --- ESTADO ---
if "msg_id" not in st.session_state: st.session_state.msg_id = None

# --- SIDEBAR (CONFIGURAÇÃO) ---
token = st.sidebar.text_input("🔑 Token:", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal:", type="password")
campeonato = st.sidebar.text_input("🏆 Campeonato:")
time_casa = st.sidebar.text_input("🆚 Time Casa:")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:")
horario = st.sidebar.text_input("⏰ Horário:")

# --- DADOS PARA CÁLCULO ---
st.sidebar.header("📊 Dados para Cálculo")
media_gols = st.sidebar.number_input("Média de Gols no Confronto:", value=2.5)
prob_btts = st.sidebar.number_input("Probabilidade BTTS (%):", value=60)

# --- FUNÇÃO DO MOTOR DE DECISÃO ---
def determinar_entrada(media, prob):
    if media >= 2.5 and prob >= 65:
        return "Over 2.5 FT"
    elif prob >= 60:
        return "BTTS (Ambas Marcam)"
    elif media >= 2.0:
        return "Over 1.5 FT"
    else:
        return "Contra o Empate (LTD)"

# --- LÓGICA ---
if st.button("▶️ ANALISAR E DECIDIR"):
    entrada_escolhida = determinar_entrada(media_gols, prob_btts)
    st.success(f"O robô decidiu a entrada: **{entrada_escolhida}**")
    
    # Monta a mensagem baseada na escolha
    def formatar_msg(tipo):
        base = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n🆚 *Jogo:* {time_casa} x {time_visitante}\n"
        if tipo == "Over 2.5 FT": return base + "🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 2.5 FT\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 2 gols no HT, saia com lucro.\n* Entrada para FT."
        if tipo == "BTTS (Ambas Marcam)": return base + "🎯 *Mercado:* BTTS\n💥 *Prognóstico:* Ambas - SIM\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, saia com lucro."
        if tipo == "Over 1.5 FT": return base + "🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 1.5 FT\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada antes do início!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, saia com lucro."
        return base + "🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Contra o Empate (LTD)\n⏰ *Horário:* " + horario + "\n\n📌 Entrada recomendada Ao vivo!\n\n⚽ **Gestão de Jogo (Ao Vivo):**\n* Se houver 1 gol no HT, saia com lucro."

    msg = formatar_msg(entrada_escolhida)
    st.code(msg)
    st.session_state.msg_final = msg

# --- ENVIO E CONTROLE ---
if "msg_final" in st.session_state:
    if st.button("🚀 Enviar Sinal"):
        # Lógica de envio (mesma de antes)
        st.success("Enviado!")
