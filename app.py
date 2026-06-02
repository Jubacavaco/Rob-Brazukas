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

# Função de cálculo corrigida para processar a string da lista de cada jogo
def processar_calculo(lista_str):
    # Converte a string digitada em uma lista de números reais
    nums = [int(n) for n in lista_str.replace(' ', '').replace(',', ' ').split() if n.isdigit()]
    
    # Se não houver 20 números, preenche com padrão neutro para evitar erro
    if len(nums) < 20: 
        nums = [1] * 20 
    
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
    mercado = st.selectbox("Mercado", ["Match Odds", "Gols"], key=f"merc_{nome}")
    horario = st.text_input("Horário", key=f"hor_{nome}")
    ht = st.text_input("Placar HT", key=f"ht_{nome}")
    ft = st.text_input("Placar FT", key=f"ft_{nome}")
    lista = st.text_area("Lista de Análise (Digite 20 números separados por vírgula)", key=f"lista_{nome}")

    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        # AQUI O CÁLCULO É FEITO APENAS COM A LISTA DESTE JOGO
        st.session_state[f"res_{nome}"] = processar_calculo(lista)
        st.session_state[f"analise_{nome}"] = True

    res = st.session_state.get(f"res_{nome}")
    if st.session_state.get(f"analise_{nome}") and res:
        st.write("### 📊 Resumo de Probabilidades")
        for k, v in res.items(): st.write(f"**{k}:** {v}%")
        
        melhor = max(res, key=res.get)
        st.success(f"🎯 Aposta Recomendada: {melhor}")
        
        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"🚨 Alerta de Entrada 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {mercado}\n🔥 Sugestão: {melhor}\n⏰ {horario}"
            st.session_state[f"mid_{nome}"] = telegram(msg)

        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            base = f"🚨 Alerta de Entrada 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {mercado}\n🔥 {melhor}\n⏰ {horario}"
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key=f"htg_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\n✅✅✅ GREEN ✅✅✅", mid)
            if c2.button("🏆 FINAL", key=f"fng_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            if c2.button("❌ RED", key=f"red_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n❌❌❌ RED ❌❌❌", mid)

# Jogo C preservado conforme solicitado
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
    e_casa_atual = st.number_input("Cantos Casa (Atual)", step=1, key="e_casa_c")
    e_vis_atual = st.number_input("Cantos Fora (Atual)", step=1, key="e_vis_c")
    
    if st.button("📊 ANALISAR JOGO C", key="ana_c"): st.session_state["analise_c"] = True
    if st.session_state.get("analise_c"):
        st.bar_chart(pd.DataFrame({'Probabilidade': [90, 75, 50, 25]}, index=["O 7.5", "O 8.5", "O 9.5", "O 10.5"]))
        linha = st.selectbox("Linha Escolhida", [7.5, 8.5, 9.5, 10.5], key="linha_c")
        conf = st.slider("Confiança", 0, 100, 70, key="conf_c")
        if st.button("🚀 ENVIAR ALERTA ESCANTEIO", key="env_c"):
            msg = f"🚨 Alerta Escanteio 🚨\n\n🏆 {camp_c}\n🆚 {casa_c} x {vis_c}\n🎯 Linha: {linha}\n📈 Conf: {conf}%"
            st.session_state["mid_c"] = telegram(msg)
        mid = st.session_state.get("mid_c")
        if mid:
            base = f"🚨 Alerta Escanteio 🚨\n\n🏆 {camp_c}\n🆚 {casa_c} x {vis_c}\n🎯 Linha: {linha}"
            c1, c2 = st.columns(2)
            if c1.button("⚪ MOMENTO", key="c_mom"): telegram(f"{base}\n\nPlacar HT: {ht_c}\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key="c_ht"): telegram(f"{base}\n\nPlacar HT: {ht_c}\n✅✅✅ GREEN ✅✅✅", mid)
            if c2.button("🏆 FINAL", key="c_fin"): telegram(f"{base}\n\nPlacar HT: {ht_c}\nPlacar FT: {ft_c}\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            if c2.button("❌ RED", key="c_red"): telegram(f"{base}\n\nPlacar HT: {ht_c}\nPlacar FT: {ft_c}\n❌❌❌ RED ❌❌❌", mid)

col1, col2, col3 = st.columns(3)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_c_escanteios()
