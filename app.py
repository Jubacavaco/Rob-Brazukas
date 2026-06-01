# Edição de Status
        if f"id_{titulo}" in st.session_state:
            st.write("---")
            st.write("🔄 **Atualizar Status no Telegram:**")
            c1, c2, c3 = st.columns(3)
            
            def registrar(status):
                msg_id = st.session_state.get(f"id_{titulo}")
                url_edit = f"https://api.telegram.org/bot{TOKEN}/editMessageText"
                # Adiciona o status ao texto original
                novo_texto = st.session_state.get(f"msg_{titulo}") + f"\n\n🔄 *Status:* {status}"
                requests.post(url_edit, data={
                    "chat_id": CHAT_ID, 
                    "message_id": msg_id, 
                    "text": novo_texto, 
                    "parse_mode": "Markdown"
                })
                st.success(f"Atualizado para {status}!")

            if c1.button("✅ GREEN", key=f"g_{titulo}"): registrar("✅ GREEN!")
            if c2.button("❌ RED", key=f"r_{titulo}"): registrar("❌ RED!")
            if c3.button("🔄 DEV", key=f"d_{titulo}"): registrar("🔄 DEVOLVIDA")
