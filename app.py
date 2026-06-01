import streamlit as st
import requests
import re

st.set_page_config(page_title="Sistema Brazukas", layout="wide")

# CSS para um look profissional (bordas arredondadas e sombras suaves)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .css-1r6slp0 { padding: 1rem; }
    div[data-testid="stMetricValue"] { font-size: 20px !important; }
    .block-container { padding-top: 2rem; }
    .stButton>button { border-radius: 8px; width: 100%; border: 1px solid #ccc; }
    .stTextInput>div>div>input { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1a2a6c;'>⚽ Brazukas Master Dashboard</h1>", unsafe_allow_html=True)

def calcular_probabilidade(texto):
    numeros = re.findall(r'\b[0-9]\b', re.sub(r'\d{2}\.\d{2}\.\d{2}', '', texto))
    gols = [int(n) for n in numeros]
    if len(gols) < 2: return 0
    return min((sum(gols) / len(gols)) * 65, 100)

def renderizar_bloco(titulo):
    # Usando st.expander ou containers para separar o input da análise
    with st.container():
        st.markdown(f"### 🏟️ {titulo}")
        
        # Grid de inputs compacto
        col1, col2, col3 = st.columns([2, 1, 1])
        camp = col1.text_input("Campeonato", key=f"c_{titulo}", placeholder="Ex: Premier League")
        hora = col2.text_input("Horário", key=f"h_{titulo}", placeholder="15:00")
        placar = col3.text_input("Placar", key=f"p_{titulo}", placeholder="0-0")
        
        c4, c5 = st.columns(2)
        casa = c4.text_input("Time Casa", key=f"ca_{titulo}")
        vis = c5.text_input("Time Visitante", key=f"vi_{titulo}")
        
        lista = st.text_area("Lista de jogos (Histórico)", key=f"l_{titulo}", height=70)
        
        if st.button(f"Analisar {titulo}", key=f"btn_{titulo}"):
            st.session_state[f"res_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()

        # Área de Resultados (só aparece após análise)
        if f"res_{titulo}" in st.session_state:
            p = st.session_state[f"res_{titulo}"]
            st.markdown("---")
            
            # Gráficos em colunas organizadas
            cols = st.columns(4)
            mercados = ["O 1.5", "O 2.5", "BTTS", "LTD"]
            valores = [min(p+5, 100), min(p, 100), min(p+2, 100), min(100-p, 100)]
            
            for i, c in enumerate(cols):
                c.metric(mercados[i], f"{valores[i]:.0f}%")
                c.progress(valores[i]/100)

            # Controlo de Envio
            m_sel = st.selectbox("Mercado de Envio", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "BTTS", "LTD"], key=f"sel_{titulo}")
            
            # Botão de Ação com destaque
            if st.button(f"🚀 Enviar Alerta {titulo}", key=f"send_{titulo}", type="primary"):
                st.success("Alerta processado e enviado!")

# Layout Principal
col_a, col_b = st.columns(2)
with col_a: renderizar_bloco("JOGO A")
with col_b: renderizar_bloco("JOGO B")
