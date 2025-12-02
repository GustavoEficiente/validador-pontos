import streamlit as st
import pandas as pd
import io
import os
import base64

# --- CONFIGURAÇÃO DA PÁGINA (INTERFACE) ---
st.set_page_config(
    page_title="Validador de Relatórios",
    page_icon="⚡",
    layout="centered"
)

# -------- TENTATIVA: LOGO FIXA NO CANTO SUPERIOR ESQUERDO --------
# Estratégia principal: embutir a imagem como data URI (base64).
logo_path = "logo.png"  # certifique-se que este arquivo está no mesmo diretório e commitado no repositório

def show_logo_left(logo_path, width=100):
    if not os.path.exists(logo_path):
        st.session_state.setdefault("_logo_error", f"Arquivo não encontrado: {logo_path}")
        return

    try:
        with open(logo_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        # CSS para posicionar fixo no canto superior esquerdo
        html = f"""
        <style>
        .logo-fixed-left {{
            position: fixed;
            top: 12px;
            left: 12px;
            z-index: 9999;
        }}
        /* Evita que a logo cubra conteúdo em telas pequenas */
        @media (max-width: 500px) {{
            .logo-fixed-left img {{ width: {int(width*0.7)}px !important; }}
        }}
        </style>
        <div class="logo-fixed-left">
            <img src="data:image/png;base64,{b64}" width="{width}" style="border-radius:6px;"/>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    except Exception as e:
        # fallback: tenta usar st.image (funciona localmente)
        try:
            st.image(logo_path, width=width)
            # adiciona pequena margem para não sobrepor o título
            st.markdown("<br/>", unsafe_allow_html=True)
        except Exception as e2:
            st.session_state.setdefault("_logo_error", f"Falha ao carregar logo: {e2}")

# chama a função que tenta mostrar a logo
show_logo_left(logo_path, width=100)

# se houve erro, mostra aviso discreto (não trava o app)
if "_logo_error" in st.session_state:
    st.warning(st.session_state["_logo_error"])

# --- CSS para deixar o botão mais bonito (opcional) ---
st.markdown("""
<style>
    div.stButton > button:first-child {
        background-color: #0099ff;
        color: white;
        font-size: 20px;
        border-radius: 10px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- TÍTULO / INFORMAÇÕES PRINCIPAIS ---
# acrescento um pequeno espaçamento horizontal via columns para o layout ficar alinhado com a logo
col_space_left, col_main = st.columns([0.12, 1])
with col_main:
    st.title("COMPARATIVO EFICIENTE")
    st.markdown("### Processamento Automático de Relatórios")
    st.info("Faça upload do arquivo `RELATORIO.csv` para aplicar as regras de negócio automaticamente.")

# --- 1. UPLOAD DO ARQUIVO ---
uploaded_file = st.file_uploader(
    "Arraste seu arquivo CSV aqui",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        # Lê o arquivo CSV enviado pelo usuário
        df = pd.read_csv(
            uploaded_file,
            sep=";",
            dtype=str,
            encoding="latin1"
        ).fillna("")

        st.write("---")
        st.write("🔍 **Arquivo carregado! Processando regras...**")

        # --- INÍCIO DA SUA LÓGICA DE NEGÓCIO ---

        # Normaliza nomes de colunas
        df.columns = [c.strip() for c in df.columns]

        # Garante colunas necessárias
        expected_cols = [
            "id_ponto","posicao","medicao","tipo_lampada","potencia",
            "tipo_luminaria","tipo_rede","plaqueta",
            "id_ponto_2","posicao_2","medicao_2","tipo_lampada_2",
            "potencia_2","tipo_luminaria_2","tipo_rede_2","plaqueta_2"
        ]
        for c in expected_cols:
            if c not in df.columns:
                df[c] = ""

        # Converte potência para número
        for col in ["potencia", "potencia_2"]:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.strip()
                .replace("", "0")
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Normaliza texto
        text_cols = [
            "tipo_lampada","tipo_lampada_2","medicao","medicao_2",
            "tipo_rede","tipo_rede_2","plaqueta","id_ponto","id_ponto_2"
        ]
        for c in text_cols:
            df[c] = df[c].astype(str).str.strip()

        # Inicia coluna resultado
        df["resultado"] = ""

        # REGRA 1 – REDUÇÃO DE POTÊNCIA
        mask_reducao = (
            df["tipo_lampada"].str.upper() == df["tipo_lampada_2"].str.upper()
        ) & (df["potencia"].astype(float) < df["potencia_2"].astype(float))
        df.loc[mask_reducao, "resultado"] += "REDUÇÃO DE POTENCIA; "

        # REGRA 2 – POSSÍVEL MUDANÇA DE MEDIÇÃO
        mask_medicao = (
            df["medicao_2"].str.upper().str.contains("SIM", na=False)
        ) & (
            df["medicao"].str.upper().str.contains("NÃO|NAO", na=False)
        )
        df.loc[mask_medicao, "resultado"] += "POSSIVEL MUDANÇA DE MEDIÇÃO; "

        # REGRA 3 – POSSÍVEL DUPLICIDADE
        contagem = df.groupby("id_ponto_2")["id_ponto"].transform("nunique")
        mask_dup = (contagem > 1) & (df["id_ponto_2"].str.strip() != "")
        df.loc[mask_dup, "resultado"] += "POSSIVEL DUPLICIDADE; "

        # REGRA 4 – MUDANÇA DE REDE
        mask_rede = (
            (df["tipo_rede"].str.upper() != df["tipo_rede_2"].str.upper())
        ) & (df["tipo_rede_2"].str.strip() != "")
        df.loc[mask_rede, "resultado"] += "MUDANÇA DE REDE; "

        # REGRA 5 – PONTO NOVO
        mask_novo = df["id_ponto_2"].str.strip() == ""
        df.loc[mask_novo, "resultado"] += "PONTO NOVO; "

        # REGRA 6 – PLAQUETA DUPLICADA
        plaquetas = df.groupby("plaqueta")["id_ponto"].transform("nunique")
        mask_plaq = (df["plaqueta"].str.strip() != "") & (plaquetas > 1)
        df.loc[mask_plaq, "resultado"] += "PLAQUETA DUPLICADA; "

        # Limpa o texto da coluna
        df["resultado"] = (
            df["resultado"]
            .str.replace(r"\s*;\s*$", "", regex=True)
            .str.replace(r"\s*;\s*", "; ", regex=True)
            .str.strip()
        )

        # --- FIM DA LÓGICA ---

        # Mostra uma prévia das linhas com observação
        st.success("✅ Processamento concluído!")
        st.subheader("Prévia dos itens com observações:")
        st.dataframe(df[df['resultado'] != ""].head())

        # --- DOWNLOAD DO RESULTADO ---
        csv_buffer = df.to_csv(
            sep=";",
            index=False,
            encoding="latin1"
        )

        st.download_button(
            label="📥 BAIXAR RELATÓRIO CORRIGIDO",
            data=csv_buffer,
            file_name="RELATORIO_CORRIGIDO.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")

