# =============================
# BLOCO JOGO A/B/C (AJUSTADO)
# =============================
def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")

    with st.form(key=nome):
        casa = st.text_input("Casa")
        visitante = st.text_input("Visitante")
        horario = st.text_input("Horário")
        
        ht = st.text_input("Placar HT")
        ft = st.text_input("Placar FT")
        
        # Caixa de seleção do Mercado
        mercado_escolha = st.selectbox("Selecione o Mercado", 
                                      ["BTTS", "OVER 1.5 FT", "OVER 2.5 FT", "LTD", "Casa vence", "Visitante"])
        
        # Caixa para o Prognóstico %
        prognostico = st.number_input("Prognóstico (%)", min_value=0, max_value=100, value=90)

        submit = st.form_submit_button("📊 ANALISAR")

    if submit:
        # Salva no session_state para permitir conferência antes do envio
        st.session_state[f"dados_{nome}"] = {
            "casa": casa, "visitante": visitante, "horario": horario, 
            "ht": ht, "ft": ft, "mercado": mercado_escolha, "prog": prognostico
        }

    # Bloco de Exibição e Envio (aparece após analisar)
    if f"dados_{nome}" in st.session_state:
        d = st.session_state[f"dados_{nome}"]
        st.write(f"🎯 **Mercado:** {d['mercado']}")
        st.write(f"🔥 **Status:** {mercado_fervendo(d['prog'])} ({d['prog']}%)")
        
        renderizar_grafico(analisar_mercados()) # Gráfico simulado
        
        if st.button("🚀 ENVIAR PARA TELEGRAM", key=f"env_{nome}"):
            msg = f"""
{nome}
⚔️ {d['casa']} x {d['visitante']}
🕒 Horário: {d['horario']}

HT: {d['ht']} | FT: {d['ft']}

🎯 Mercado: {d['mercado']}
📊 Prognóstico: {d['prog']}%
🔥 {mercado_fervendo(d['prog'])}
"""
            enviar_telegram(msg)
            st.success("Enviado com sucesso!")
