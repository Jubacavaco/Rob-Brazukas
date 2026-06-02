import streamlit as st
import requests
import re

st.set_page_config(layout="wide", page_title="Sistema Brazukas 4 Jogos")
st.title("🤖 Sistema Brazukas Top Tips (4 Jogos)")

TOKEN = st.secrets.get("token", "")
CHAT_ID = st.secrets.get("chat_id", "")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\b\d+\b', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    
    over15, over25, btts, ltd = 0, 0, 0, 0
    v_casa, v_vis, empate, total = 0, 0, 0, 0
    
    i = 0
    while i < len(gols) - 1:
        g1, g2 = gols[i], gols[i+1]
        total += 1
        if (g1 + g2) >= 2: over15 += 1
        if (g1 + g2) >= 3: over25 += 1
        if g1 > 0 and g2 > 0: btts += 1
        if g1 != g2: ltd += 1
        if g1 > g2: v_casa += 1
        elif g2 > g1: v_vis += 1
        else: empate += 1
        i += 2

    if total == 0: return 50, 50, 0, 0, 0, 0, 0
    
    # Cálculos
    pc, pv, pe = (v_casa/total)*100, (v_vis/total)*100, (empate/total)*100
    p15 = min((over15/total)*100 + 5, 95)
    p25 = min((over25/total)*100 + 5, 90)
    pb = min((btts/total)*100, 85)
    pl = min((ltd/total)*100, 95)
    
    return round(pc, 1), round(pv, 1), round(pe, 1), round(p15, 1), round(p25, 1), round(pb, 1), round(pl, 1)

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    hora = st.text_input("Horário", key=f"h_{titulo}")
    lista = st.text_area("Lista de jogos", key=f"l_{titulo}")

    if st.button("Analisar", key=f"an_{titulo}"):
        st.session_state[f"res_{titulo}"] = calcular_probabilidade(lista)
        st.rerun()

    if f"res_{titulo}" in st.session_state:
        pc, pv, pe, p15, p25, pb, pl = st.session_state[f"res_{titulo}"]
        
        # Gráficos de Barra
        st.write("### 📊 Estatísticas")
        st.progress(p25/100, text=f"Over 2.5: {p25}%")
        st.progress(p15/100, text=f"Over 1.5: {p15}%")
        st.progress(pb/100, text=f"BTTS: {pb}%")
        st.progress(pl/100, text=f"LTD: {pl}%")
        
        # Resumo Final
        st.markdown(f"""
        | Resultado | Prob. |
        |---|---|
        | Casa | {pc}% |
        | Empate | {pe}% |
        | Vis. | {pv}% |
        """)
        
        # Botão Enviar
        if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
            msg = f"🚨 *Alerta de Entrada*\n🏆 {camp}\n🆚 {casa} x {vis}\n📈 O2.5: {p25}% | BTTS: {pb}%"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg})
            st.success("Enviado!")

# Interface
c1, c2, c3, c4 = st.columns(4)
with c1: renderizar_bloco("JOGO_A")
with c2: renderizar_bloco("JOGO_B")
with c3: renderizar_bloco("JOGO_C")
with c4: renderizar_bloco("JOGO_D")
