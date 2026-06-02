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

# Lógica Estatística Integrada
def analyze_match(data):
    def avg(lst): return sum(lst) / len(lst) if lst else 0
    home_attack = avg(data["home_last_games_goals_scored"])
    home_defense = avg(data["home_last_games_goals_conceded"])
    away_attack = avg(data["away_last_games_goals_scored"])
    away_defense = avg(data["away_last_games_goals_conceded"])
    expected_home_goals = (home_attack + away_defense) / 2
    expected_away_goals = (away_attack + home_defense) / 2
    total_goals = expected_home_goals + expected_away_goals
    return {
        "Over 1.5 FT (%)": round(min(95, max(10, total_goals * 35)), 1),
        "Over 2.5 FT (%)": round(min(90, max(5, (total_goals - 1.2) * 40)), 1),
        "BTTS (%)": round(min(90, max(5, (expected_home_goals * expected_away_goals) * 30)), 1),
        "Home Win (%)": round(min(70, max(10, (expected_home_goals / (total_goals + 0.1)) * 100)), 1),
        "Away Win (%)": round(min(70, max(10, (expected_away_goals / (total_goals + 0.1)) * 100)), 1),
        "Lay The Draw (%)": round(min(85, max(20, (total_goals * 20) - 10)), 1),
    }

# Função Jogo Normal (A e B)
def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    mercado = st.selectbox("Mercado", ["Match Odds", "Gols"], key=f"merc_{nome}")
    horario = st.text_input("Horário", key=f"hor_{nome}")
    ht = st.text_input("Placar HT", key=f"ht_{nome}")
    ft = st.text_input("Placar FT", key=f"ft_{nome}")
    
    st.write("---")
    h_goals = st.text_input("Casa: Gols Feitos (ex: 2,0,1,0,4)", key=f"h_g_{nome}")
    h_conc = st.text_input("Casa: Gols Sofridos (ex: 4,2,7,1,1)", key=f"h_c_{nome}")
    a_goals = st.text_input("Visitante: Gols Feitos (ex: 3,2,2,2,0)", key=f"a_g_{nome}")
    a_conc = st.text_input("Visitante: Gols Sofridos (ex: 5,1,1,2,0)", key=f"a_c_{nome}")

    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        try:
            data = {
                "home_last_games_goals_scored": [int(x) for x in h_goals.split(',')],
                "home_last_games_goals_conceded": [int(x) for x in h_conc.split(',')],
                "away_last_games_goals_scored": [int(x) for x in a_goals.split(',')],
                "away_last_games_goals_conceded": [int(x) for x in a_conc.split(',')],
            }
            st.session_state[f"res_{nome}"] = analyze_match(data)
            st.session_state[f"analise_{nome}"] = True
        except: st.error("Erro nos dados! Use apenas números separados por vírgula.")

    # Verificação de segurança adicionada aqui
    if st.session_state.get(f"analise_{nome}", False) and f"res_{nome}" in st.session_state:
        res = st.session_state[f"res_{nome}"]
        st.write("### 📊 Resultado Estatístico")
        for k, v in res.items(): st.write(f"**{k}:** {v}%")
        
        melhor = max(res, key=res.get)
        st.success(f"🎯 Sugestão: {melhor}")

        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            res_str = "\n".join([f"{k}: {v}%" for k, v in res.items()])
            msg = f"🚨 Alerta de Entrada 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n{res_str}\n⏰ {horario}"
            st.session_state[f"mid_{nome}"] = telegram(msg)

        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            base = f"🚨 Alerta de Entrada 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n⏰ {horario}"
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key=f"htg_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\n✅✅✅ GREEN ✅✅✅", mid)
            if c2.button("🏆 FINAL", key=f"fng_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            if c2.button("❌ RED", key=f"red_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n❌❌❌ RED ❌❌❌", mid)

# Função Jogo C (Intacta)
def jogo_c_escanteios():
    st.subheader("🏟️ JOGO_C (Escanteios)")
    camp_c = st.text_input("Campeonato", key="camp_c")
    casa_c = st.text_input("Casa", key="casa_c")
    vis_c = st.text_input("Visitante", key="vis_c")
    ht_c = st.text_input("Placar HT", key="ht_c")
    ft_c = st.text_input("Placar FT", key="ft_c")
    e_casa_atual = st.number_input("Cantos Casa", step=1, key="e_casa_c")
    e_vis_atual = st.number_input("Cantos Fora", step=1, key="e_vis_c")
    
    if st.button("📊 ANALISAR JOGO C", key="ana_c"): st.session_state["analise_c"] = True
    if st.session_state.get("analise_c", False):
        st.write("### 📊 Gráfico de Escanteios FT")
        st.bar_chart(pd.DataFrame({'Probabilidade': [90, 75, 50, 25]}, index=["O 7.5", "O 8.5", "O 9.5", "O 10.5"]))
        linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5], key="linha_c")
        if st.button("🚀 ENVIAR ALERTA ESCANTEIO", key="env_c"):
            st.session_state["mid_c"] = telegram(f"🚨 Escanteio: {linha}")

# Layout
col1, col2, col3 = st.columns(3)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_c_escanteios()
