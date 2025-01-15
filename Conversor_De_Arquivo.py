import os
from tkinter import filedialog, Tk

# Função para selecionar múltiplos arquivos
def selecionar_arquivos():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    arquivos = filedialog.askopenfilenames(title="Selecione os arquivos", filetypes=[("Todos os Arquivos", "*.*")])
    return arquivos

# Função para renomear os arquivos com a extensão .FIX
def renomear_arquivos(arquivos):
    for arquivo in arquivos:
        # Obtém o caminho do arquivo sem a extensão
        nome_arquivo, ext = os.path.splitext(arquivo)
        
        # Define o novo nome com a extensão .FIX
        novo_nome = nome_arquivo + ".csv"
        
        # Renomeia o arquivo
        os.rename(arquivo, novo_nome)
        print(f"Arquivo renomeado: {arquivo} -> {novo_nome}")

# Função principal
def main():
    arquivos = selecionar_arquivos()
    if arquivos:
        renomear_arquivos(arquivos)
    else:
        print("Nenhum arquivo selecionado.")

# Executando o programa
if __name__ == "__main__":
    main()
