if btn_enviar:
        probs = st.session_state.get(f"probs_{nome}", {"Erro": 0})
        prob_val = probs.get(mercado, 0)
        status = "🔥 MERCADO PEGANDO FOGO" if prob_val >= 70 else "⚠️ Mercado estável"
        
        # Modelo de mensagem solicitado
        msg = f"""🚨 Alerta de Cantos 🚨

🏆 Campeonato: [INSERIR CAMPEONATO]
🆚 Jogo: {casa} x {visitante}
🎯 Mercado: {mercado}
💥 Prognóstico: {status}
📈 Probabilidade: {prob_val}%
⏰ Horário: {horario} (BR)

🔞 Aposte com responsabilidade.
⚠️ Não há garantias de lucro."""
        
        enviar_telegram(msg)
        st.success("Enviado com sucesso!")
