import streamlit as st
import pandas as pd
import unicodedata

st.set_page_config(page_title="Sistema de Processamento - Eficiente", layout="wide")

st.title("🔌 SISTEMA DE PROCESSAMENTO – EFICIENTE")

# ---------------------------------------
# FUNÇÃO: REMOVER ACENTOS
# ---------------------------------------
def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    )


# =====================================================================
# MODELO 1 – RELATÓRIO COMPARATIVO
# =====================================================================

st.markdown("---")
st.header("📘 MODELO 1 – RELATÓRIO COMPARATIVO")

st.info("Faça upload da base CSV para análise (Modelo 1).")

uploaded_file_1 = st.file_uploader(
    "Arraste aqui o arquivo RELATORIO.csv (Modelo 1)",
    type=["csv"],
    key="base1"
)

if uploaded_file_1 is not None:
    try:
        df1 = pd.read_csv(uploaded_file_1, sep=";", dtype=str, encoding="latin1").fillna("")

        st.success("✅ Arquivo carregado com sucesso!")

        st.subheader("🔎 Prévia dos dados:")
        st.dataframe(df1.head(50))

        csv_buffer_1 = df1.to_csv(sep=";", index=False, encoding="latin1")

        st.download_button(
            label="📥 Baixar Arquivo Modelo 1",
            data=csv_buffer_1,
            file_name="BASE_MODELO_1_PROCESSADA.csv",
            mime="text/csv",
            key="download1"
        )

    except Exception as e:
        st.error(f"Erro ao processar a base 1: {e}")


# =====================================================================
# MODELO 2 – PADRONIZAÇÃO DE BASE
# =====================================================================

st.markdown("---")
st.header("📙 MODELO 2 – PADRONIZAÇÃO DE BASE")

st.info("Faça upload do arquivo CSV para aplicar as regras de padronização (colunas O, N e Q).")

uploaded_file_2 = st.file_uploader(
    "Arraste aqui o arquivo do Modelo 2 (Padronização)",
    type=["csv"],
    key="base2"
)

if uploaded_file_2 is not None:
    try:
        df2 = pd.read_csv(uploaded_file_2, sep=";", dtype=str, encoding="latin1").fillna("")

        st.success("✅ Arquivo carregado. Iniciando tratamento...")

        # =====================================
        # 1) COLOCAR TUDO EM MAIÚSCULO
        # =====================================
        df2 = df2.applymap(lambda x: str(x).upper().strip())

        # =====================================
        # 2) REMOVER ACENTOS
        # =====================================
        df2 = df2.applymap(remover_acentos)

        # =====================================
        # 3) COLUNA Q – PADRONIZAÇÃO DAS LÂMPADAS (VERSÃO FORTE)
        # =====================================
        if "Q" in df2.columns:

            df2["Q"] = df2["Q"].astype(str).str.strip()

            df2.loc[df2["Q"].str.contains("LED", na=False), "Q"] = "LD"
            df2.loc[df2["Q"].str.contains("VAPOR", na=False), "Q"] = "VS"
            df2.loc[df2["Q"].str.contains("METAL", na=False), "Q"] = "ME"
            df2.loc[df2["Q"].str.contains("FLUOR", na=False), "Q"] = "FLC"

        # =====================================
        # 4) REGRA: COLUNA O -> N
        # =====================================
        if "O" in df2.columns and "N" in df2.columns:
            df2.loc[df2["O"] == "AGUARDANDO MEDICAO", "N"] = "NAO"

        # ============================


