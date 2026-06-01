import streamlit as st
import requests
import re

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🤖 Painel Brazukas - Cálculo por Estatística")

# --- SIDEBAR (CONFIGURAÇÕES) ---
token = st.sidebar.text_input("🔑 Token Telegram", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal", type="password")
campeonato = st.sidebar.text_input("🏆 Campeonato")
time_casa = st.sidebar.text_input("🆚 Time Casa")
time_visitante = st.sidebar.text_input("🆚 Time Visitante")
horario = st.sidebar.text_input("⏰ Horário")

# --- LISTA DE JOGOS ---
st.subheader("📋 Cole aqui a lista de jogos do site")
lista_jogos = st.text_area("Ex: Cruzeiro 2 1, Fluminense 3 1...", height=150)

# --- FUNÇÃO DE CÁLCULO DE PROBABILIDADE ---
def calcular_probabilidade(texto):
    # Procura todos os números na lista (os gols)
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10] # Filtra apenas números plausíveis como gols
    
    if len(gols) < 2: return 0
    
    media = sum(gols) / len(gols)
    # Exemplo de lógica: Média acima de 2.5 gols = 80% de chance de Over 2.5
    # Média entre 1.5 e 2.5 = 70% de chance de BTTS
    prob = min(media * 35, 100) 
    return prob

# --- MODELOS DE MENSAGEM ---
def get_msg(tipo, camp, casa, vis, hora):
    base = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n"
    if tipo == "Over 2.5":
        corpo = f"🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 2.5 FT\n⏰ *Horário:* {hora}\n\n📌 Entrada baseada em alta média de gols!"
    elif tipo == "BTTS":
        corpo = f"🎯 *Mercado:* BTTS\n💥 *Prognóstico:* Ambas - SIM\n⏰ *Horário:* {hora}\n\n📌 Entrada baseada em histórico de gols de ambos!"
    else:
        corpo = f"🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Contra o Empate (LTD)\n⏰ *Horário:* {hora}\n\n📌 Entrada padrão!"
    return base + corpo + "\n\n⚠️ Aposte com responsabilidade."

# --- LÓGICA DE ANÁLISE ---
if "msg_preview" not in st.session_state: st.session_state.msg_preview = None

if st.button("📊 Analisar Estatísticas e Gerar Sinal"):
    if not lista_jogos:
        st.error("Cole os dados!")
    else:
        prob = calcular_probabilidade(lista_jogos)
        st.write(f"📈 **Probabilidade Calculada:** {prob:.1f}%")
        
        # Lógica de decisão baseada na % calculada da lista
        if prob >= 75: tipo = "Over 2.5"
        elif prob >= 55: tipo = "BTTS"
        else: tipo = "LTD"
        
        st.session_state.msg_preview = get_msg(tipo, campeonato, time_casa, time_visitante, horario)

# --- PRÉ-VISUALIZAÇÃO E ENVIO ---
if st.session_state.msg_preview:
    st.info(st.session_state.msg_preview)
    if st.button("🚀 Enviar para Telegram"):
        payload = {"chat_id": chat_id, "text": st.session_state.msg_preview, "parse_mode": "Markdown"}
        resp = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
        if resp.get("ok"):
            st.session_state.msg_id = resp["result"]["message_id"]
            st.session_state.ultima_msg = st.session_state.msg_preview
            st.success("Enviado!")
            st.session_state.msg_preview = None

# --- ATUALIZAÇÃO DE RESULTADO (Mesmo código anterior) ---
if "msg_id" in st.session_state and st.session_state.msg_id:
    # (Adicione aqui o bloco de botões Green/Red/Devolvida)
