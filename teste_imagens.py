import streamlit as st

# Configuração básica
st.set_page_config(page_title="Teste de Imagens GitHub", layout="centered")

st.title("🧪 Teste de Acesso às Imagens no GitHub")

# --- Configurações do repositório ---
GITHUB_USER = "mostruario"
GITHUB_REPO = "catalogo_pronta_entrega"
GITHUB_BRANCH = "main"

# --- Lista de imagens para testar ---
imagens = [
    "SEM IMAGEM.jpg",
    "SOFA SONETO_379922_379923.jpg"
]

st.write("🔍 Abaixo estão os links gerados diretamente do GitHub:")

for img_name in imagens:
    img_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/STATIC/IMAGENS/{img_name.replace(' ', '%20')}"
    st.markdown(f"**{img_name}** → [Abrir no navegador]({img_url})")
    st.image(img_url, caption=img_name)
