import pandas as pd
from tkinter import Tk, filedialog

# Abre janela para selecionar o arquivo
Tk().withdraw()
file_path = filedialog.askopenfilename(title="Selecione o arquivo CSV", filetypes=[("CSV Files", "*.csv")])

# Lê o arquivo
df = pd.read_csv(file_path)

# Cria a coluna SUSPEITO
df['SUSPEITO'] = 'confiável'  # padrão

# Função para identificar o IP mais comum por USER
def analisar_user(user_df):
    ip_entries = user_df[(user_df['FIELD'].str.contains('IP', case=False)) & (user_df['ENTRADA'].notnull())]
    mac_entries = user_df[(user_df['FIELD'].str.contains('MAC', case=False)) & (user_df['ENTRADA'].notnull())]

    ip_mais_comum = ip_entries['ENTRADA'].mode()
    mac_mais_comum = mac_entries['ENTRADA'].mode()

    ip_mais_comum = ip_mais_comum.iloc[0] if not ip_mais_comum.empty else None
    mac_mais_comum = mac_mais_comum.iloc[0] if not mac_mais_comum.empty else None

    for idx, row in user_df.iterrows():
        if row['FIELD'].strip().upper().startswith('IP'):
            if ip_mais_comum and row['ENTRADA'] != ip_mais_comum:
                df.at[idx, 'SUSPEITO'] = 'suspeito'
        elif row['FIELD'].strip().upper().startswith('MAC'):
            if mac_mais_comum and row['ENTRADA'] != mac_mais_comum:
                df.at[idx, 'SUSPEITO'] = 'suspeito'

# Aplica a análise para cada USER individualmente
for user in df['USER'].unique():
    user_df = df[df['USER'] == user]
    analisar_user(user_df)

# Salva o arquivo
output_path = file_path.replace('.csv', '_analisado.csv')
df.to_csv(output_path, index=False)

print(f"Arquivo salvo com sucesso: {output_path}")
