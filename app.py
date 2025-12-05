import streamlit as st
import pandas as pd
import os
import base64
import unicodedata

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================
st.set_page_config(
    page_title="Validador de Relatórios",
    page_icon="⚡",
    layout="centered"
)

# =====================================
# CARREGAR LOGO NO TOPO ESQUERDO
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
            top: 70px;
            left: 25px;
            z-index: 9999;
        }}
        .logo-container img {{
            width: 160px;
        }}
        .titulo {{
            text-align: center;
            font-size: 34px;
            font-weight: bold;
        }}
        .subtitulo {{
            text-align: center;
            font-size: 18px;
        }}
        div.stButton > button:first-child {{
            background-color: #003366;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            width: 100%;
        }}
        </style>

        <div class="logo-container">
            <img src="data:image/png;base64,{encoded_logo}">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ arquivo logo.png não encontrado")

# Espaço para não conflitar com a logo
st.markdown("<div style='margin-top:120px;'></div>", unsafe_allow_html=True)

# =====================================
# TÍTULOS CENTRALIZADOS
# =====================================
st.markdown("<div class='titulo'>COMPARATIVO EFICIENTE</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Processamento Automático de Relatório</div>", unsafe_allow_html=True)

st.info("Faça upload do arquivo RELATORIO.csv para aplicar as regras de negócio automaticamente.")


# =====================================
# PRIMEIRO UPLOAD (SEU CÓDIGO ORIGINAL - INTACTO)
# =====================================
uploaded_file = st.file_uploader("Arraste seu arquivo CSV aqui", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=";", dtype=str, encoding="latin1").fillna("")

        st.write("---")
        st.write("🔍 **Arquivo carregado! Processando regras...**")

        df.columns = [c.strip() for c in df.columns]

        expected_cols = [
            "id_ponto","posicao","medicao","tipo_lampada","potencia",
            "tipo_luminaria","tipo_rede","plaqueta",
            "id_ponto_2","posicao_2","medicao_2","tipo_lampada_2",
            "potencia_2","tipo_luminaria_2","tipo_rede_2","plaqueta_2"
        ]

        for c in expected_cols:
            if c not in df.columns:
                df[c] = ""

        for col in ["potencia", "potencia_2"]:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.strip()
                .replace("", "0")
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        text_cols = [
            "tipo_lampada","tipo_lampada_2","medicao","medicao_2",
            "tipo_rede","tipo_rede_2","plaqueta","id_ponto","id_ponto_2"
        ]

        for c in text_cols:
            df[c] = df[c].astype(str).str.strip()

        df["resultado"] = ""

        mask_reducao = (
            df["tipo_lampada"].str.upper() == df["tipo_lampada_2"].str.upper()
        ) & (df["potencia"] < df["potencia_2"])
        df.loc[mask_reducao, "resultado"] += "REDUÇÃO DE POTENCIA; "

        mask_medicao = (
            df["medicao_2"].str.upper().str.contains("SIM", na=False)
        ) & (
            df["medicao"].str.upper().str.contains("NÃO|NAO", na=False)
        )
        df.loc[mask_medicao, "resultado"] += "POSSIVEL MUDANÇA DE MEDIÇÃO; "

        contagem = df.groupby("id_ponto_2")["id_ponto"].transform("nunique")
        mask_dup = (contagem > 1) & (df["id_ponto_2"].str.strip() != "")
        df.loc[mask_dup, "resultado"] += "POSSIVEL DUPLICIDADE; "

        mask_rede = (
            df["tipo_rede"].str.upper() != df["tipo_rede_2"].str.upper()
        ) & (df["tipo_rede_2"].str.strip() != "")
        df.loc[mask_rede, "resultado"] += "MUDANÇA DE REDE; "

        mask_novo = df["id_ponto_2"].str.strip() == ""
        df.loc[mask_novo, "resultado"] += "PONTO NOVO; "

        plaquetas = df.groupby("plaqueta")["id_ponto"].transform("nunique")
        mask_plaq = (df["plaqueta"].str.strip() != "") & (plaquetas > 1)
        df.loc[mask_plaq, "resultado"] += "PLAQUETA DUPLICADA; "

        df["resultado"] = (
            df["resultado"]
            .str.replace(r"\s*;\s*$", "", regex=True)
            .str.replace(r"\s*;\s*", "; ", regex=True)
            .str.strip()
        )

        st.success("✅ Processamento concluído!")
        st.subheader("Prévia dos itens com observações:")
        st.dataframe(df[df['resultado'] != ""].head())

        csv_buffer = df.to_csv(sep=";", index=False, encoding="latin1")

        st.download_button(
            label="📥 BAIXAR RELATÓRIO CORRIGIDO",
            data=csv_buffer,
            file_name="RELATORIO_CORRIGIDO.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")


# =====================================================================
# ✅✅✅ SEGUNDO UPLOAD - MODELO DIFERENTE (QUE VOCÊ PEDIU)
# =====================================================================

st.write("---")
st.subheader("📂 Upload - Modelo Alternativo (Padronização de Base)")

uploaded_file2 = st.file_uploader(
    "Arraste o SEGUNDO modelo de base aqui",
    type=["csv"],
    key="segundo_upload"
)

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    )

if uploaded_file2 is not None:
    try:
        df2 = pd.read_csv(uploaded_file2, sep=";", dtype=str, encoding="latin1").fillna("")

        # -----------------------------
        # COLOCAR TUDO EM MAIÚSCULO
        # -----------------------------
        df2 = df2.applymap(lambda x: str(x).upper())

        # -----------------------------
        # REMOVER ACENTOS
        # -----------------------------
        df2 = df2.applymap(remover_acentos)

        # -----------------------------
        # SUBSTITUIÇÃO EM tipo_lampada
        # -----------------------------
        if "tipo_lampada" in df2.columns:
            df2["tipo_lampada"] = df2["tipo_lampada"].replace({
                "LAMPADA LED": "LD",
                "LAMPADA VAPOR SODIO": "VS",
                "LAMPADA METALICA": "ME",
                "LAMPADA FLUORESCENTES": "FLC"
            })

        # ----------------------------------------------------
        # REGRA: medidor_nc = AGUARDANDO MEDICAO → medicao = NAO
        # ----------------------------------------------------
        if "medidor_nc" in df2.columns and "medicao" in df2.columns:
            mask_medidor = df2["medidor_nc"].str.contains("AGUARDANDO MEDICAO", na=False)
            df2.loc[mask_medidor, "medicao"] = "NAO"

        st.success("✅ Segunda base processada com sucesso!")
        st.subheader("Prévia do segundo modelo tratado:")
        st.dataframe(df2.head())

        csv_buffer2 = df2.to_csv(sep=";", index=False, encoding="latin1")

        st.download_button(
            label="📥 BAIXAR BASE PADRONIZADA",
            data=csv_buffer2,
            file_name="BASE_PADRONIZADA.csv",
            mime="text/csv",
            key="download2"
        )

    except Exception as e:
        st.error(f"Erro ao processar o segundo modelo: {e}")

