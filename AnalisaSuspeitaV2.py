import pandas as pd
from tkinter import Tk, filedialog

# Abre janela para selecionar o arquivo
Tk().withdraw()
file_path = filedialog.askopenfilename(title="Selecione o arquivo CSV", filetypes=[("CSV Files", "*.csv")])

# Lê o arquivo CSV
df = pd.read_csv(file_path)

# Cria as colunas
df['SUSPEITO'] = 'confiável'
df['MOTIVO'] = ''

# Função para analisar por usuário
def analisar_user(user_df):
    ip_entries = user_df[(user_df['FIELD'].str.contains('IP', case=False)) & (user_df['ENTRADA'].notnull())]
    mac_entries = user_df[(user_df['FIELD'].str.contains('MAC', case=False)) & (user_df['ENTRADA'].notnull())]

    ip_mais_comum = ip_entries['ENTRADA'].mode()
    mac_mais_comum = mac_entries['ENTRADA'].mode()

    ip_mais_comum = ip_mais_comum.iloc[0] if not ip_mais_comum.empty else None
    mac_mais_comum = mac_mais_comum.iloc[0] if not mac_mais_comum.empty else None

    for idx, row in user_df.iterrows():
        field = row['FIELD'].strip().upper()
        entrada = row['ENTRADA']

        if field.startswith('IP') and ip_mais_comum and entrada != ip_mais_comum:
            df.at[idx, 'SUSPEITO'] = 'suspeito'
            df.at[idx, 'MOTIVO'] = f"IP diferente do mais comum ({ip_mais_comum}) para o usuário"
        elif field.startswith('MAC') and mac_mais_comum and entrada != mac_mais_comum:
            df.at[idx, 'SUSPEITO'] = 'suspeito'
            df.at[idx, 'MOTIVO'] = f"MAC address diferente do mais comum ({mac_mais_comum}) para o usuário"

# Executa a análise por usuário
for user in df['USER'].unique():
    user_df = df[df['USER'] == user]
    analisar_user(user_df)

# Salva a nova versão
output_path = file_path.replace('.csv', '_analisado_com_motivo.csv')
df.to_csv(output_path, index=False)

print(f"Análise concluída! Arquivo salvo em: {output_path}")
