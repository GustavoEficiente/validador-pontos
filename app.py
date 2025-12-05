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

st.info("Coluna Q ➜ tipo_lampada | Coluna O ➜ medidor_nc | Coluna N ➜ medicao")

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
        # 3) PADRONIZAÇÃO DA COLUNA tipo_lampada
        # =====================================
        if "TIPO_LAMPADA" in df2.columns:

            df2["TIPO_LAMPADA"] = df2["TIPO_LAMPADA"].astype(str).str.strip()

            df2.loc[df2["TIPO_LAMPADA"].str.contains("LED", na=False), "TIPO_LAMPADA"] = "LD"
            df2.loc[df2["TIPO_LAMPADA"].str.contains("VAPOR", na=False), "TIPO_LAMPADA"] = "VS"
            df2.loc[df2["TIPO_LAMPADA"].str.contains("SODIO", na=False), "TIPO_LAMPADA"] = "VS"
            df2.loc[df2["TIPO_LAMPADA"].str.contains("METAL", na=False), "TIPO_LAMPADA"] = "ME"
            df2.loc[df2["TIPO_LAMPADA"].str.contains("FLUOR", na=False), "TIPO_LAMPADA"] = "FLC"

        else:
            st.warning("⚠️ A coluna 'tipo_lampada' não foi encontrada no arquivo!")

        # =====================================
        # 4) REGRA: medidor_nc ➜ medicao
        # =====================================
        if "MEDIDOR_NC" in df2.columns and "MEDICAO" in df2.columns:

            df2.loc[df2["MEDIDOR_NC"] == "AGUARDANDO MEDICAO", "MEDICAO"] = "NAO"

        else:
            st.warning("⚠️ As colunas 'medidor_nc' ou 'medicao' não foram encontradas!")

        # =====================================
        # EXIBIR PRÉVIA
        # =====================================
        st.success("✅ Tratamento finalizado com sucesso!")

        st.subheader("🔍 Prévia do arquivo tratado:")
        st.dataframe(df2.head(50))

        # =====================================
        # DOWNLOAD
        # =====================================
        csv_buffer_2 = df2.to_csv(sep=";", index=False, encoding="latin1")

        st.download_button(
            label="📥 Baixar Modelo 2 tratado",
            data=csv_buffer_2,
            file_name="BASE_MODELO_2_TRATADA.csv",
            mime="text/csv",
            key="download2"
        )

    except Exception as e:
        st.error(f"Erro ao processar a segunda base: {e}")


st.markdown("---")
st.caption("Sistema desenvolvido para a empresa EFICIENTE ⚡ Trabalhando de forma eficiente")


