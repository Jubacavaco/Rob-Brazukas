if st.button("🚀 ENVIAR PARA TELEGRAM", key=f"en_{titulo}"):
            if not TOKEN:
                st.error("TOKEN não configurado!")
            elif not CHAT_ID:
                st.error("CHAT_ID não configurado!")
            else:
                # Monta a URL completa para depuração
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                payload = {"chat_id": CHAT_ID, "text": msg}
                
                try:
                    res = requests.post(url, data=payload)
                    resultado = res.json()
                    
                    if resultado.get("ok"):
                        st.session_state[f"id_{titulo}"] = resultado["result"]["message_id"]
                        st.session_state[f"msg_{titulo}"] = msg
                        st.success("Enviado com sucesso!")
                    else:
                        # Exibe o erro exato do Telegram
                        st.error(f"Erro Telegram: {resultado.get('description')}")
                        st.write(f"URL testada: {url.replace(TOKEN, '***TOKEN_OCULTO***')}")
                except Exception as e:
                    st.error(f"Erro de conexão: {str(e)}")
