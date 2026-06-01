# --- FUNÇÃO PARA CALCULAR % (Exemplo baseado em contagem de gols) ---
def calcular_porcentagem(lista):
    # Procura por números no texto (ex: gols nos últimos jogos)
    gols = re.findall(r'\d+', lista)
    gols = [int(g) for g in gols]
    
    if not gols: return 0
    
    # Exemplo de lógica: se a média de gols for alta, retorna uma % alta
    media = sum(gols) / len(gols)
    porcentagem = min(media * 20, 100) # Exemplo: multiplica a média por 20 para ter a %
    return porcentagem

# --- LÓGICA NO BOTÃO ---
if st.button("🔍 Analisar e Gerar"):
    if not lista_jogos:
        st.error("Por favor, cole a lista de jogos.")
    else:
        # Calcula a %
        perc = calcular_porcentagem(lista_jogos)
        st.write(f"📊 Probabilidade calculada: {perc:.1f}%")
        
        # Lógica de decisão baseada na %
        if perc >= 70: tipo = "Over 2.5"
        elif perc >= 50: tipo = "BTTS"
        else: tipo = "LTD"
        
        st.session_state.msg_preview = get_msg(tipo, campeonato, time_casa, time_visitante, horario)
