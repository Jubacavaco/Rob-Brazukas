if st.button("🚀 ENVIAR PARA TELEGRAM", key=f"en_{titulo}"):
            if not TOKEN or not CHAT_ID:
                st.error("TOKEN ou CHAT_ID não encontrados no arquivo de Secrets.")
            else:
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
                
                # Fazemos a requisição e capturamos a resposta
                r = requests.post(url, data=payload)
                resultado = r.json()
                
                if resultado.get("ok"):
                    st.session_state[f"id_{titulo}"] = resultado["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg
                    st.success("Enviado com sucesso!")
                else:
                    # ISSO VAI TE MOSTRAR O ERRO REAL
                    st.error(f"Erro do Telegram: {resultado.get('description', 'Erro desconhecido')}")
