import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Comparativo Eficiente",
    page_icon="⚡",
    layout="centered"
)

# Estilo personalizado
st.markdown("""
    <style>
        .titulo {
            text-align: center;
            font-size: 34px;
            font-weight: bold;
            margin-top: 10px;
        }

        .subtitulo {
            text-align: center;
            font-size: 18px;
            margin-bottom: 30px;
            color: #555;
        }

        .container {
            max-width: 800px;
            margin: auto;
        }

        .imagem {
            display: flex;
            justify-content: center;
            margin-top: 40px; /* desce a imagem */
            margin-bottom: 40px;
        }
    </style>
""", unsafe_allow_html=True)


# Container principal
st.markdown("<div class='container'>", unsafe_allow_html=True)

# Títulos CENTRALIZADOS
st.markdown("<div class='titulo'>COMPARATIVO EFICIENTE</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Processamento Automático de Relatório</div>", unsafe_allow_html=True)

# IMAGEM (ajustada para mais para baixo, mesmo tamanho)
st.markdown("<div class='imagem'>", unsafe_allow_html=True)
st.image("logo.png", width=350)  # <-- mantenha esse tamanho
st.markdown("</div>", unsafe_allow_html=True)

# Upload de arquivos
st.markdown("### 📂 Envie os relatórios para análise")

arquivo1 = st.file_uploader("Relatório Atual", type=["xlsx", "csv"])
arquivo2 = st.file_uploader("Relatório Anterior", type=["xlsx", "csv"])

# Botão processar
if st.button("⚙️ Processar Comparação"):
    if arquivo1 and arquivo2:
        st.success("✅ Arquivos enviados com sucesso!")
        st.info("Aqui será exibido o resultado do processamento...")
        # Aqui você pode chamar sua função principal
        # resultado = processar(arquivo1, arquivo2)
        # st.dataframe(resultado)
    else:
        st.warning("⚠️ Envie os dois arquivos para continuar.")

st.markdown("</div>", unsafe_allow_html=True)

