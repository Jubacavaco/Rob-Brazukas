import streamlit as st
import requests
import pandas as pd

# Configuração da página
st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

# Configurações do Bot
TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1002539693401"
RODAPE = "\n\n🔞Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

# Função de Envio com Diagnóstico de Erros
def telegram(msg, msg_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    texto_final = msg + RODAPE
    try:
        if msg_id:
            resp = requests.post(url + "editMessageText", json={"chat_id": CHAT_ID, "message_id": msg_id, "text": texto_final})
        else:
            resp = requests.post(url + "sendMessage", json={"chat_id": CHAT_ID, "text": texto_final})
        
        if resp.status_code == 200:
            return resp.json().get("result", {}).get("message_id")
        else:
            st.error(f"Erro no Telegram: {resp.status_code} - Verifique se o Bot é Administrador no grupo.")
            return None
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

# Lógica de cálculo
def calcular_probabilidades(lista_str):
    try:
        nums = [int(n) for n in lista_str.replace(',', ' ').split() if n.isdigit()]
        if len(nums) < 20: nums = [1] * 20 
        h_s, h_c = nums[0:5], nums[5:10]
        a_s, a_c = nums[10:15], nums[15:20]
        avg = lambda lst: sum(lst) / len(lst) if lst else 0
        exp_h = (avg(h_s) + avg(a_c)) / 2
        exp_a = (avg(a_s) + avg(h_c)) / 2
        total = exp_h + exp_a
        return {
            "Over 1.5 FT": round(min(95, max(10, total * 35)), 1),
            "Over 2.5 FT": round(min(90, max(5, (total - 1.2) * 40)), 1),
            "BTTS": round(min(90, max(5, (exp_h * exp_a) * 30)), 1),
            "LTD": round(min(85, max(20, (total * 20) - 10)), 1),
            "Casa Vence": round(min(70, max(10, (exp_h / (total + 0.1)) * 100)), 1),
            "Visitante Vence": round(min(70, max(10, (exp_a / (total + 0.1)) * 100)), 1),
        }
    except: return {}

def definir_aposta(res):
    if res.get("Over 2.5 FT", 0) >= 65: return "Over 2.5 FT"
    if res.get("BTTS", 0) >= 55: return "BTTS"
    if res.get("LTD", 0) >= 51: return "LTD"
    if res.get("Over 1.5 FT", 0) >= 75: return "Over 1.5 FT"
    return "Nenhum mercado atingiu a meta"

# Função do jogo normal
def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    mercado = st.selectbox("Mercado", ["Match Odds", "Gols"], key=f"mercado_{nome}")
    prognostico = st.selectbox("Prognóstico", ["Over 1.5 FT", "Over 2.5 FT", "BTTS", "LTD", "Casa Vence", "Visitante Vence"], key=f"prog_{nome}")
    prob = st.number_input("Probabilidade (%)", 0, 100, 70, key=f"prob_{nome}")
    horario = st.text_input("Horário", key=f"hor_{nome}")
    ht = st.text_input("Placar HT", key=f"ht_{nome}")
    ft = st.text_input("Placar FT", key=f"ft_{nome}")
    lista = st.text_area("Lista de Análise", key=f"lista_{nome}")

    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"res_{nome}"] = calcular_probabilidades(lista)
        st.session_state[f"analise_{nome}"] = True

    if st.session_state.get(f"analise_{nome}"):
        res = st.session_state.get(f"res_{nome
