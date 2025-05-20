import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from datetime import datetime

# Passo 1: Selecionar os arquivos
root = Tk()
root.withdraw()  # Esconde a janela principal do tkinter
file_paths = askopenfilenames(
    title="Selecione os arquivos de log",
    filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")]
)

# Passo 2: Ler todos os arquivos e concatenar os dados
df_list = []
for file_path in file_paths:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Formato de arquivo não suportado: {file_path}")
    df_list.append(df)

# Junta todos os dados
df_total = pd.concat(df_list, ignore_index=True)

# Passo 3: Cria pasta de saída
output_folder = os.path.join(os.path.dirname(file_paths[0]), "logs_por_usuario")
os.makedirs(output_folder, exist_ok=True)

# Passo 4: Agrupa os dados por usuário e salva
for user_id, user_data in df_total.groupby("USER"):
    safe_user_id = "".join(c for c in str(user_id) if c.isalnum() or c in (' ', '.', '_')).rstrip()
    user_file_name = f"user_{safe_user_id}.xlsx"
    output_path = os.path.join(output_folder, user_file_name)
    user_data.to_excel(output_path, index=False)

print(f"Planilhas geradas com sucesso em: {output_folder}")
