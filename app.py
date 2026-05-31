import streamlit as st
import pandas as pd
import requests
import re
import matplotlib.pyplot as plt

# ==============================================================================
# CONFIGURAÇÕES INICIAIS & CONSTANTES
# ==============================================================================
st.set_page_config(page_title="Robô Brazukas - Painel de Tips", layout="wide")

# ==============================================================================
# FUNÇÕES DE PROCESSAMENTO DE TEXTO (REGEX)
# ==============================================================================
def extrair_dados_partida(texto):
    """
    Função para processar o texto bruto da mensagem e extrair as informações
    dos blocos de jogos, corrigindo variações de digitação (como Únlimos).
    """
    # Linha 137 corrigida: Unificação das strings para evitar quebra de linha física
    bloco_casa_match = re.search(r"(.*?)(?:Últimos jogos:|Únlimos jogos:)", texto, re.DOTALL)
    bloco_fora_match = re.search(r"(?:Últimos jogos:|Únlimos jogos:)(.*)", texto, re.DOTALL)
    
    casa_texto = bloco_casa_match.group(1).strip() if bloco_casa_match else ""
    fora_texto = bloco_fora_match.group(1).strip() if bloco_fora_match else ""
    
    return casa_texto, fora_texto

# ==============================================================================
# INTERFACE DO UTILIZADOR (STREAMLIT)
# ==============================================================================
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")
st.write("Insira os dados abaixo para gerar a formatação padrão da entrada.")

# Área de texto para colar a mensagem bruta
entrada_texto = st.text_area("Cole aqui o texto bruto da análise:", height=200)

if st.button("Processar Análise"):
    if entrada_texto:
        casa, fora = extrair_dados_partida(entrada_texto)
        
        st.subheader("📊 Dados Extraídos com Sucesso")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Histórico Equipas da Casa:**")
            st.info(casa if casa else "Nenhum dado encontrado para a equipa da casa.")
            
        with col2:
            st.markdown("**Histórico Equipas de Fora:**")
            st.info(fora if fora else "Nenhum dado encontrado para a equipa de fora.")
            
        # ======================================================================
        # MODELO DE SAÍDA PADRÃO (CONFORME DIRETRIZES)
        # ======================================================================
        st.subheader("📋 Mensagem Formatada para Envio")
        
        template_tip = (
            "🚨 **Alerta de Entrada** 🚨\n\n"
            "🏆 **Campeonato:** [Inserir Campeonato]\n"
            "🆚 **Jogo:** [Equipa Casa] x [Equipa Fora]\n"
            "🎯 **Mercado Principal:** [Inserir Mercado]\n"
            "📈 **Mercado Secundário (Escanteios):** Mais de X Escanteios\n"
            "⏰ **Horário:** [Inserir Horário] (BR)\n\n"
            "📌 *Entrada recomendada ao vivo!*\n"
            "⚠️ Aposte com responsabilidade. Gestão de banca é fundamental."
        )
        
        st.code(template_tip, language="text")
    else:
        st.warning("Por favor, cole algum texto antes de processar.")
