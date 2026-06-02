import streamlit as st
import requests
import pandas as pd

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

def processar_calculo(lista_str):
    nums = [int(n) for n in lista_str.replace(' ', '').replace(',', ' ').split() if n.isdigit()]
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
        "Home Win": round(min(70, max(10, (exp_h / (total + 0.1)) * 100)), 1),
        "Away Win": round(min(70, max(10, (exp_a / (total + 0.1)) * 100)), 1),
        "LTD": round(min(85, max(20, (total * 20) - 10)), 1),
    }

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    prognostico = st.selectbox("Prognóstico", ["Over 1.5 FT", "Over 2.5 FT", "BTTS", "LTD", "Casa Vence", "Visitante Vence"], key=f"prog_{nome}")
    prob = st.number_input("Probabilidade (%)", 0, 100, 70, key=f"prob_{nome}")
    horario = st.text_input("Horário", key=f"hor_{nome}")
    ht = st.text_input("Placar HT", key=f"ht_{nome}")
    ft = st.text_input("Placar FT", key=f"ft_{nome}")
    lista = st.text_area("Lista de Análise", key=f"lista_{nome}")

    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"res_{nome}"] = processar_calculo(lista)
        st.session_state[f"analise_{nome}"] = True

    if st.session_state.get(f"analise_{nome}"):
        res = st.session_state.get(f"res_{nome}")
        st.write("### 📊 Resumo")
        for k, v in res.items(): st.write(f"**{k}:** {v}%")
        
        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"🚨 Alerta de Entrada 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {prognostico}\n💥 Prognóstico: {prognostico}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario}"
            st.session_state[f"mid_{nome}"] = telegram(msg)

        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            base = f"🚨 Alerta de Entrada 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {prognostico}\n💥 Prognóstico: {prognostico}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario}"
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key=f"htg_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\n✅✅✅ GREEN ✅✅✅", mid)
            if c2.button("🏆 FINAL", key=f"fng_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            if c2.button("❌ RED", key=f"red_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n❌❌❌ RED ❌❌❌", mid)

# --- JOGO C MANTIDO COMO ESTAVA ORIGINALMENTE ---
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
        st.write("### 📊 Gráfico de Escanteios FT")
        st.bar_chart(pd.DataFrame({'Probabilidade': [90, 75, 50, 25]}, index=["O 7.5", "O 8.5", "O 9.5", "O 10.5"]))
        linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5], key="linha_c")
        if st.button("🚀 ENVIAR ALERTA ESCANTEIO", key="env_c"):
            st.session_state["mid_c"] = telegram(f"🚨 Escanteio: {linha}")

col1, col2, col3 = st.columns(3)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_c_escanteios()
