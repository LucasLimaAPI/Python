import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime

# Passo 1: Selecionar o arquivo
root = Tk()
root.withdraw()  # Esconde a janela principal do tkinter
file_path = askopenfilename(title="Selecione o arquivo de log", filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")])

# Verifica extensão para ler corretamente
ext = os.path.splitext(file_path)[1].lower()
if ext == '.csv':
    df = pd.read_csv(file_path)
elif ext in ['.xls', '.xlsx']:
    df = pd.read_excel(file_path)
else:
    raise ValueError("Formato de arquivo não suportado")

# Passo 2: Cria pasta de saída
output_folder = os.path.join(os.path.dirname(file_path), "logs_por_usuario")
os.makedirs(output_folder, exist_ok=True)

# Passo 3: Agrupa os dados por usuário
for user_id, user_data in df.groupby("USER"):
    user_file_name = f"user_{user_id}.xlsx"
    output_path = os.path.join(output_folder, user_file_name)
    user_data.to_excel(output_path, index=False)

print(f"Planilhas geradas com sucesso em: {output_folder}")
