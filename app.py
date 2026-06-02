# --- JOGO C AJUSTADO ---
def jogo_c_escanteios():
    st.subheader("🏟️ JOGO_C (Escanteios)")
    camp_c = st.text_input("Campeonato", key="camp_c")
    casa_c = st.text_input("Casa", key="casa_c")
    vis_c = st.text_input("Visitante", key="vis_c")
    horario_c = st.text_input("Horário", key="hor_c")
    
    # Médias
    med_total = st.number_input("Média Escanteios (Casa+Vis)", step=0.1, key="med_total_c")
    med_liga = st.number_input("Média Escanteios Liga", step=0.1, key="med_liga_c")
    
    # Escanteios Atuais
    e_casa_atual = st.number_input("Escanteios Casa (Atual)", step=1, key="e_casa_c")
    e_vis_atual = st.number_input("Escanteios Visitante (Atual)", step=1, key="e_vis_c")
    e_total_atual = e_casa_atual + e_vis_atual
    
    st.write(f"**Total de Escanteios Atual:** {e_total_atual}")
    
    ht_c = st.text_input("Placar HT", key="ht_c")
    ft_c = st.text_input("Placar FT", key="ft_c")
    
    if st.button("📊 ANALISAR JOGO C", key="ana_c"): st.session_state["analise_c"] = True
    
    if st.session_state.get("analise_c", False):
        linha = st.selectbox("Linha Escolhida", [7.5, 8.5, 9.5, 10.5], key="linha_c")
        
        if st.button("🚀 ENVIAR ALERTA ESCANTEIO", key="env_c"):
            msg = (f"🚨 Alerta Escanteio 🚨\n\n🏆 {camp_c}\n🆚 {casa_c} x {vis_c}\n⏰ {horario_c}\n\n"
                   f"📊 Escanteios Casa: {e_casa_atual}\n📊 Escanteios Vis: {e_vis_atual}\n"
                   f"📈 Total Atual: {e_total_atual}\n🎯 Linha: {linha}")
            st.session_state["mid_c"] = telegram(msg)
        
        mid = st.session_state.get("mid_c")
        if mid:
            base = (f"🚨 Alerta Escanteio 🚨\n\n🏆 {camp_c}\n🆚 {casa_c} x {vis_c}\n⏰ {horario_c}\n\n"
                    f"📊 Casa: {e_casa_atual} | Vis: {e_vis_atual} | Total: {e_total_atual}\n🎯 Linha: {linha}")
            c1, c2 = st.columns(2)
            if c1.button("⚪ MOMENTO", key="c_mom"): telegram(f"{base}\n\nPlacar HT: {ht_c}\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key="c_ht"): telegram(f"{base}\n\nPlacar HT: {ht_c}\n✅✅✅ GREEN ✅✅✅", mid)
            if c2.button("🏆 FINAL", key="c_fin"): telegram(f"{base}\n\nPlacar HT: {ht_c}\nPlacar FT: {ft_c}\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            if c2.button("❌ RED", key="c_red"): telegram(f"{base}\n\nPlacar HT: {ht_c}\nPlacar FT: {ft_c}\n❌❌❌ RED ❌❌❌", mid)
