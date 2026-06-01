import streamlit as st

st.title("Painel Brazukas")

# Teste simples para ver se ele lê o ficheiro
try:
    token = st.secrets["token"]
    st.write("✅ Consegui ler o Token!")
except:
    st.write("❌ Não encontrei o token. O ficheiro .streamlit/secrets.toml está lá?")
