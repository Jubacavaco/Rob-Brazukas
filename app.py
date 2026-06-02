import streamlit as st
import requests
import re

st.set_page_config(layout="wide", page_title="Sistema Brazukas")

# --- Função de Cálculo Corrigida (Sempre retorna 4 valores) ---
def calcular_probabilidade(texto):
    numeros = re.findall(r'\b\d+\b', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    v_casa = v_vis = empate = total = over_gols = 0
    
    i = 0
    while i < len(gols) - 1:
        total += 1
        if (gols[i] + gols[i+1]) >= 3: over_gols += 1
        if gols[i] > gols[i+1]: v_casa += 1
        elif gols[i+1] > gols[i]: v_vis += 1
        else: empate += 1
        i += 2
        
    if total == 0: return 33.3, 33.3, 33.3, 50.0
    
    pc = (v_casa / total) * 100
    pv = (v_vis / total) * 100
    pe = (empate / total) * 100
    pg = (over_gols / total) * 100
    return round(pc, 1), round(pv, 1), round(pe, 1), round(pg, 1)

# --- Função de Renderização ---
def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    casa = st.text_input("Casa", key=f"casa_{titulo}")
    vis = st.text_input("Visitante", key=f"vis_{titulo}")
    lista = st.text_area("Lista de jogos", key=f"lista_{titulo}")

    if st.button("Analisar", key=f"btn_{titulo}"):
        pc, pv, pe, pg = calcular_probabilidade(lista)
        st.session_state[f"probs_{titulo}"] = (pc, pv, pe, pg)
        st.rerun()

    if f"probs_{titulo}" in st.session_state:
        pc, pv, pe, pg = st.session_state[f"probs_{titulo}"]
        
        st.write("📊 **Análise de Gols:**")
        # Proteção para garantir que o valor do gráfico esteja entre 0 e 1
        st.progress(max(min(pg/100, 1.0), 0.0), text=f"Over 2.5: {pg}%")
        
        st.write("🏆 **Match Odds:**")
        st.progress(max(min(pc/100, 1.0), 0.0), text=f"Casa: {pc}%")
        st.progress(max(min(pv/100, 1.0), 0.0), text=f"Visitante: {pv}%")

# Layout
col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
