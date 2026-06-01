import streamlit as st
import requests
import re

# Configuração da página
st.set_page_config(layout="wide", page_title="Painel Brazukas")

# --- FUNÇÃO DE PERSISTÊNCIA ---
# Esta função garante que o valor digitado fique guardado no estado
def input_persistente(label, key, default=""):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.text_input(label, key=key, value=st.session_state[key])

st.title("🤖 Painel Brazukas - Gestão Total")

# Sidebar - Configurações que não se perdem
with st.sidebar:
    st.header("⚙️ Configurações")
    st.session_state['token'] = st.text_input("Token Telegram", value=st.session_state.get('token', ''), type="password")
    st.session_state['chat_id'] = st.text_input("ID Canal", value=st.session_state.get('chat_id', ''), type="password")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 20, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Usando os campos persistentes
        camp = st.text_input(f"Campeonato", key=f"c_{titulo}")
        hora = st.text_input(f"Horário", key=f"h_{titulo}")
        casa = st.text_input(f"Casa", key=f"ca_{titulo}")
        vis = st.text_input(f"Visitante", key=f"v_{titulo}")
        placar = st.text_input(f"Placar Final", key=f"p_{titulo}")
        lista = st.text_area(f"Lista de jogos", key=f"l_{titulo}", height=100)
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}", use_container_width=True):
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            # Caixa de ajuste manual (mantém o valor)
            p_manual = st.text_input("Ajustar Prob (%)", value=f"{p:.1f}", key=f"ajuste_{titulo}")
            p = min(float(p_manual), 100)
            
            # Gráficos
            col_g1, col_g2 = st.columns(2)
            col_g1.write(f"O 1.5 ({min(p+5, 100):.0f}%)"); col_g1.progress(min((p+5)/100, 1.0))
            col_g2.write(f"O 2.5 ({min(p, 100):.0f}%)"); col_g2.progress(min(p/100, 1.0))
            
            col_g3, col_g4 = st.columns(2)
            col_g3.write(f"BTTS ({max(0, p-10):.0f}%)"); col_g3.progress(max(0, p-10)/100)
            col_g4.write(f"LTD ({max(0, 100-p):.0f}%)"); col_g4.progress(max(0, 100-p)/100)
            
            mercado = st.selectbox(f"Mercado ({titulo})", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
            tipo = mercado if mercado != "Automático" else ("Over 1.5 FT" if p >= 70 else "LTD")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n📈 *Probabilidade:* {p:.1f}%\n⏰ *Horário:* {hora}\n\n⚠️ *Aposte com responsabilidade.*"
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                # Busca token e id salvos no session_state da sidebar
                t = st.session_state.get('token')
                c = st.session_state.get('chat_id')
                if t and c:
                    requests.post(f"https://api.telegram.org/bot{t}/sendMessage", data={"chat_id": c, "text": msg, "parse_mode": "Markdown"})
                    st.success("Enviado!")
                    st.session_state[f"msg_{titulo}"] = msg
                else:
                    st.error("Preencha Token e ID na lateral!")

# Layout
c_a, c_b = st.columns(2)
with c_a: renderizar_bloco("JOGO_A")
with c_b: renderizar_bloco("JOGO_B")
