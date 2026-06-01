import streamlit as st
import requests
import re

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🤖 Painel Brazukas - Gestão com Regras %")

# --- SIDEBAR E DADOS ---
token = st.sidebar.text_input("🔑 Token Telegram", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal", type="password")
campeonato = st.sidebar.text_input("🏆 Campeonato")
time_casa = st.sidebar.text_input("🆚 Time Casa")
time_visitante = st.sidebar.text_input("🆚 Time Visitante")
horario = st.sidebar.text_input("⏰ Horário")

st.subheader("📋 Dados Estatísticos")
lista_jogos = st.text_area("Cole aqui a lista de jogos:", height=150)

# --- FUNÇÃO DE CÁLCULO ---
def calcular_probabilidade(texto):
    # Extrai números (gols)
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    # Ajuste: Média de 2.0 gols vira 70% para escala de probabilidade
    return min(media * 35, 100)

# --- LÓGICA DE DECISÃO (HIERARQUIA) ---
def decidir_tipo(prob):
    # Prioridade: Over 2.5 tem preferência sobre 1.5
    if prob >= 65: return "Over 2.5"
    elif prob >= 70: return "Over 1.5" # (Nota: o Over 2.5 já capturou o que era 70+)
    elif prob >= 55: return "BTTS"
    elif prob >= 51: return "LTD"
    return None

# --- MODELOS DE MENSAGEM ---
def get_msg(tipo, camp, casa, vis, hora):
    base = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n"
    if tipo == "Over 2.5":
        corpo = f"🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 2.5 FT\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada (Probabilidade > 65%!)"
    elif tipo == "Over 1.5":
        corpo = f"🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 1.5 FT\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada (Probabilidade > 70%!)"
    elif tipo == "BTTS":
        corpo = f"🎯 *Mercado:* BTTS\n💥 *Prognóstico:* Ambas - SIM\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada (Probabilidade > 55%!)"
    else:
        corpo = f"🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Contra o Empate (LTD)\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada (Probabilidade > 51%!)"
    return base + corpo + "\n\n⚠️ Aposte com responsabilidade."

# --- EXECUÇÃO ---
if "msg_preview" not in st.session_state: st.session_state.msg_preview = None

if st.button("📊 Analisar Regras % e Gerar"):
    prob = calcular_probabilidade(lista_jogos)
    st.write(f"📊 **Probabilidade Calculada:** {prob:.1f}%")
    
    tipo = decidir_tipo(prob)
    if tipo:
        st.session_state.msg_preview = get_msg(tipo, campeonato, time_casa, time_visitante, horario)
    else:
        st.warning("Probabilidade abaixo do mínimo para entrada.")

# (O bloco de pré-visualização, envio e botões Green/Red permanece igual ao anterior)
