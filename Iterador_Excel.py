import pandas as pd
from tkinter import Tk, filedialog

# Inicializa a janela do Tkinter (não será exibida)
Tk().withdraw()

# Seleção de múltiplos arquivos CSV
arquivos_selecionados = filedialog.askopenfilenames(
    title="Selecione os arquivos CSV",
    filetypes=[("Arquivos CSV", "*.csv")]
)

# Verifica se algum arquivo foi selecionado
if not arquivos_selecionados:
    print("Nenhum arquivo selecionado.")
else:
    # Lista para armazenar os DataFrames
    dataframes = []

    # Lê cada arquivo selecionado, usando ; como separador e latin1 como encoding
    for arquivo in arquivos_selecionados:
        try:
            df = pd.read_csv(arquivo, sep=';', encoding='latin1', dtype=str)
            dataframes.append(df)
            print(f"Arquivo {arquivo} carregado com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar o arquivo {arquivo}: {e}")

    # Combina todos os DataFrames sem perder a estrutura
    if dataframes:
        df_final = pd.concat(dataframes, ignore_index=True)

        # Exporta para um novo arquivo CSV com ponto e vírgula como separador
        df_final.to_csv('arquivo_final.csv', sep=';', index=False, encoding='latin1')

        print("Arquivo combinado criado com sucesso: 'arquivo_final.csv'")
    else:
        print("Nenhum arquivo válido foi carregado.")
