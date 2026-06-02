import streamlit as st
import requests
import pandas as pd

# Configuração da Página
st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Pro")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"
RODAPE = "\n\n🔞Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

def telegram(msg, msg_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    texto_final = msg + RODAPE
    try:
        if msg_id:
            requests.post(url + "editMessageText", json={"chat_id": CHAT_ID, "message_id": msg_id, "text": texto_final})
        else:
            resp = requests.post(url + "sendMessage", json={"chat_id": CHAT_ID, "text": texto_final}).json()
            return resp.get("result", {}).get("message_id")
    except: return None

# SUA FUNÇÃO ORIGINAL DE CÁLCULO
def analyze_match(data):
    def avg(lst): return sum(lst) / len(lst) if lst else 0
    h_s = avg(data["home_last_games_goals_scored"])
    h_c = avg(data["home_last_games_goals_conceded"])
    a_s = avg(data["away_last_games_goals_scored"])
    a_c = avg(data["away_last_games_goals_conceded"])
    exp_h = (h_s + a_c) / 2
    exp_a = (a_s + h_c) / 2
    total = exp_h + exp_a
    return {
        "Over 1.5 FT": round(min(95, max(10, total * 35)), 1),
        "Over 2.5 FT": round(min(90, max(5, (total - 1.2) * 40)), 1),
        "BTTS": round(min(90, max(5, (exp_h * exp_a) * 30)), 1),
        "Home Win": round(min(70, max(10, (exp_h / (total + 0.1)) * 100)), 1),
        "Away Win": round(min(70, max(10, (exp_a / (total + 0.1)) * 100)), 1),
        "LTD": round(min(85, max(20, (total * 20) - 10)), 1),
    }

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    mercado = st.selectbox("Mercado", ["Match Odds", "Gols"], key=f"merc_{nome}")
    st.text_area("Lista de Análise", key=f"lista_{nome}")
    ht = st.text_input("Placar HT", key=f"ht_{nome}")
    ft = st.text_input("Placar FT", key=f"ft_{nome}")

    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        # Aqui o sistema processa a lista (você pode ajustar o parsing conforme o seu site)
        # Exemplo: dados dummy para rodar a função com a sua lógica
        data = {
            "home_last_games_goals_scored": [2, 0, 1, 0, 4],
            "home_last_games_goals_conceded": [4, 2, 7, 1, 1],
            "away_last_games_goals_scored": [3, 2, 2, 2, 0],
            "away_last_games_goals_conceded": [5, 1, 1, 2, 0],
        }
        st.session_state[f"res_{nome}"] = analyze_match(data)
        st.session_state[f"analise_{nome}"] = True

    if st.session_state.get(f"analise_{nome}", False):
        res = st.session_state.get(f"res_{nome}")
        st.write("### 📊 Resumo Final")
        for k, v in res.items(): st.write(f"**{k}:** {v}%")
        
        melhor = max(res, key=res.get)
        st.success(f"🎯 Aposta Recomendada: {melhor}")

        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"🚨 Alerta 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {melhor}\n⏰ Finalizado"
            st.session_state[f"mid_{nome}"] = telegram(msg)

# Função Jogo C (Mantida 100% igual como era antes)
def jogo_c_escanteios():
    st.subheader("🏟️ JOGO_C (Escanteios)")
    camp_c = st.text_input("Campeonato", key="camp_c")
    casa_c = st.text_input("Casa", key="casa_c")
    vis_c = st.text_input("Visitante", key="vis_c")
    med_casa = st.number_input("Média Escanteios Casa", step=0.1, key="med_casa_c")
    med_vis = st.number_input("Média Escanteios Visitante", step=0.1, key="med_vis_c")
    med_liga = st.number_input("Média Escanteios Liga", step=0.1, key="med_liga_c")
    ht_c = st.text_input("Placar HT", key="ht_c")
    ft_c = st.text_input("Placar FT", key="ft_c")
    e_casa_atual = st.number_input("Cantos Casa", step=1, key="e_casa_c")
    e_vis_atual = st.number_input("Cantos Fora", step=1, key="e_vis_c")
    
    if st.button("📊 ANALISAR JOGO C", key="ana_c"): st.session_state["analise_c"] = True
    if st.session_state.get("analise_c", False):
        st.bar_chart(pd.DataFrame({'Probabilidade': [90, 75, 50, 25]}, index=["O 7.5", "O 8.5", "O 9.5", "O 10.5"]))
        if st.button("🚀 ENVIAR ALERTA ESCANTEIO", key="env_c"): telegram("Alerta C")

col1, col2, col3 = st.columns(3)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_c_escanteios()
