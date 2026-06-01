import streamlit as st
import re

st.set_page_config(layout="wide")
st.title("🤖 Painel Brazukas - Gestão Total")

# Função de análise simples
def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    return min((sum(gols)/len(gols)) * 35, 100)

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    # Inputs
    lista = st.text_area(f"Lista de jogos ({titulo})", key=f"l_{titulo}")
    
    # Botão Análise
    if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
        prob = calcular_probabilidade(lista)
        st.session_state[f"prob_{titulo}"] = prob
        st.write(f"📈 Probabilidade: {prob:.1f}%")
        
    # Exibir resultados se existir análise
    if f"prob_{titulo}" in st.session_state:
        st.write(f"Probabilidade atual: {st.session_state[f'prob_{titulo}']:.1f}%")
        if st.button(f"🚀 Enviar {titulo}", key=f"en_{titulo}"):
            st.success("Mensagem enviada com sucesso!")

# Layout de Colunas
col1, col2 = st.columns(2)

with col1:
    renderizar_bloco("JOGO A")
with col2:
    renderizar_bloco("JOGO B")
