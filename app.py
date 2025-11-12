import streamlit as st
import pandas as pd
import os

# Caminho do arquivo Excel
DATA_PATH = "ESTOQUE PRONTA ENTREGA CLAMI.xlsx"

# Caminho para imagens
IMAGE_PATH = "STATIC/IMAGENS"

# --- Leitura e padronização do DataFrame ---
df = pd.read_excel(DATA_PATH, header=1)
df.columns = df.columns.str.strip().str.upper()

# Padroniza nomes de colunas abreviadas
df = df.rename(columns={
    "LARGU": "LARGURA",
    "ALTU": "ALTURA",
    "DIAME": "DIAMETRO",
    "CÓDIGO DO PRODUTO": "CODIGO DO PRODUTO"
})

df = df.drop_duplicates(subset="CODIGO DO PRODUTO", keep="first")

# --- Interface ---
st.image(os.path.join(IMAGE_PATH, "logo.png"), width=200)
st.title("CATÁLOGO - PRONTA ENTREGA")

# Filtros
marcas = df["MARCA"].dropna().unique().tolist()
marcas.insert(0, "")
marca_selecionada = st.selectbox("Marca", options=marcas)

descricao_filtro = st.text_input("Buscar produto")

# Filtragem
df_filtrado = df.copy()

if marca_selecionada:
    df_filtrado = df_filtrado[df_filtrado["MARCA"] == marca_selecionada]

if descricao_filtro:
    df_filtrado = df_filtrado[df_filtrado["DESCRIÇÃO DO PRODUTO"].str.contains(descricao_filtro, case=False, na=False)]

# --- Exibição dos produtos ---
for _, row in df_filtrado.iterrows():
    with st.container():
        cols = st.columns([1, 2])
        with cols[0]:
            imagem = row["LINK_IMAGEM"]
            if not os.path.exists(imagem):
                imagem = os.path.join(IMAGE_PATH, "SEM IMAGEM.jpg")
            st.image(imagem, use_container_width=True)

        with cols[1]:
            st.markdown(f"**{row['DESCRIÇÃO DO PRODUTO']}**", unsafe_allow_html=True)
            st.markdown(f"<small><b>Código:</b> {row['CODIGO DO PRODUTO']}</small>", unsafe_allow_html=True)
            st.markdown(f"<small><b>Marca:</b> {row['MARCA']}</small>", unsafe_allow_html=True)

            comp = row.get("COMPRIMENTO", "")
            alt = row.get("ALTURA", "")
            larg = row.get("LARGURA", "")
            diam = row.get("DIAMETRO", "")

            medidas = []
            if comp: medidas.append(f"<b>Comp.:</b> {comp}")
            if alt: medidas.append(f"<b>Alt.:</b> {alt}")
            if larg: medidas.append(f"<b>Larg.:</b> {larg}")
            if diam: medidas.append(f"<b>Diâm.:</b> {diam}")

            if medidas:
                st.markdown("<small>" + ", ".join(medidas) + "</small>", unsafe_allow_html=True)

            estoque = row.get("ESTOQUE DISPONIVEL", "")
            if estoque:
                st.markdown(f"<small><b>Estoque:</b> {estoque}</small>", unsafe_allow_html=True)

        st.markdown("---")
