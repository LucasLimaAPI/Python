import os
import gzip
import tarfile
from tkinter import filedialog, Tk
import shutil

# Função para selecionar múltiplos arquivos compactados
def selecionar_arquivos():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    arquivos = filedialog.askopenfilenames(title="Selecione os arquivos compactados", filetypes=[("Arquivos Compactados", "*.gz;*.tar.gz")])
    return arquivos

# Função para descompactar arquivos .gz (não .tar.gz)
def descompactar_gz(arquivo):
    with gzip.open(arquivo, 'rb') as f_in:
        # O nome do arquivo descompactado será o mesmo sem a extensão '.gz'
        nome_arquivo = arquivo[:-3]
        with open(nome_arquivo, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Arquivo descompactado: {nome_arquivo}")

# Função para descompactar arquivos .tar.gz
def descompactar_tar_gz(arquivo):
    with tarfile.open(arquivo, "r:gz") as tar_ref:
        tar_ref.extractall()  # Extrai na pasta atual
    print(f"Arquivo descompactado: {arquivo}")

# Função principal que seleciona os arquivos e chama as funções de descompactação apropriadas
def descompactar_arquivos(arquivos):
    for arquivo in arquivos:
        if arquivo.endswith('.gz'):
            print(f"Descompactando {arquivo}...")
            descompactar_gz(arquivo)
        elif arquivo.endswith('.tar.gz'):
            print(f"Descompactando {arquivo}...")
            descompactar_tar_gz(arquivo)
        else:
            print(f"Formato de arquivo {arquivo} não suportado!")

# Função principal
def main():
    arquivos = selecionar_arquivos()
    if arquivos:
        descompactar_arquivos(arquivos)
    else:
        print("Nenhum arquivo selecionado.")

# Executando o programa
if __name__ == "__main__":
    main()
