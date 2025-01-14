import pandas as pd
from tkinter import filedialog, Tk
import os

# Função para selecionar múltiplos arquivos .txt
def selecionar_arquivos_txt():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    arquivos = filedialog.askopenfilenames(title="Selecione os arquivos de texto", filetypes=[("Arquivos Texto", "*.log")])
    return arquivos

# Função para processar os arquivos .txt e extrair as informações
def processar_arquivos_txt(arquivos):
    dados_combinados = []

    for arquivo in arquivos:
        with open(arquivo, 'r', encoding='utf-8') as file:
            linhas = file.readlines()  # Lê todas as linhas do arquivo
            for linha in linhas:
                # Se houver necessidade de remover espaços ou quebras de linha, podemos fazer isso:
                linha = linha.strip()
                
                # Adiciona cada linha à lista de dados
                dados_combinados.append([linha])  # Cada linha é uma lista, para adicionar como uma linha do Excel
    
    return dados_combinados

# Função para salvar os dados em um novo arquivo Excel
def salvar_novo_arquivo(dados):
    # Cria um DataFrame com os dados combinados
    df_novo = pd.DataFrame(dados)

    # Salva em um novo arquivo Excel
    caminho_arquivo = "dados_combinados.xlsx"
    df_novo.to_excel(caminho_arquivo, index=False, header=False)

    print(f"Arquivo Excel gerado em: {os.path.abspath(caminho_arquivo)}")

# Função principal
def main():
    arquivos = selecionar_arquivos_txt()
    if arquivos:
        dados = processar_arquivos_txt(arquivos)
        salvar_novo_arquivo(dados)
    else:
        print("Nenhum arquivo selecionado.")

# Executando o programa
if __name__ == "__main__":
    main()
