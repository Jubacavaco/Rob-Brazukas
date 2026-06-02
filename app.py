import streamlit as st
import requests

# Função de cálculo baseada na sua lista (exemplo)
def calcular_probabilidades(lista):
    # Lógica simples: o tamanho da lista e o conteúdo definem os valores
    tamanho = len(lista)
    return {
        "O 1.5": min(95, 50 + tamanho * 2),
        "O 2.5": min(95, 30 + tamanho * 3),
        "BTTS": min(95, 20 + tamanho * 4),
        "LTD": min(95, 40 + tamanho * 1),
        "CASA": 60,
        "VIS": 30
    }

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    mercado = st.selectbox("Mercado", ["Match Odds", "Gols"], key=f"merc_{nome}")
    horario = st.text_input("Horário", key=f"hor_{nome}")
    prob = st.number_input("Probabilidade (%)", 0, 100, 70, key=f"prob_{nome}")
    ht = st.text_input("Placar HT (ex: 0x0)", key=f"ht_{nome}")
    ft = st.text_input("Placar FT (ex: 1x2)", key=f"ft_{nome}")
    lista = st.text_area("Lista de Análise", key=f"lista_{nome}")
    
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"analise_{nome}"] = True
        st.session_state[f"probs_{nome}"] = calcular_probabilidades(lista)

    if st.session_state.get(f"analise_{nome}"):
        p = st.session_state[f"probs_{nome}"]
        
        # --- RESUMO FINAL E GRÁFICO ---
        st.write("### 📊 Resumo Final")
        st.bar_chart(p)

        st.markdown(f"| Mercado | Probabilidade |\n|---|---|\n| ✅ Over 1.5 FT | {p['O 1.5']}% |\n| ⚠️ Over 2.5 FT | {p['O 2.5']}% |\n| ⚠️ BTTS | {p['BTTS']}% |\n| 🔥 LTD | {p['LTD']}% |")

        # --- MERCADOS E PLACARES ---
        col_m, col_p = st.columns(2)
        with col_m:
            st.write("### 🎯 Mercados Fortes")
            if p['O 1.5'] >= 75: st.write("✅ Over 1.5 FT — Muito Forte")
        with col_p:
            st.write("### 📌 Placares Sugeridos")
            st.write(f"• 1x0 | 1x1")

        # --- ENVIO TELEGRAM ---
        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {mercado}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario}\n\n🔞Aposte com responsabilidade."
            st.session_state[f"mid_{nome}"] = telegram(msg)

        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            base = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n⏰ Horário: {horario}"
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"):
                telegram(f"{base}\nHT: ({ht})\n\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key=f"htg_{nome}"):
                telegram(f"{base}\nHT: ({ht})\n✅✅✅", mid)
            if c2.button("🏆 FINAL", key=f"fng_{nome}"):
                telegram(f"{base}\nHT: ({ht})\nFT: ({ft})\n🏆🏆🏆", mid)
            if c2.button("❌ RED", key=f"red_{nome}"):
                telegram(f"{base}\nHT: ({ht})\nFT: ({ft})\n❌❌❌", mid)
