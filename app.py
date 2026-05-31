import streamlit as st

# ==============================================================================
# CONFIGURAÇÕES DA PÁGINA
# ==============================================================================
st.set_page_config(page_title="Robô Brazukas - Gerador de Tips", layout="centered")

st.title("🚨 Painel de Controle - Robô Brazukas 🚨")
st.write("Preencha os campos abaixo para gerar o Alerta de Entrada padronizado.")

# ==============================================================================
# FORMULÁRIO COM OS CAMPOS DO COLAB
# ==============================================================================
with st.form("form_tips"):
    st.subheader("📝 Dados da Partida")
    
    # Campo para o Campeonato
    campeonato = st.text_input("🏆 Campeonato:", placeholder="Ex: Campeonato Brasileiro Série A")
    
    # Campos para o Jogo (Equipes)
    col_jogos = st.columns(2)
    with col_jogos[0]:
        time_casa = st.text_input("🆚 Time da Casa:", placeholder="Ex: Athletico Paranaense")
    with col_jogos[1]:
        time_fora = st.text_input("🆚 Time de Fora:", placeholder="Ex: Botafogo")
        
    st.markdown("---")
    st.subheader("📈 Mercado & Odds")
    
    # Campos para as Odds (Probabilidades)
    col_odds = st.columns(3)
    with col_odds[0]:
        odd_casa = st.number_input("Odds Casa (1):", min_value=1.0, max_value=100.0, value=2.0, step=0.01)
    with col_odds[1]:
        odd_empate = st.number_input("Odds Empate (X):", min_value=1.0, max_value=100.0, value=3.40, step=0.01)
    with col_odds[2]:
        odd_fora = st.number_input("Odds Fora (2):", min_value=1.0, max_value=100.0, value=3.50, step=0.01)

    # Configuração dos Mercados
    mercado_principal = st.text_input("🎯 Mercado Principal:", value="Resultado Final (1X2) ou Ambas Marcam")
    linha_escanteios = st.text_input("📐 Linha de Escanteios (Mercado Secundário):", placeholder="Ex: Mais de 9.5 Escanteios")
    
    st.markdown("---")
    st.subheader("⏰ Horário e Configurações de Envio")
    
    # Horário do Jogo
    horario = st.text_input("⏰ Horário do Jogo:", placeholder="Ex: 19h30")
    
    # Botão para processar e gerar o texto final
    submetido = st.form_submit_button("🔥 Gerar Alerta de Entrada")

# ==============================================================================
# PROCESSAMENTO E SAÍDA DA TIP FORMATADA
# ==============================================================================
if submetido:
    if campeonato and time_casa and time_fora and horario:
        st.subheader("📋 Mensagem Formatada Pronto para Copiar")
        
        # Estrutura exata com base nas suas diretrizes salvas
        template_tip = (
            f"🚨 Alerta de Entrada 🚨\n\n"
            f"🏆 Campeonato: {campeonato}\n"
            f"🆚 Jogo: {time_casa} x {time_fora}\n"
            f"🎯 Mercado Principal: {mercado_principal}\n"
            f"📈 Mercado Secundário (Escanteios): {linha_escanteios}\n"
            f"⏰ Horário: {horario} (BR)\n\n"
            f"📊 Odds de Momento:\n"
            f"• {time_casa}: {odd_casa:.2f} | • Empate: {odd_empate:.2f} | • {time_fora}: {odd_fora:.2f}\n\n"
            f"📌 Entrada recomendada ao vivo!\n\n"
            f"⚽ Gestão da Entrada:\n"
            f"• Buscar o
