# Lógica de Sugestão seguindo a regra dos 51%
            if p >= 75:
                sugestao = "Over 1.5 FT"
            elif 51 <= p < 75:
                sugestao = "Over 2.5 FT"
            elif 30 <= p < 51:
                sugestao = "Ambas Marcam (BTTS)"
            else:
                sugestao = "LTD"

            st.success(f"💡 **Sugestão:** {sugestao} (Prob: {p:.1f}%)")
            
            # Mapeamento para o Selectbox
            opcoes = ["Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"]
            tipo = st.selectbox(f"Selecione o Mercado ({titulo}):", 
                                opcoes, 
                                index=opcoes.index(sugestao),
                                key=f"sel_{titulo}")
