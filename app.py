def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    hora = st.text_input("Horário", key=f"h_{titulo}")
    prob_manual = st.text_input("Probabilidade Manual (%)", key=f"pr_{titulo}")
    pm = st.text_input("Placar Momento", key=f"pm_{titulo}")
    pht = st.text_input("Placar HT", key=f"pht_{titulo}")
    pf = st.text_input("Placar Final", key=f"pf_{titulo}")
    lista = st.text_area("Lista de jogos", key=f"l_{titulo}")

    if st.button("Analisar", key=f"an_{titulo}"):
        if lista:
            st.session_state[f"probs_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        else:
            st.warning("Cole a lista de jogos primeiro!")

    if f"probs_{titulo}" in st.session_state:
        pc, pv, pe, p15, p25, pbtts, pltd = st.session_state[f"probs_{titulo}"]
        sugestao = obter_sugestao(p15, p25, pbtts, pltd)
        if sugestao != "Nenhum mercado recomendado":
            st.success(f"🎯 Sugestão: {sugestao}")

        st.progress(min(max(p25/100, 0), 1), text=f"O2.5: {p25:.0f}%")
        st.progress(min(max(p15/100, 0), 1), text=f"O1.5: {p15:.0f}%")
        st.progress(min(max(pbtts/100, 0), 1), text=f"BTTS: {pbtts:.0f}%")
        st.progress(min(max(pltd/100, 0), 1), text=f"LTD: {pltd:.0f}%")
        
        tipo = st.selectbox("Mercado", [sugestao, "Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
        msg_base = f"🚨 Alerta de Entrada 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {tipo}\n📈 Probabilidade: {prob_manual}%\n⏰ Horário: {hora}\n\n⚠️ Aposte com responsabilidade."
        st.info(msg_base)

        if st.button("🚀 ENVIAR", key=f"en_{titulo}"):
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg_base}).json()
            if res.get("ok"):
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                st.session_state[f"msg_base_{titulo}"] = msg_base
                st.success("Mensagem enviada!")

    if f"id_{titulo}" in st.session_state:
        st.write("---")
        def atualizar(status, modo):
            msg_id = st.session_state[f"id_{titulo}"]
            txt = f"{st.session_state[f'msg_base_{titulo}']}\n\n⚽ {(f'Momento: {pm}' if modo=='MOMENTO' else (f'HT: {pht}' if modo=='HT' else f'HT: {pht}\nFinal: {pf}'))}\n\n🔄 STATUS: {status}"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": msg_id, "text": txt})
            st.success(f"Atualizado: {status}")

        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Momento", key=f"m_{titulo}"): atualizar("GREEN 🟢✅", "MOMENTO")
        if c2.button("HT", key=f"ht_{titulo}"): atualizar("EM ANDAMENTO ⚪", "HT")
        if c3.button("Final", key=f"f_{titulo}"): atualizar("GREEN 🟢✅", "FINAL")
        if c4.button("RED", key=f"r_{titulo}"): atualizar("RED 🔴❌", "FINAL")
