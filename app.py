# ... dentro de renderizar_bloco
    if st.button("Analisar", key=f"an_{titulo}"):
        st.write("Botão clicado! Processando...") # Debug
        if lista:
            st.session_state[f"probs_{titulo}"] = calcular_probabilidade(lista)
            st.rerun() # Força a atualização da tela
        else:
            st.warning("A lista de jogos está vazia!")
