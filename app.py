import pandas as pd

def processar_planilha(caminho_arquivo):
    print("\n✅ Arquivo carregado. Iniciando tratamento...\n")

    df = pd.read_excel(caminho_arquivo)

    # Conferir se existem colunas suficientes
    if df.shape[1] < 17:
        print("❌ ERRO: A planilha não possui colunas suficientes (deve ter pelo menos até a coluna Q).")
        return

    # Colunas por posição (A=0, B=1, C=2...)
    col_medicao = df.columns[13]      # N
    col_medidor_nc = df.columns[14]   # O
    col_tipo_lampada = df.columns[16] # Q

    print("✅ Colunas identificadas:")
    print(f"Coluna N (medicao): {col_medicao}")
    print(f"Coluna O (medidor_nc): {col_medidor_nc}")
    print(f"Coluna Q (tipo_lampada): {col_tipo_lampada}\n")

    resultados = []

    for index, row in df.iterrows():

        medicao = row[col_medicao]
        medidor_nc = row[col_medidor_nc]
        tipo_lampada = row[col_tipo_lampada]

        status = "OK"
        observacao = "Sem irregularidade"

        # REGRA 1 - Medição vazia
        if pd.isna(medicao):
            status = "ERRO"
            observacao = "Medição não informada"

        # REGRA 2 - Medidor NC vazio
        elif pd.isna(medidor_nc):
            status = "ERRO"
            observacao = "Medidor NC não informado"

        # REGRA 3 - Tipo de lâmpada vazio
        elif pd.isna(tipo_lampada):
            status = "ERRO"
            observacao = "Tipo da lâmpada não informado"

        # REGRA 4 - Medição não numérica
        elif not str(medicao).replace('.', '').isdigit():
            status = "ERRO"
            observacao = "Medição inválida (não é numérica)"

        # REGRA 5 - Medição muito baixa (exemplo)
        elif float(medicao) < 10:
            status = "ALERTA"
            observacao = "Medição abaixo do esperado"

        # Se passou em tudo
        else:
            status = "OK"
            observacao = "Conforme"

        resultados.append({
            "linha_planilha": index + 2,
            "medicao (N)": medicao,
            "medidor_nc (O)": medidor_nc,
            "tipo_lampada (Q)": tipo_lampada,
            "status": status,
            "observacao": observacao
        })

    resultado_df = pd.DataFrame(resultados)

    # Salvar arquivo final
    saida = "resultado_tratado.xlsx"
    resultado_df.to_excel(saida, index=False)

    print("✅ Tratamento finalizado com sucesso!")
    print(f"📁 Arquivo gerado: {saida}")


# ========================
# EXECUÇÃO
# ========================

caminho = input("Cole aqui o caminho do arquivo Excel: ")
processar_planilha(caminho)


