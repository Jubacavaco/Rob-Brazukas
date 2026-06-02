import streamlit as st
import requests
import pandas as pd
import re

# ... (Mantendo as funções de Config e Telegram intactas)

def calcular_metricas_reais(lista_texto):
    """
    Lógica de cálculo: Analisa a frequência de termos e números no texto 
    para gerar probabilidades dinâmicas.
    """
    lista_texto = lista_texto.lower()
    
    # Extração de números do texto (ex: se o usuário digitar "3 gols", "80% de chance")
    numeros = re.findall(r'\d+', lista_texto)
    fator = int(numeros[0]) if numeros else 10 
    
    # Base de cálculo inicial diferente para cada mercado
    scores = {
        "Over 1.5 FT": 40 + (fator if "gol" in lista_texto else 0),
        "Over 2.5 FT": 30 + (fator if "over" in lista_texto else 0),
        "BTTS": 35 + (fator if "ambas" in lista_texto else 0),
        "LTD": 20 + (fator if "ltd" in lista_texto else 0),
        "Casa Vence": 45 + (fator if "casa" in lista_texto else 0),
        "Visitante Vence": 45 + (fator if "fora" in lista_texto else 0)
    }
    
    # Normalização para não passar de 99%
    for k in scores:
        scores[k] = min(99, max(10, scores[k]))
        
    return pd.DataFrame(list(scores.values()), index=scores.keys(), columns=['%'])

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    # ... (Inputs permanecem exatamente como antes)
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
        st.write("### 📊 Probabilidades Calculadas")
        df = calcular_metricas_reais(lista)
        
        # Exibição vertical limpa
        for mercado_nome, row in df.iterrows():
            st.write(f"**{mercado_nome}:** {row['%']}%")
        
        melhor_mercado = df['%'].idxmax()
        
        st.write("---")
        st.success(f"🎯 Mercado Mais Forte: {melhor_mercado} ({df.loc[melhor_mercado].values[0]}%)")

        # ... (Botões de Envio e Alertas permanecem intactos)
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

# ... (Mantém o Jogo C exatamente como estava antes)
