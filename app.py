import streamlit as st
import requests
import re

st.set_page_config(page_title="Sistema Brazukas", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { border-radius: 12px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🤖 Sistema Brazukas Top Tips</h1>", unsafe_allow_html=True)
st.write("---")

with st.sidebar:
    st.header("⚙️ Configurações")
    token = st.text_input("Token Telegram", type="password")
    chat_id = st.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    texto_limpo = re.sub(r'\d{2}\.\d{2}\.\d{2}', '', texto)
    numeros = re.findall(r'\b[0-9]\b', texto_limpo)
    gols = [int(n) for n in numeros]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 65, 100)

def renderizar_bloco(titulo):
    with st.container():
        st.subheader(f"🏟️ {titulo}")
        
        # Criação de chaves únicas para os inputs
        c1, c2 = st.columns(2)
        camp = c1.text_input("Campeonato", key=f"c_in_{titulo}")
        hora = c2.text_input("Horário", key=f"h_in_{titulo}")
        
        c3, c4, c5 = st.columns(3)
        casa = c3.text_input("Casa", key=f"ca_in_{titulo}")
        vis = c4.text_input("Visitante", key=f"v_in_{titulo}")
        placar = c5.text_input("Placar", key=f"p_in_{titulo}")
        
        lista = st.text_area("Lista de jogos", key=f"l_in_{titulo}", height=100)
        
        # Botão de análise
        if st.button(f"Analisar {titulo}", key=f"btn_{titulo}"):
            # Calculamos o valor e guardamos numa chave específica
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
            st.rerun() # Recarrega para exibir os resultados
            
        # Exibição dos resultados se a chave existir
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            st.markdown("---")
            st.write("📊 **Análise de Mercados:**")
            
            prob = float(p)
            v15 = min(prob + 5, 100)
            v25 = min(prob, 100)
            vBTTS = min(prob + 2, 100)
            vLTD = min(100 - prob, 100)
            
            cols = st.columns(4)
            cols[0].write(f"O 1.5: **{v15:.0f}%**"); cols[0].progress(v15/100)
            cols[1].write(f"O 2.5: **{v25:.0f}%**"); cols[1].progress(v25/100)
            cols[2].write(f"BTTS: **{vBTTS:.0f}%**"); cols[2].progress(vBTTS/100)
            cols[3].write(f"LTD: **{vLTD:.0f}%**"); cols[3].progress(vLTD/100)
            
            mercado_escolhido = st.selectbox("Mercado de Envio", 
                                            ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], 
                                            key=f"sel_mercado_{titulo}")
            
            if mercado_escolhido == "Automático":
                if prob >= 80: m_final = "Over 2.5 FT"
                elif prob >= 65: m_final = "Over 1.5 FT"
                elif prob >= 50: m_final = "Ambas Marcam (BTTS)"
                else: m_final = "LTD"
            else:
                m_final = mercado_escolhido
            
            prob_ajustada = st.text_input("Ajustar Prob (%)", value=f"{prob:.1f}", key=f"adj_{titulo}")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 Mercado: {m_final}\n📈 Probabilidade: {prob_ajustada}%\n⏰ {hora}"
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"send_{titulo}", type="primary"):
                if token and chat_id:
                    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                                  data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
                    st.success("Enviado com sucesso!")
                else:
                    st.error("Configure o Token e ID no menu lateral!")

col_a, col_b = st.columns(2)
with col_a: renderizar_bloco("JOGO_A")
with col_b: renderizar_bloco("JOGO_B")
