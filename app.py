import streamlit as st
import pandas as pd
from PIL import Image
import os

# ---------- CONFIGURAÇÃO DA PÁGINA ----------
st.set_page_config(page_title="Catálogo Digital CLAMI", layout="wide")

# ---------- LOGO ----------
logo_path = "STATIC/IMAGENS/logo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=250)

# ---------- CARREGAR DADOS ----------
file_path = "ESTOQUE PRONTA ENTREGA CLAMI.xlsx"
df = pd.read_excel(file_path)

# ---------- NORMALIZAR NOMES DAS COLUNAS ----------
df.columns = df.columns.str.strip().str.upper()

# ---------- AJUSTAR NOMES PARA PADRÃO ----------
df = df.rename(columns={
    "DESCRIÇÃO": "DESCRIÇÃO",
    "CODIGO": "CÓDIGO",
    "MARCA": "MARCA",
    "COMPRIMENTO": "COMPRIMENTO",
    "ALTURA": "ALTURA",
    "LARGURA": "LARGURA",
    "DIÂMETRO": "DIÂMETRO",
    "IMAGEM": "IMAGEM"
})

# ---------- FILTRO ----------
st.sidebar.header("Filtros")
marcas = df["MARCA"].dropna().unique()
marca_filtro = st.sidebar.multiselect("Filtrar por Marca", marcas)

if marca_filtro:
    df = df[df["MARCA"].isin(marca_filtro)]

# ---------- GRID ----------
colunas = st.columns(4)

for i, (_, row) in enumerate(df.iterrows()):
    col = colunas[i % 4]
    with col:
        st.markdown("---")

        # ---------- IMAGEM ----------
        imagem_path = row.get("IMAGEM")
        if pd.notna(imagem_path) and os.path.exists(f"STATIC/IMAGENS/{imagem_path}"):
            st.image(f"STATIC/IMAGENS/{imagem_path}", use_container_width=True)
        else:
            st.image("STATIC/IMAGENS/sem_foto.png", use_container_width=True)

        # ---------- DESCRIÇÃO ----------
        st.markdown(f"**{row.get('DESCRIÇÃO', '')}**", unsafe_allow_html=True)

        # ---------- CÓDIGO ----------
        if pd.notna(row.get("CÓDIGO")):
            st.markdown(f"<small><b>Código:</b> {row.get('CÓDIGO')}</small>", unsafe_allow_html=True)

        # ---------- MARCA ----------
        if pd.notna(row.get("MARCA")):
            st.markdown(f"<small><b>Marca:</b> {row.get('MARCA')}</small>", unsafe_allow_html=True)

        # ---------- DIMENSÕES ----------
        dimensoes = []
        if pd.notna(row.get("COMPRIMENTO")):
            dimensoes.append(f"Comp.: {row.get('COMPRIMENTO')}")
        if pd.notna(row.get("ALTURA")):
            dimensoes.append(f"Alt.: {row.get('ALTURA')}")
        if pd.notna(row.get("LARGURA")):
            dimensoes.append(f"Larg.: {row.get('LARGURA')}")
        if pd.notna(row.get("DIÂMETRO")):
            dimensoes.append(f"Ø Diam: {row.get('DIÂMETRO')}")

        if dimensoes:
            st.markdown(f"<small>{', '.join(dimensoes)}</small>", unsafe_allow_html=True)
