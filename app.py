def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input(f"Campeonato ({titulo})", key=f"c_{titulo}")
    casa = st.text_input(f"Casa ({titulo})", key=f"ca_{titulo}")
    vis = st.text_input(f"Visitante ({titulo})", key=f"v_{titulo}")
    hora = st.text_input(f"Horário ({titulo})", key=f"h_{titulo}")
    lista = st.text_area(f"Lista de jogos ({titulo})", key=f"l_{titulo}")
    
    # Botão de análise
    if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
        p = calcular_probabilidade(lista)
        st.session_state[f"prob_{titulo}"] = p
    
    # Exibe dados se a análise existir
    if f"prob_{titulo}" in st.session_state:
        p = st.session_state[f"prob_{titulo}"]
        st.write(f"📈 **Probabilidade:** {p:.1f}%")
        
        # Gráficos
        st.write("📊 **Monitor de Mercados:**")
        st.progress(min((p+5)/100, 1.0)); st.write(f"Over 1.5 FT ({min(p+5, 100)}%)")
        st.progress(min(p/100, 1.0)); st.write(f"Over 2.5 FT ({min(p, 100)}%)")
        
        # Seletor de mercado manual
        opcao = st.selectbox(f"Escolha o Mercado ({titulo})", 
                            ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], 
                            key=f"sel_{titulo}")
        
        # Lógica de definição do mercado
        if opcao == "Automático":
            tipo = "LTD" if p >= 51 else None
            if p >= 55: tipo = "Ambas Marcam (BTTS)"
            if p >= 65: tipo = "Over 2.5 FT"
            if p >= 70: tipo = "Over 1.5 FT"
        else:
            tipo = opcao
            
        if tipo:
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n⏰ *Horário:* {hora}\n\n⚠️ Aposte com responsabilidade."
            st.info(msg)
            st.session_state[f"msg_{titulo}"] = msg

    # Botão Enviar
    if f"msg_{titulo}" in st.session_state:
        if st.button(f"🚀 Enviar {titulo}", key=f"en_{titulo}"):
            payload = {"chat_id": chat_id, "text": st.session_state[f"msg_{titulo}"], "parse_mode": "Markdown"}
            r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
            if r.get("ok"): 
                st.session_state[f"id_{titulo}"] = r["result"]["message_id"]
                st.rerun()
    
    # ... (restante do código de botões de controle igual ao anterior)
