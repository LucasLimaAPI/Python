import os
from tkinter import filedialog, Tk

# Função para selecionar arquivos
def selecionar_arquivos():
    root = Tk()
    root.withdraw()  # Oculta a janela principal
    arquivos = filedialog.askopenfilenames(title="Selecione os arquivos", filetypes=[("Todos os Arquivos", "*.*")])
    return arquivos

# Função para renomear arquivos
def renomear_arquivos(arquivos):
    if not arquivos:
        print("Nenhum arquivo selecionado.")
        return
    
    nome_base = input("Digite o nome base para os arquivos: ")
    
    for i, arquivo in enumerate(arquivos, 1):
        # Extrai o diretório e a extensão do arquivo
        diretório, nome_arquivo = os.path.split(arquivo)
        nome, ext = os.path.splitext(nome_arquivo)
        
        # Cria o novo nome sequencial
        novo_nome = f"{nome_base}_{i}{ext}"
        
        # Caminho completo do novo arquivo
        novo_caminho = os.path.join(diretório, novo_nome)
        
        # Verifica se o arquivo existe antes de renomear
        if os.path.exists(arquivo):
            os.rename(arquivo, novo_caminho)
            print(f"Arquivo renomeado para: {novo_caminho}")
        else:
            print(f"O arquivo {arquivo} não foi encontrado.")
        
# Função principal
def main():
    arquivos = selecionar_arquivos()
    renomear_arquivos(arquivos)
    print("Todos os arquivos foram processados!")

if __name__ == "__main__":
    main()
