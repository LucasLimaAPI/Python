import re
import pandas as pd
from tkinter import filedialog, Tk

def verificar_codigo_sessao(campo_dict):
    codigo_49 = campo_dict.get('49', '-')
    
    if codigo_49 in ['OE204', 'OE124']:
        codigo_56 = campo_dict.get('56', '-')
        
        if codigo_56 == 'OE124':
            return campo_dict.get('49', '-')
        return codigo_56
        
    return codigo_49

def processar_arquivo_log(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    dados_extraidos = []
    padrao = re.compile(r"(?P<hora>\d{2}:\d{2}:\d{2}:\d{3})==>?#?(?P<evento>\w+)\s(?P<campos>.+)")

    for linha in linhas:
        match = padrao.search(linha)
        if '#' not in linha[0]:
            evento = match.group('evento')
            teste = linha.split("|")
            
            campo_dict = {campo.split('=')[0]: campo.split('=')[1] for campo in teste if '=' in campo}

            data = campo_dict['52'].split('-')[0]
            hora = (campo_dict['52'].split('-')[1])

            codigo_sessao = verificar_codigo_sessao(campo_dict)

            registro = {
                "Código Participante": '93',
                "Plataforma de negociação": "VALDI TRADER",
                "OMS": 'Trading Line Handler 11.1.2. 1049335',
                "Data": data,
                "Hora": hora,
                "ID da oferta": campo_dict.get('11', '-'),
                "Id da oferta B3": campo_dict.get('17', '-'),
                "Usuário": campo_dict.get('448', ''),
                "Código do Operador_Assessor": campo_dict.get('448', '-'),
                "Código do cliente": campo_dict.get('1', '-'),
                "Código Sessão": codigo_sessao,
                "Status": campo_dict.get('39', '-'),
                "Origem da oferta": campo_dict.get('50', '-'),
                "Time Zone": '-'
            }
            
            dados_extraidos.append(registro)

    return dados_extraidos

def processar_dados(dados):
    # Converter para DataFrame
    df = pd.DataFrame(dados)
    
    # Criar um dicionário para armazenar as origens da oferta por ID
    origens_por_id = {}
    
    # Primeiro passo: identificar todas as origens de oferta não vazias
    for idx, row in df.iterrows():
        id_oferta = row['ID da oferta']
        origem = row['Origem da oferta']
        if origem != '-' and id_oferta != '-':
            origens_por_id[id_oferta] = origem
    
    # Segundo passo: preencher as origens vazias usando o dicionário
    df['Origem da oferta'] = df.apply(
        lambda row: origens_por_id.get(row['ID da oferta'], row['Origem da oferta'])
        if row['ID da oferta'] != '-' else row['Origem da oferta'],
        axis=1
    )
    
    # Agrupar registros similares
    # Primeiro, identifique as colunas que devem ser únicas por grupo
    colunas_agrupamento = ['ID da oferta', 'Id da oferta B3', 'Código do cliente']
    
    # Agrupe e mantenha o primeiro valor não vazio para cada coluna
    df_agrupado = df.groupby(colunas_agrupamento, as_index=False).agg({
        'Código Participante': 'first',
        'Plataforma de negociação': 'first',
        'OMS': 'first',
        'Data': 'first',
        'Hora': 'min',  # Pega o primeiro horário
        'Usuário': lambda x: x.iloc[0] if x.iloc[0] != '-' else x.iloc[-1],
        'Código do Operador_Assessor': lambda x: x.iloc[0] if x.iloc[0] != '-' else x.iloc[-1],
        'Código Sessão': lambda x: x.iloc[0] if x.iloc[0] != '-' else x.iloc[-1],
        'Status': lambda x: x.iloc[-1],  # Pega o último status
        'Origem da oferta': lambda x: x.iloc[0] if x.iloc[0] != '-' else x.iloc[-1],
        'Time Zone': 'first'
    })
    
    return df_agrupado

def salvar_como_csv(df, caminho_saida):
    colunas_ordenadas = [
        "Código Participante", "Plataforma de negociação", "OMS", "Data", "Hora", 
        "ID da oferta", "Id da oferta B3", "Usuário", "Código do Operador_Assessor", 
        "Código do cliente", "Código Sessão", "Status", "Origem da oferta", "Time Zone"
    ]

    colunas_presentes = [col for col in colunas_ordenadas if col in df.columns]
    df[colunas_presentes].to_csv(caminho_saida, index=False, sep=';', encoding='utf-8')
    print(f"Arquivo salvo com sucesso em: {caminho_saida}")

def main():
    Tk().withdraw()
    caminhos_arquivos = filedialog.askopenfilenames(
        title="Selecione os arquivos de log", 
        filetypes=[("Arquivo de log", "*.log"), ("Todos os arquivos", "*.*")]
    )

    if not caminhos_arquivos:
        print("Nenhum arquivo selecionado.")
        return

    dados = []
    for caminho_arquivo in caminhos_arquivos:
        dados.extend(processar_arquivo_log(caminho_arquivo))

    if dados:
        # Processar os dados para agrupar e preencher informações
        df_processado = processar_dados(dados)
        
        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar arquivo CSV",
            defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv")]
        )
        if caminho_saida:
            salvar_como_csv(df_processado, caminho_saida)
        else:
            print("Nenhum caminho de saída selecionado.")
    else:
        print("Nenhum dado foi extraído dos arquivos.")

if __name__ == "__main__":
    main()