# 1. Função de envio com limpeza automática em caso de erro
def enviar_ou_editar(nome, msg):
    url_base = f"https://api.telegram.org/bot{TOKEN}"
    payload = {"chat_id": CHAT_ID, "text": msg}
    
    # Tenta editar se tiver ID salvo
    if f"msg_id_{nome}" in st.session_state:
        payload["message_id"] = st.session_state[f"msg_id_{nome}"]
        resp = requests.post(f"{url_base}/editMessageText", json=payload).json()
        
        # Se a edição falhar (ex: mensagem foi apagada no Telegram), reseta o ID
        if not resp.get("ok"):
            del st.session_state[f"msg_id_{nome}"]
            enviar_ou_editar(nome, msg) # Tenta enviar do zero
    else:
        # Envia nova
        resp = requests.post(f"{url_base}/sendMessage", json=payload).json()
        if resp.get("ok"):
            st.session_state[f"msg_id_{nome}"] = resp["result"]["message_id"]
        else:
            st.error(f"Erro ao enviar: {resp.get('description')}")

# 2. Bloco do botão ENVIAR ALERTA dentro da função jogo_normal
    if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
        if f"dados_{nome}" in st.session_state:
            d = st.session_state[f"dados_{nome}"]
            msg = f"""🚨 Alerta de Cantos 🚨

🏆 Campeonato: {d['camp']}
🆚 Jogo: {d['casa']} x {d['vis']}
🎯 Mercado: {d['merc']}
💥 Prognóstico: Analisado
📈 Probabilidade: {d['prob']}%
⏰ Horário: {d['horario']} (BR)

🔞 Aposte com responsabilidade.
⚠️ Não há garantias de lucro."""
            enviar_ou_editar(nome, msg)
            st.success("Enviado com sucesso!")
        else:
            st.warning("Analise o jogo antes de enviar!")
