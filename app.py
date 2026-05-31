# Botão de Envio
        if not st.session_state.msg_id:
            if st.button("🚀 Enviar Sinal"):
                if not token or not chat_id:
                    st.error("Preencha o Token e o ID do Canal na barra lateral!")
                else:
                    # Tenta enviar e captura o erro
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    params = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
                    
                    try:
                        resp = requests.get(url, params=params)
                        data = resp.json()
                        
                        if data.get("ok"):
                            st.session_state.msg_id = data["result"]["message_id"]
                            st.success("Sinal enviado com sucesso!")
                        else:
                            # AQUI VAI APARECER O ERRO DO TELEGRAM NA TELA
                            st.error(f"Erro do Telegram: {data.get('description')}")
                            st.write("Verifique se o Bot é Administrador do Canal.")
                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")
