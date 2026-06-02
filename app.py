import streamlit as st
import requests
import re
from supabase import create_client

# 1. Configurações e Conexão (No topo do arquivo)
SUPABASE_URL = "https://levzsvuikgqfnosykigi.supabase.co"
SUPABASE_KEY = "sb_publishable_esm8GzVdsIrPSjfcAkcX8Q_0NYasNBn"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

# 2. Definição das Funções (calcular_probabilidade e renderizar_bloco)
def calcular_probabilidade(texto):
    # ... (seu código aqui) ...
    return ...

def renderizar_bloco(titulo):
    # ... (seu código aqui) ...
    # O botão deve estar DENTRO desta função, nunca solto no arquivo!
    if st.button("🚀 ENVIAR PARA TELEGRAM", key=f"en_{titulo}"):
        # ...

# 3. Execução Final (Apenas no final do arquivo)
col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
