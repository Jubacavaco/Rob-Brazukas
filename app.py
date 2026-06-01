def obter_sugestao(p):
    # Hierarquia ajustada conforme suas regras:
    if p >= 75: 
        return "Over 1.5 FT"
    elif p >= 65: 
        return "Over 2.5 FT"
    elif p >= 51: 
        return "Ambas Marcam (BTTS)"
    else: 
        return "LTD"
