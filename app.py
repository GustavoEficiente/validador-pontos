import streamlit as st
import os
import base64

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================
st.set_page_config(
    page_title="Comparativo Eficiente",
    page_icon="⚡",
    layout="wide"
)

# =====================================
# IDENTIFICAÇÃO DA LOGO
# =====================================
logo_path = "logo.png"

if os.path.exists(logo_path):
    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
            .logo-container {{
                position: fixed;
                top: 70px;   /* ↓ DESCEU A LOGO */
                left: 40px;
                z-index: 999;
            }}

            .logo-container img {{
                width: 160px;
            }}

            .center-content {{
                text-align: center;
            }}

            .box-upload {{
                max-width: 600px;
                margin: 0 auto 30px auto;
                background-color: #162033;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }}
        </style>

        <div class="logo-container">
            <img src="data:image/png;base64,{encoded_logo}">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Arquivo não encontrado: logo.png")

# =====================================
# AFASTAR CONTEÚDO DA LOGO
# =====================================
st.markdown("<div style='margin-top:120px;'></div>", unsafe_allow_html=True)

# =====================================
# CONTEÚDO CENTRALIZADO
# =====================================

st.markdown('<div class="center-content">', unsafe_allow_html=True)

st.title("COMPARATIVO EFICIENTE")
st.subheader("Processamento Automático de Relatórios")

st.markdown(
    """
    <div class="box-upload">
        Faça upload do arquivo <b>RELATORIO.csv</b> para aplicar as regras de negócio automaticamente.
    </div>
    """,
    unsafe_allow_html=True
)

# Upload também centralizado
uploaded_file = st.file_uploader(
    "Arraste seu arquivo CSV aqui",
    type=["csv"]
)

st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    st.success("✅ Arquivo carregado com sucesso!")
    # Aqui entra seu processamento depois

