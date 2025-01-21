import os
from tkinter import Tk, filedialog

# Função para ler o conteúdo de um arquivo
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Função para processar o conteúdo e gerar o texto formatado
def process_content(content, file_name):
    lines = content.strip().split('\n')
    data_lines = lines[2:]  # Ignorando o cabeçalho
    formatted_content = [f"# Arquivo: {file_name}"]  # Adiciona o nome do arquivo como cabeçalho

    for line in data_lines:
        if 'MOVIMENTO' in line:
            formatted_content.append("#movimento")
        elif 'PAGAMENTO' in line:
            formatted_content.append("#pagamento")
        elif 'SALDO' in line:
            formatted_content.append("#saldo")
        formatted_content.append(line)

    return "\n".join(formatted_content)

# Abrindo a interface para selecionar os arquivos
root = Tk()
root.withdraw()  # Esconde a janela principal do Tkinter
file_paths = filedialog.askopenfilenames(title="Selecione os arquivos", filetypes=[("Todos os arquivos", "*.*")])

# Processando cada arquivo selecionado e armazenando o conteúdo formatado
all_formatted_content = []
for file_path in file_paths:
    file_name = os.path.basename(file_path)  # Obtém o nome do arquivo
    content = read_file(file_path)
    formatted_content = process_content(content, file_name)
    all_formatted_content.append(formatted_content)

# Juntando todo o conteúdo formatado
final_content = "\n\n".join(all_formatted_content)  # Separa os arquivos com uma linha em branco

# Escrevendo o conteúdo formatado em um novo arquivo
output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de texto", "*.txt")], title="Salvar arquivo formatado como")
if output_file_path:
    with open(output_file_path, "w", encoding="utf-8") as final_file:
        final_file.write(final_content)
    print(f"Arquivo '{output_file_path}' gerado com sucesso!")
else:
    print("Operação cancelada pelo usuário.")