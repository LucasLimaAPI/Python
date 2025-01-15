import os
import gzip
import tarfile
from tkinter import filedialog, Tk
import shutil

# Função para selecionar múltiplos arquivos compactados
def selecionar_arquivos():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    arquivos = filedialog.askopenfilenames(title="Selecione os arquivos compactados", filetypes=[("Arquivos Compactados", "*.gz;*.tar.gz;*.tar")])
    print(f"Arquivos selecionados: {arquivos}")  # Mensagem de depuração
    return arquivos

# Função para descompactar arquivos .gz (não .tar.gz)
def descompactar_gz(arquivo):
    print(f"Iniciando descompactação do arquivo .gz: {arquivo}")  # Mensagem de depuração
    with gzip.open(arquivo, 'rb') as f_in:
        nome_arquivo = arquivo[:-3]  # Remove a extensão '.gz'
        with open(nome_arquivo, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Arquivo descompactado: {nome_arquivo}")

# Função para filtrar arquivos potencialmente inseguros durante a extração
def filtro_seguro(tarinfo, path):
    print(f"Verificando arquivo: {tarinfo.name}")  # Mensagem de depuração
    # Aceita apenas arquivos que estão dentro do diretório atual
    if os.path.commonprefix([os.path.abspath(tarinfo.name), os.getcwd()]) == os.getcwd():
        return tarinfo
    else:
        print(f"Arquivo ignorado por motivo de segurança: {tarinfo.name}")  # Mensagem de depuração
        return None

# Função para descompactar arquivos .tar.gz com filtro de segurança
def descompactar_tar_gz(arquivo):
    print(f"Iniciando descompactação do arquivo .tar.gz: {arquivo}")  # Mensagem de depuração
    with tarfile.open(arquivo, "r:gz") as tar_ref:
        tar_ref.extractall(path=".", filter=filtro_seguro)  # Aplica o filtro de segurança
    print(f"Arquivo descompactado: {arquivo}")

# Função para descompactar arquivos .tar com filtro de segurança
def descompactar_tar(arquivo):
    print(f"Iniciando descompactação do arquivo .tar: {arquivo}")  # Mensagem de depuração
    with tarfile.open(arquivo, "r:") as tar_ref:
        tar_ref.extractall(path=".", filter=filtro_seguro)  # Aplica o filtro de segurança
    print(f"Arquivo descompactado: {arquivo}")

# Função principal que seleciona os arquivos e chama as funções de descompactação apropriadas
def descompactar_arquivos(arquivos):
    if not arquivos:
        print("Nenhum arquivo foi selecionado.")  # Mensagem de depuração
    for arquivo in arquivos:
        print(f"Processando o arquivo: {arquivo}")  # Mensagem de depuração
        if arquivo.endswith('.gz') and not arquivo.endswith('.tar.gz'):
            descompactar_gz(arquivo)
        elif arquivo.endswith('.tar.gz'):
            descompactar_tar_gz(arquivo)
        elif arquivo.endswith('.tar'):
            descompactar_tar(arquivo)
        else:
            print(f"Formato de arquivo {arquivo} não suportado!")  # Mensagem de depuração

# Função principal
def main():
    arquivos = selecionar_arquivos()
    if arquivos:
        descompactar_arquivos(arquivos)
    else:
        print("Nenhum arquivo selecionado.")  # Mensagem de depuração

# Executando o programa
if __name__ == "__main__":
    main()
