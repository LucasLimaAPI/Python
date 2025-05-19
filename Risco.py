import pandas as pd
import re

CAMINHO_ARQUIVO = r'C:\Users\lucas.oliveira\OneDrive - Terra Investimentos DTVM\Área de Trabalho\Documentos\Python\Caldara\Planilha_Win.xlsx'

colunas_esperadas = [
    'nVendaID', 'nOperadorID', 'ID do Ponto', 'Plano', 'Operador', 'Documento',
    'Conta', 'SubConta', 'Data de Venda', 'Data da Início', 'Data Final',
    'Dias Assinatura', 'Valor Cobrado ( R$ )', 'Data limite de utilização (Perícia)',
    'Situação', 'Páginas', 'Observação'
]

def normalizar(texto):
    if pd.isna(texto):
        return ''
    return re.sub(r'\s+', ' ', str(texto).strip()).lower()

def encontrar_linha_cabecalho_flex(df):
    for i in range(len(df)):
        linha = df.iloc[i].astype(str).apply(normalizar)
        acertos = sum(1 for col in colunas_esperadas if any(normalizar(col) in cell for cell in linha))
        if acertos >= 5:
            return i
    return None

def combinar_planilhas(caminho_arquivo):
    xl = pd.ExcelFile(caminho_arquivo)
    df_final = pd.DataFrame()

    for sheet in xl.sheet_names:
        df_raw = xl.parse(sheet, header=None)
        linha_cabecalho = encontrar_linha_cabecalho_flex(df_raw)

        if linha_cabecalho is not None:
            df = xl.parse(sheet, header=linha_cabecalho)
            df.columns = [normalizar(col) for col in df.columns]

            mapa_colunas = {normalizar(orig): orig for orig in colunas_esperadas}
            df = df.rename(columns={col: mapa_colunas[col] for col in df.columns if col in mapa_colunas})

            colunas_validas = [col for col in colunas_esperadas if col in df.columns]
            df = df[colunas_validas]
            df["Planilha"] = sheet
            df_final = pd.concat([df_final, df], ignore_index=True)
        else:
            print(f"⚠️ Cabeçalho não encontrado na aba: {sheet}")

    if not df_final.empty:
        df_final.to_excel("planilha_combinada_ordenada.xlsx", index=False)
        print("✅ Arquivo salvo: planilha_combinada_ordenada.xlsx")
    else:
        print("❌ Nenhuma aba pôde ser processada. Verifique se o layout está dentro do esperado.")

# Execute
combinar_planilhas(CAMINHO_ARQUIVO)
