if st.button("🚀 ENVIAR PARA TELEGRAM", key=f"en_{titulo}"):
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
            if res.get("ok"):
                try:
                    # Garantir que o message_id seja tratado como inteiro e não como string
                    dados_sinal = {
                        "message_id": int(res["result"]["message_id"]),
                        "bloco": str(titulo),
                        "msg_original": str(msg),
                        "status": "ativa"
                    }
                    supabase.table("sinais").insert(dados_sinal).execute()
                    st.success("Enviado e salvo no banco!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar no banco: {e}")
