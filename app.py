# --- Adicione isto no topo do seu script, logo após o TOKEN/CHAT_ID ---
def enviar_ou_editar(nome, msg):
    # Se já enviamos uma mensagem para este jogo, editamos ela
    if f"msg_id_{nome}" in st.session_state:
        msg_id = st.session_state[f"msg_id_{nome}"]
        url = f"https://api.telegram.org/bot{TOKEN}/editMessageText"
        requests.post(url, json={"chat_id": CHAT_ID, "message_id": msg_id, "text": msg})
    else:
        # Se é a primeira vez, enviamos e salvamos o ID
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json={"chat_id": CHAT_ID, "text": msg}).json()
        if resp.get("ok"):
            st.session_state[f"msg_id_{nome}"] = resp["result"]["message_id"]

# --- Substitua a parte do botão de envio no 'jogo_normal' por isto ---

    if btn_enviar:
        d = st.session_state[f"dados_{nome}"]
        msg = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {d['camp']}\n🆚 Jogo: {d['casa']} x {d['vis']}\n🎯 Mercado: {mercado_envio}\n⏰ Horário: {d['horario']} (BR)"
        enviar_ou_editar(nome, msg)
        st.success("Enviado!")

    # NOVOS BOTÕES DE AÇÃO (Edição)
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        if st.button("MOMENTO", key=f"mom_{nome}"):
            d = st.session_state.get(f"dados_{nome}", {"casa": "...", "vis": "..."})
            msg = f"⏱️ MOMENTO AO VIVO\n{d['casa']} x {d['vis']}\nPlacar HT: {ht} | FT: {ft}"
            enviar_ou_editar(nome, msg)
            
        if st.button("HT GREEN ✅", key=f"htg_{nome}"):
            msg = f"✅ HT GREEN! Placar: {ht}"
            enviar_ou_editar(nome, msg)
            
    with col_a2:
        if st.button("FINAL GREEN ✅", key=f"fng_{nome}"):
            msg = f"🏆 FINAL GREEN! Placar: {ft}"
            enviar_ou_editar(nome, msg)
            
        if st.button("RED ❌", key=f"red_{nome}"):
            msg = f"❌ RED! Placar Final: {ft}"
            enviar_ou_editar(nome, msg)
