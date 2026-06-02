# ... (dentro da função jogo_normal)
    
    # Esta função será chamada ao clicar em ANALISAR
    def processar_analise(lista_texto):
        # Aqui você pode colocar a lógica que conta gols, escanteios, etc.
        # Por enquanto, apenas um exemplo para mostrar que funcionou
        return "Lista Processada com Sucesso"

    if btn_analisar:
        # 1. Processa a lista
        resultado = processar_analise(lista)
        
        # 2. Salva os dados no estado da sessão
        st.session_state[f"dados_{nome}"] = {
            "camp": camp, "casa": casa, "vis": visitante, 
            "horario": horario, "ht": ht, "ft": ft, 
            "merc": mercado, "prob": prob, "analise": resultado
        }
        
        # 3. Notifica e recarrega
        st.success(f"Análise de {nome} concluída: {resultado}")
        st.rerun()
