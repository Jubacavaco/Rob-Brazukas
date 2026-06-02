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

# Lógica de cálculo baseada na lista de entrada
def calcular_metricas_reais(lista_texto):
    lista_texto = lista_texto.lower()
    scores = {"Over 1.5 FT": 50, "Over 2.5 FT": 50, "BTTS": 50, "LTD": 50, "Casa Vence": 50, "Visitante Vence": 50}
    
    if "gol" in lista_texto or "over 1" in lista_texto: scores["Over 1.5 FT"] += 35
    if "2.5" in lista_texto: scores["Over 2.5 FT"] += 40
    if "ambas" in lista_texto or "btts" in lista_texto: scores["BTTS"] += 45
    if "favorito" in lista_texto or "ltd" in lista_texto: scores["LTD"] += 30
    if "casa" in lista_texto: scores["Casa Vence"] += 30
    if "fora" in lista_texto or "visitante" in lista_texto: scores["Visitante Vence"] += 30
    
    return pd.DataFrame(list(scores.values()), index=scores.keys(), columns=['%'])

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    mercado = st.selectbox("Mercado", ["Match Odds", "Gols"], key=f"merc_{nome}")
    prognostico = st.multiselect("Prognóstico", ["Over 1.5 FT", "Over 2.5 FT", "BTTS", "LTD", "Casa Vence", "Visitante Vence"], key=f"prog_{nome}")
    prog_str = ", ".join(prognostico)
    horario = st.text_input("Horário", key=f"hor_{nome}")
    prob = st.number_input("Probabilidade (%)", 0, 100, 70, key=f"prob_{nome}")
    ht = st.text_input("Placar HT", key=f"ht_{nome}")
    ft = st.text_input("Placar FT", key=f"ft_{nome}")
    lista = st.text_area("Lista de Análise", key=f"lista_{nome}")
    
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"analise_{nome}"] = True

    if st.session_state.get(f"analise_{nome}", False):
        st.write("### 📊 Análise de Probabilidade")
        df = calcular_metricas_reais(lista)
        
        # Lista vertical de mercados e probabilidades
        for mercado_nome, row in df.iterrows():
            st.write(f"**{mercado_nome}:** {row['%']}%")
        
        melhor_mercado = df['%'].idxmax()
        
        st.write("---")
        st.write(f"### 📌 Aposta Sugerida")
        st.success(f"🎯 Mercado Mais Forte: {melhor_mercado} ({df.loc[melhor_mercado].values[0]}%)")

        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"🚨 Alerta de Entrada 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 Mercado: {mercado}\n💥 Prog: {prog_str}\n📈 Prob: {prob}%\n⏰ {horario}"
            st.session_state[f"mid_{nome}"] = telegram(msg)

        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            base = f"🚨 Alerta de Entrada 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {mercado}\n💥 {prog_str}\n📈 {prob}%\n⏰ {horario}"
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key=f"htg_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\n✅✅✅ GREEN ✅✅✅", mid)
            if c2.button("🏆 FINAL", key=f"fng_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            if c2.button("❌ RED", key=f"red_{nome}"): telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n❌❌❌ RED ❌❌❌", mid)

# Função Jogo C (Escanteios - Mantida intacta)
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
    e_casa_atual = st.number_input("Cantos Casa (Atual)", step=1, format="%d", key="e_casa_c")
    e_vis_atual = st.number_input("Cantos Fora (Atual)", step=1, format="%d", key="e_vis_c")
    total_esc = int(e_casa_atual + e_vis_atual)
    
    if st.button("📊 ANALISAR JOGO C", key="ana_c"):
        st.session_state["analise_c"] = True

    if st.session_state.get("analise_c", False):
        st.write("### 📊 Gráfico de Escanteios FT")
        st.bar_chart(pd.DataFrame({'Probabilidade': [90, 75, 50, 25]}, index=["O 7.5", "O 8.5", "O 9.5", "O 10.5"]))
        
        linha = st.selectbox("Linha Escolhida", [7.5, 8.5, 9.5, 10.5], key="linha_c")
        conf = st.slider("Porcentagem de Confiança", 0, 100, 70, key="conf_c")
        
        if st.button("🚀 ENVIAR ALERTA ESCANTEIO", key="env_c"):
            msg = f"🚨 Alerta de Entrada 🚨\n\n🏆 {camp_c}\n🆚 {casa_c} x {vis_c}\n🎯 Linha: {linha} FT\n📈 Confiança: {conf}%"
            st.session_state["mid_c"] = telegram(msg)

        mid = st.session_state.get("mid_c")
        if mid:
            base = (f"🚨 Alerta de Entrada 🚨\n\n🏆 {camp_c}\n🆚 {casa_c} x {vis_c}\n🎯 Linha: {linha} FT\n\n"
                    f"Cantos Casa: {int(e_casa_atual)}\n"
                    f"Cantos Visitante: {int(e_vis_atual)}\n"
                    f"Total: {total_esc}")
            c1, c2 = st.columns(2)
            if c1.button("⚪ MOMENTO", key="c_mom"): telegram(f"{base}\n\nPlacar HT: {ht_c}\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key="c_ht"): telegram(f"{base}\n\nPlacar HT: {ht_c}\n✅✅✅ GREEN ✅✅✅", mid)
            if c2.button("🏆 FINAL", key="c_fin"): telegram(f"{base}\n\nPlacar HT: {ht_c}\nPlacar FT: {ft_c}\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            if c2.button("❌ RED", key="c_red"): telegram(f"{base}\n\nPlacar HT: {ht_c}\nPlacar FT: {ft_c}\n❌❌❌ RED ❌❌❌", mid)

col1, col2, col3 = st.columns(3)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_c_escanteios()
