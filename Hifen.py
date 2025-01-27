import csv
import os
from tkinter import Tk, Button, Label, filedialog, messagebox

# Função para selecionar os arquivos CSV
def selecionar_arquivos():
    arquivos = filedialog.askopenfilenames(
        title="Selecione os arquivos CSV",
        filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*"))
    )
    if arquivos:
        label_arquivos_selecionados.config(text=f"{len(arquivos)} arquivo(s) selecionado(s)")
        global arquivos_csv
        arquivos_csv = arquivos

# Função para selecionar a pasta de saída
def selecionar_pasta_saida():
    pasta = filedialog.askdirectory(title="Selecione a pasta para salvar os arquivos modificados")
    if pasta:
        label_pasta_saida.config(text=pasta)
        global output_directory
        output_directory = pasta

# Função para processar os arquivos
def processar_arquivos():
    if not arquivos_csv or not output_directory:
        messagebox.showerror("Erro", "Selecione os arquivos e a pasta de saída!")
        return

    # Verifica se o diretório de saída existe, se não, cria ele
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Processa cada arquivo CSV selecionado
    for arquivo in arquivos_csv:
        # Nome do arquivo de saída
        nome_arquivo = os.path.basename(arquivo)
        output_file = os.path.join(output_directory, f"modificado_{nome_arquivo}")

        # Abre o arquivo original para leitura e o novo arquivo para escrita
        with open(arquivo, mode='r', newline='', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile, delimiter=';')
            writer = csv.writer(outfile, delimiter=';')

            # Itera sobre cada linha do arquivo original
            for row in reader:
                # Substitui os valores vazios por "-"
                modified_row = [cell if cell.strip() != '' else '-' for cell in row]
                # Escreve a linha modificada no novo arquivo
                writer.writerow(modified_row)

    messagebox.showinfo("Concluído", f"Arquivos processados e salvos em: {output_directory}")

# Configuração da interface gráfica
root = Tk()
root.title("Processador de Arquivos CSV")
root.geometry("500x200")

# Variáveis globais para armazenar os arquivos e a pasta de saída
arquivos_csv = []
output_directory = ""

# Botão para selecionar os arquivos CSV
Label(root, text="Arquivos CSV:").pack(pady=5)
label_arquivos_selecionados = Label(root, text="Nenhum arquivo selecionado", fg="blue")
label_arquivos_selecionados.pack(pady=5)
Button(root, text="Selecionar Arquivos CSV", command=selecionar_arquivos).pack(pady=5)

# Botão para selecionar a pasta de saída
Label(root, text="Pasta de Saída:").pack(pady=5)
label_pasta_saida = Label(root, text="Nenhuma pasta selecionada", fg="blue")
label_pasta_saida.pack(pady=5)
Button(root, text="Selecionar Pasta de Saída", command=selecionar_pasta_saida).pack(pady=5)

# Botão para processar os arquivos
Button(root, text="Processar Arquivos", command=processar_arquivos).pack(pady=20)

# Inicia a interface gráfica
root.mainloop()