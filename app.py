import streamlit as st
import pandas as pd


st.set_page_config(page_title="Validador de Pontos", layout="wide")

st.title("Validador de Pontos - Censo de Iluminação")


# ==============================
# FUNÇÕES
# ==============================

def preencher_tipo_lampada(df):
    """
    Preenche a coluna 'tipo_lampada' baseada em palavras-chave
    encontradas na descrição ou em outras colunas.
    """

    if "tipo_lampada" not in df.columns:
        df["tipo_lampada"] = ""

    if "descricao" not in df.columns:
        return df

    for i, row in df.iterrows():

        if pd.isna(row["tipo_lampada"]) or str(row["tipo_lampada"]).strip() == "":

            texto = str(row["descricao"]).upper()

            if "LED" in texto:
                df.at[i, "tipo_lampada"] = "LAMPADA LED"

            elif "VAPOR" in texto and "SODIO" in texto:
                df.at[i, "tipo_lampada"] = "LAMPADA VAPOR SODIO"

            elif "MERCURIO" in texto:
                df.at[i, "tipo_lampada"] = "LAMPADA VAPOR MERCURIO"

            else:
                df.at[i, "tipo_lampada"] = "DESCONHECIDO"

    return df


def validar_potencia(df):
    """
    Garante que a potência seja numérica e válida
    """

    if "potencia" in df.columns:
        df["potencia"] = pd.to_numeric(df["potencia"], errors="coerce")

    return df


# ==============================
# INTERFACE
# ==============================

st.markdown("Faça upload da sua planilha (.xlsx)")

arquivo = st.file_uploader("Selecione seu arquivo", type=["xlsx", "xls"])


if arquivo is not None:

    try:

        df = pd.read_excel(arquivo)

        st.success("Arquivo carregado com sucesso!")

        st.subheader("Pré-visualização dos dados")
        st.dataframe(df.head(50))

        # ==============================
        # PROCESSAMENTOS
        # ==============================

        df = preencher_tipo_lampada(df)
        df = validar_potencia(df)

        st.subheader("Dados após tratamento do tipo da lâmpada")
        st.dataframe(df)

        # ==============================
        # DOWNLOAD
        # ==============================

        nome_saida = "arquivo_tratado.xlsx"
        df.to_excel(nome_saida, index=False)

        with open(nome_saida, "rb") as file:
            st.download_button(
                label="📥 Baixar arquivo tratado",
                data=file,
                file_name=nome_saida,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error("Erro no processamento do arquivo.")
        st.exception(e)


else:
    st.info("Aguardando upload do arquivo...")



