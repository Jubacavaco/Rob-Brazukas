# Lógica de Sugestão com Hierarquia de Prioridade
            # 1. Verifica se atende ao critério de Over 2.5 (>= 65%)
            if p >= 65:
                sugestao = "Over 2.5 FT"
            # 2. Se não, verifica Over 1.5 (>= 75% - embora se for menor que 65, o Over 2.5 já foi descartado)
            elif p >= 75: 
                sugestao = "Over 1.5 FT"
            # 3. Se não, verifica BTTS (>= 51%)
            elif p >= 51:
                sugestao = "Ambas Marcam (BTTS)"
            # 4. Caso contrário, LTD
            else:
                sugestao = "LTD"

            st.success(f"💡 **Sugestão:** {sugestao} (Prob: {p:.1f}%)")
            
            opcoes = ["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"]
            # Ajuste no index para garantir que a prioridade apareça primeiro no selectbox
            tipo = st.selectbox(f"Selecione o Mercado ({titulo}):", opcoes, index=opcoes.index(sugestao), key=f"sel_{titulo}")
