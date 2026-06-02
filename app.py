# ... (código anterior dentro de calcular_probabilidade)

    # LIMITES
    p_over15 = min(round(p_over15, 1), 95)
    p_over25 = min(round(p_over25, 1), 90)
    p_btts = min(round(p_btts, 1), 85)
    p_ltd = min(round(p_ltd, 1), 95)

    return (
        round(p_casa, 1),
        round(p_visitante, 1),
        round(p_empate, 1),
        p_over15,
        p_over25,
        p_btts,
        p_ltd
    )
