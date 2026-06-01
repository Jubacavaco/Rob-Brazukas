import streamlit as st
import requests
import re

st.set_page_config(page_title="Robô Brazukas Dual", layout="wide")
st.title("🤖 Painel Brazukas - Gestão Dual de Sinais")

# --- CONFIGURAÇÕES NO SIDEBAR ---
st.sidebar.header("⚙️ Configurações Telegram")
token = st.sidebar.text_input("🔑 Token", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal", type="password")

# --- FUNÇÕES ---
def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 35, 100)

def decidir_tipo(prob):
    if prob >= 65: return "Over 2.5"
    elif prob >= 70: return "Over 1.5"
    elif prob >= 55: return "BTTS"
    elif prob >= 51: return "LTD"
    return None

def get_msg(tipo, camp, casa, vis, hora):
    return f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n⏰ *Horário:* {hora}\n\n⚠️ Aposte com responsabilidade."

# --- FUNÇÃO DE PROCESSO DE JOGO ---
def gerar_bloco_jogo(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input(f"Campeonato ({titulo})", key=f"camp_{titulo}")
    casa = st.text_input(f"Time Casa ({titulo})", key=f"casa_{titulo}")
    vis = st.text_input(f"Time Vis ({titulo})", key=f"vis_{titulo}")
    hora = st.text_input(f"Horário ({titulo})", key=f"hora_{titulo}")
    lista = st.text_area(f"Cole a lista de jogos para {titulo}:", height=120, key=f"lista_{titulo}")
    
    if st.button(f"Analisar {titulo}", key=f"btn_{titulo}"):
        prob = calcular_probabilidade(lista)
        tipo = decidir_tipo(prob)
        st.write(f"📈 Probabilidade: {prob:.1f}%")
        
        if tipo:
            msg = get_msg(tipo, camp, casa, vis, hora)
            st.info(msg)
            if st.button(f"🚀 Enviar {titulo} ao Telegram", key=f"envio_{titulo}"):
                payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
                resp = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
                if resp.get("ok"): st.success(f"Sinal {titulo} enviado!")
        else:
            st.warning("Probabilidade abaixo do limite.")

# --- LAYOUT DUAL ---
col1, col2 = st.columns(2)

with col1:
    gerar_bloco_jogo("Jogo 01")

with col2:
    gerar_bloco_jogo("Jogo 02")
