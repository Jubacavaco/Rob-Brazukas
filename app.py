import streamlit as st
import re
import requests

st.set_page_config(page_title="Robô Brazukas - Autônomo", layout="wide")
st.title("🤖 Robô Brazukas - Decisão Autônoma")

# --- SIDEBAR (CONFIGURAÇÃO E ODDS) ---
st.sidebar.header("🔑 Configurações")
token = st.sidebar.text_input("Token Telegram:", type="password")
chat_id = st.sidebar.text_input("ID Canal:", type="password")

st.sidebar.header("📊 ODDS Atuais")
odd_casa = st.sidebar.number_input("Odd Casa:", value=2.0)
odd_fora = st.sidebar.number_input("Odd Fora:", value=3.0)
odd_btts = st.sidebar.number_input("Odd BTTS:", value=1.8)

# --- CORPO ---
lista_jogos = st.text_area("Cole a lista de histórico aqui:", height=200)

def analisar_dados(texto):
    # Procura todos os pares de números (gols) no formato "X-Y" ou "X Y"
    gols = re.findall(r'(\d+)\s*[-:]\s*(\d+)', texto)
    if not gols: return 0, 0
    
    total_gols = sum(int(g[0]) + int(g[1]) for g in gols)
    btts_count = sum(1 for g in gols if int(g[0]) > 0 and int(g[1]) > 0)
    
    media = total_gols / len(gols)
    prob_btts = (btts_count / len(gols)) * 100
    return media, prob_btts

if st.button("🚀 ANALISAR E ENVIAR"):
    media, prob_btts = analisar_dados(lista_jogos)
    
    # LÓGICA DE DECISÃO DO ROBÔ
    if media >= 2.8 and odd_btts <= 1.90:
        tipo = "BTTS (Ambas Marcam)"
    elif media >= 2.5:
        tipo = "Over 2.5 FT"
    elif media >= 1.8:
        tipo = "Over 1.5 FT"
    elif odd_casa < odd_fora:
        tipo = "Casa Vence"
    else:
        tipo = "Contra o Empate (LTD)"
        
    st.write(f"📊 **Dados extraídos:** Média {media:.2f} | Prob. BTTS {prob_btts:.0f}%")
    st.success(f"O robô decidiu pela estratégia: **{tipo}**")
    
    # MENSAGEM (O robô monta baseado na decisão)
    msg = f"🚨 *Alerta de Entrada* 🚨\n\n🎯 *Mercado:* {tipo}\n..." # (Aqui entram seus modelos)
    
    # Envio Automático
    # ... (código de request.get para o Telegram)
