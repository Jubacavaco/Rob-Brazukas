# --- JOGO C (MENSAGEM AJUSTADA) ---
def jogo_c_escanteios():
    st.subheader("🏟️ JOGO_C (Escanteios)")
    camp_c = st.text_input("Campeonato", key="camp_c")
    casa_c = st.text_input("Casa", key="casa_c")
    vis_c = st.text_input("Visitante", key="vis_c")
    horario_c = st.text_input("Horário", key="hor_c")
    med_total = st.number_input("Média Escanteios (Casa+Vis)", step=0.1, key="med_total_c")
    med_liga = st.number_input("Média Escanteios Liga", step=0.1, key="med_liga_c")
    e_casa_c = st.number_input("Escanteios Casa (Atual)", step=1, key="e_casa_c")
    e_vis_c = st.number_input("Escanteios Vis (Atual)", step=1, key="e_vis_c")
    ht_c = st.text_input("Placar HT", key="ht_c")
    ft_c = st.text_input("Placar FT", key="ft_c")
    
    if st.button("📊 ANALISAR JOGO C", key="ana_c"): st.session_state["analise_c"] = True
    
    if st.session_state.get("analise_c", False):
        st.write("### 📊 Probabilidade Escanteios")
        st.bar_chart(pd.DataFrame({'Probabilidade': [90, 75, 50, 25]}, index=["O 7.5", "O 8.5", "O 9.5", "O 10.5"]))
        
        linha = st.selectbox("Linha Escolhida", [7.5, 8.5, 9.5, 10.5], key="linha_c")
        
        if st.button("🚀 ENVIAR ALERTA ESCANTEIO", key="env_c"):
            msg = f"🚨 Alerta Escanteio 🚨\n\n🏆 {camp_c}\n⏰ {horario_c}\n\n📊 Escanteios Casa: {e_casa_c}\n📊 Escanteios Vis: {e_vis_c}\n📈 Total: {e_casa_c + e_vis_c}\n🎯 Linha: {linha}"
            st.session_state["mid_c"] = telegram(msg)
        
        mid = st.session_state.get("mid_c")
        if mid:
            base = f"🚨 Alerta Escanteio 🚨\n\n🏆 {camp_c}\n⏰ {horario_c}\n\n📊 Escanteios Casa: {e_casa_c}\n📊 Escanteios Vis: {e_vis_c}\n📈 Total: {e_casa_c + e_vis_c}\n🎯 Linha: {linha}"
            c1, c2 = st.columns(2)
            
            # Botões Momento e HT (Sem FT)
            if c1.button("⚪ MOMENTO", key="c_mom"): telegram(f"{base}\n\nPlacar HT: {ht_c}\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key="c_ht"): telegram(f"{base}\n\nPlacar HT: {ht_c}\n✅✅✅ GREEN ✅✅✅", mid)
            
            # Botões Final e Red (Com FT)
            if c2.button("🏆 FINAL", key="c_fin"): telegram(f"{base}\n\nPlacar HT: {ht_c}\nPlacar FT: {ft_c}\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            if c2.button("❌ RED", key=f"c_red"): telegram(f"{base}\n\nPlacar HT: {ht_c}\nPlacar FT: {ft_c}\n❌❌❌ RED ❌❌❌", mid)
