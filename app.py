def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    
    # 1. Formulário para entrada de dados
    with st.form(key=f"form_{nome}"):
        camp = st.text_input("Campeonato", key=f"camp_{nome}")
        casa = st.text_input("Casa", key=f"casa_{nome}")
        visitante = st.text_input("Visitante", key=f"vis_{nome}")
        horario = st.text_input("Horário", key=f"hor_{nome}")
        ht = st.text_input("Placar HT", key=f"ht_in_{nome}")
        ft = st.text_input("Placar FT", key=f"ft_in_{nome}")
        
        lista = st.text_area("Lista de Jogos", key=f"lista_{nome}")
        mercado_envio = st.selectbox("Mercado", ["BTTS", "O1.5", "O2.5", "LTD", "Casa", "Vis"], key=f"merc_{nome}")
        prob_manual = st.number_input("% Probabilidade", 0, 100, 70, key=f"prob_{nome}")
        
        btn_analisar = st.form_submit_button("📊 ANALISAR")
        btn_enviar = st.form_submit_button("🚀 ENVIAR ALERTA")

    # 2. Lógica de Análise
    if btn_analisar:
        st.session_state[f"probs_{nome}"] = calcular_probabilidades(lista, nome)
        st.session_state[f"dados_{nome}"] = {"camp": camp, "casa": casa, "vis": visitante, "horario": horario, "ht": ht, "ft": ft}
        st.rerun()

    # 3. Se houver dados, mostrar botões de ação e gráfico
    if f"dados_{nome}" in st.session_state:
        d = st.session_state[f"dados_{nome}"]
        
        # Exibição do gráfico e métricas (mantendo o que já funcionava)
        if f"probs_{nome}" in st.session_state:
            renderizar_grafico(st.session_state[f"probs_{nome}"])

        # BOTÕES DE AÇÃO (Agora com acesso aos dados salvos na sessão)
        st.write("---")
        col_a1, col_a2 = st.columns(2)
        
        with col_a1:
            if st.button("⏱️ MOMENTO", key=f"mom_{nome}"):
                msg = f"⏱️ MOMENTO AO VIVO\n{d['casa']} x {d['vis']}\nPlacar: HT {d['ht']} | FT {d['ft']}"
                enviar_ou_editar(nome, msg)
            if st.button("✅ HT GREEN", key=f"htg_{nome}"):
                msg = f"✅ HT GREEN!\n{d['casa']} x {d['vis']}\nPlacar HT: {d['ht']}"
                enviar_ou_editar(nome, msg)
        
        with col_a2:
            if st.button("✅ FINAL GREEN", key=f"fng_{nome}"):
                msg = f"🏆 FINAL GREEN!\n{d['casa']} x {d['vis']}\nPlacar Final: {d['ft']}"
                enviar_ou_editar(nome, msg)
            if st.button("❌ RED", key=f"red_{nome}"):
                msg = f"❌ RED!\n{d['casa']} x {d['vis']}\nPlacar Final: {d['ft']}"
                enviar_ou_editar(nome, msg)

    # 4. Envio inicial
    if btn_enviar and f"dados_{nome}" in st.session_state:
        d = st.session_state[f"dados_{nome}"]
        msg = f"🚨 Alerta de Cantos 🚨\n\n🏆 {d['camp']}\n🆚 {d['casa']} x {d['vis']}\n🎯 {mercado_envio}\n📈 {prob_manual}%\n⏰ {d['horario']} (BR)"
        enviar_ou_editar(nome, msg)
        st.success("Enviado!")
