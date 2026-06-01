import streamlit as st

st.set_page_config(layout="wide")
st.title("🤖 Painel Brazukas - Teste de Renderização")

# Teste simples: se isso aparecer, o problema era a complexidade do código anterior
col1, col2 = st.columns(2)

with col1:
    st.header("JOGO A")
    if st.button("Teste Botão A"):
        st.success("Botão A funcionando!")

with col2:
    st.header("JOGO B")
    if st.button("Teste Botão B"):
        st.success("Botão B funcionando!")
