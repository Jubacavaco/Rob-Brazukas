import streamlit as st
import requests
import re
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

# ... (Função calcular_probabilidade mantida como estava) ...
def calcular_probabilidade(texto):
    numeros = re.findall(r'\b\d+\b', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    over15 = over25 = btts = ltd = 0
    v_casa = v_vis = empate = total = 0
    i = 0
    while i < len(gols) - 1:
        g1, g2 = gols[i], gols[i+1]
        total += 1
        if (g1 + g2) >= 2: over15 += 1
        if (g1 + g2) >= 3: over25 += 1
        if g1 > 0 and g2 > 0: btts += 1
        if g1 != g2: ltd += 1
        if g1 > g2: v_casa += 1
        elif g2 > g1: v_vis += 1
        else: empate += 1
        i += 2
    if total == 0: return 0, 0, 0, 0, 0, 0, 0
    p15 = min(round(((over15/total)*100)+5, 1), 95)
    p25 = min(round(((over25/total)*100)+5, 1), 90)
    pb = min(round((btts/total)*100, 1), 85)
    pl = min(round((ltd/total)*100, 1), 95)
    return round((v_casa/total)*100, 1), round((v_vis/total)*100, 1), round((empate/total)*100, 1), p15, p25, pb, pl

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    hora = st.text_input("Horário", key=f"h_{titulo}")
    
    # Novos campos de escanteios (Jogo 4 ou outros)
    c_casa = st.number_input("Cantos Casa", min_value=0, key=f"cc_{titulo}")
    c_vis = st.number_input("Cantos Visitante", min_value=0, key=f"cv_{titulo}")
    total_cantos = c_casa + c_vis
    st.write(f"**Total de Cantos:** {total_cantos}")
    
    metodo = st.selectbox("Mercado", ["HT", "FT"], key=f"met_{titulo}")
    tipo = st.selectbox("Seleção", ["Over", "Under"], key=f"tipo_{titulo}")
    media_time = st.text_input("Média Escanteios Time", key=f"mt_{titulo}")
    media_liga = st.text_input("Média Liga", key=f"ml_{titulo}")
    
    # Botão para enviar no padrão solicitado
    if st.button("🚀 ENVIAR ALERTA ESCANTEIOS", key=f"en_{titulo}"):
        msg = (f"🚨🔥 ALERTA DE ESCANTEIOS 🔥🚨\n\n"
               f"🏆 Campeonato: {camp}\n"
               f"⚔️ Confronto: {casa} x {vis}\n"
               f"🎯 Mercado: Cantos {metodo} ({tipo})\n"
               f"💎 Entrada: {total_cantos} Cantos\n"
               f"📈 Probabilidade: Média Time {media_time} | Média Liga {media_liga}\n"
               f"🕒 Horário: {hora} (BR)\n\n"
               f"✅ Melhor momento para entrar no mercado.\n"
               f"📊 Seleção baseada em estatísticas e tendências das equipes.\n"
               f"🔞 Jogue com responsabilidade.\n"
               f"⚠️ Não há garantia de lucro. Gestão de banca é essencial.")
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg})
        st.success("Enviado!")

    # Gráfico (Apenas no Jogo 4)
    if titulo == "JOGO_D":
        st.subheader("📊 Gráfico de Probabilidade")
        html_code = """...[seu HTML AQUI]...""" # Cole seu código HTML/JS aqui
        components.html(html_code, height=450)

# Estrutura final
col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
