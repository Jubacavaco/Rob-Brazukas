# No bloco de ENVIO (dentro da função renderizar_bloco)
        if st.button("🚀 ENVIAR", key=f"en_{titulo}"):
            try:
                payload = {"chat_id": CHAT_ID, "text": msg_base}
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=payload).json()
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg_base
                    st.success("Enviado com sucesso!")
                else:
                    st.error(f"Erro Telegram: {res.get('description')}")
            except Exception as e:
                st.error(f"Falha na conexão: {e}")

    # No bloco de ATUALIZAÇÃO (abaixo da função de renderizar_bloco)
    if f"id_{titulo}" in st.session_state:
        st.write("---")
        def at(status, placar):
            try:
                msg_id = st.session_state[f"id_{titulo}"]
                txt = f"{st.session_state[f'msg_{titulo}']}\n\n⚽ {placar}\n\n🔄 {status}"
                payload = {"chat_id": CHAT_ID, "message_id": msg_id, "text": txt}
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data=payload).json()
                if res.get("ok"):
                    st.success(f"Atualizado: {status}")
                else:
                    st.error(f"Erro edição: {res.get('description')}")
            except Exception as e:
                st.error(f"Erro ao atualizar: {e}")
