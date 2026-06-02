def atualizar(status, modo):
            msg_id = st.session_state[f"id_{titulo}"]
            msg_base = st.session_state[f"msg_base_{titulo}"]
            
            if modo == 'MOMENTO':
                placar_txt = f"Momento: {pm}"
            elif modo == 'HT':
                placar_txt = f"HT: {pht}"
            else:
                placar_txt = f"HT: {pht}\nFinal: {pf}"
                
            txt = f"{msg_base}\n\n⚽ {placar_txt}\n\n🔄 STATUS: {status}"
            
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/editMessageText", 
                data={"chat_id": CHAT_ID, "message_id": msg_id, "text": txt}
            )
            st.success(f"Atualizado: {status}")
