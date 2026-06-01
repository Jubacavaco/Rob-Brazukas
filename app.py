import streamlit as st
import requests
import re

st.set_page_config(layout="wide", page_title="Sistema Brazukas Top Tips")
st.title("🤖 Sistema Brazukas Top Tips")

# --- Função de persistência ---
def manter_valor(key, valor_padrao=""):
    if key not in st.session_state:
        st.session_state[key] = valor_padrao
    return st.session_state[key]

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 20, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Usamos o 'manter_valor' para que o Streamlit lembre o que foi digitado
        camp = st.text_input("Campeonato", value=manter_valor(f"c_{titulo}"), key=f"c_{titulo}")
        hora = st.text_input("Horário", value=manter_valor(f"h_{titulo}"), key=f"h_{titulo}")
        casa = st.text_input("Casa", value=manter_valor(f"ca_{titulo}"), key=f"ca_{titulo}")
        vis = st.text_input("Visitante", value=manter_valor(f"v_{titulo}"), key=f"v_{titulo}")
        lista = st.text_area("Lista de jogos", value=manter_valor(f"l_{titulo}"), key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            # Campo de probabilidade também persistente
            prob_valor = st.number_input("Probabilidade (%)", value=float(p), key=f"p_val_{titulo}")
            placar = st.text_input("Placar Final", value=manter_valor(f"p_{titulo}"), key=f"p_{titulo}")
            
            # Gráficos e Lógica permanecem visíveis porque dependem do session_state
            st.write("📊 **Análise Gráfica:**")
            col1, col2 = st.columns(2)
            col1.write(f"O 1.5 ({min(p+5, 100):.0f}%)"); col1.progress(min((p+5)/100, 1.0))
            col2.write(f"O 2.5 ({min(p, 100):.0f}%)"); col2.progress(min(p/100, 1.0))
            
            # Lógica de sugestão
            if prob_valor >= 65: sugestao = "Over 2.5 FT"
            elif prob_valor >= 75: sugestao = "Over 1.5 FT"
            elif prob_valor >= 51: sugestao = "Ambas Marcam (BTTS)"
            else: sugestao = "LTD"

            st.success(f"💡 Sugestão: {sugestao}")
            opcoes = ["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"]
            tipo = st.selectbox(f"Selecione o Mercado ({titulo}):", opcoes, index=opcoes.index(sugestao), key=f"sel_{titulo}")
            
            # Botão de envio (mantido como antes)
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                # (Seu código de envio permanece aqui...)
                st.success("Enviado!")

# Restante do código de Edição e Status igual ao anterior...
