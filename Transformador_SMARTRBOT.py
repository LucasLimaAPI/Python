import re
import pandas as pd
from tkinter import filedialog, Tk

# Função para processar o arquivo FIX
def processar_arquivo_fix(caminho_arquivo):
    """Processa arquivos FIX e extrai os dados"""
    with open(caminho_arquivo, 'rb') as arquivo:  # Abrir como binário para lidar com SOH (0x01)
        linhas = arquivo.read().split(b'\x01')  # Dividir o arquivo pelo delimitador SOH (0x01)

    dados_extraidos = []

    for linha in linhas:
        if not linha.strip():
            continue  # Ignorar linhas vazias

        # Processa cada linha para extrair tag e valor
        campos = linha.decode('utf-8').split('|')  # Converter para string e dividir pelas tags

        campo_dict = {}
        for campo in campos:
            if '=' in campo:
                tag, valor = campo.split('=', 1)
                campo_dict[tag] = valor

        # Agora extrair as informações do campo_dict
        # Adapte as tags conforme o formato real do seu arquivo FIX
        data = campo_dict.get('52', '').split('-')[0]  # Extrai a data do campo '52'
        hora = campo_dict.get('52', '').split('-')[1] if '52' in campo_dict else ''  # Hora do campo '52'

        # Criar o registro a ser adicionado
        registro = {
            "Código Participante": '93',
            "Plataforma de negociação": "SMARTBOT",
            "OMS": 'Trading Line Handler 11.1.2. 1049335',
            "Data": data,
            "Hora": hora,
            "ID da oferta": campo_dict.get('11', ''),
            "Id da oferta B3": campo_dict.get('17', ''),
            "Usuário": campo_dict.get('448', ''),
            "Código do Operador_Assessor": campo_dict.get('448', ''),
            "Código do cliente": campo_dict.get('1', ''),
            "Código Sessão": campo_dict.get('49', ''),
            "Status": campo_dict.get('35', ''),  # Evento extraído da tag 35 (por exemplo)
            "Origem da oferta": campo_dict.get('50', ''),
            "Time Zone": ''
        }

        dados_extraidos.append(registro)

    return dados_extraidos

# Função para processar arquivo CSV (não modificada)
def processar_arquivo_csv(caminho_arquivo):
    """Processa arquivos CSV e retorna os dados"""
    df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8')
    dados_extraidos = df.to_dict(orient='records')
    return dados_extraidos

# Função para salvar os dados em um arquivo CSV
def salvar_como_csv(dados, caminho_saida):
    """Salva os dados extraídos em um arquivo CSV"""
    df = pd.DataFrame(dados)

    # Organiza as colunas na ordem desejada
    colunas_ordenadas = [
        "Código Participante", "Plataforma de negociação", "OMS", "Data", "Hora", 
        "ID da oferta", "Id da oferta B3", "Usuário", "Código do Operador_Assessor", 
        "Código do cliente", "Código Sessão", "Status", "Origem da oferta", "Time Zone"
    ]

    colunas_presentes = [col for col in colunas_ordenadas if col in df.columns]
    df[colunas_presentes].to_csv(caminho_saida, index=False, sep=';', encoding='utf-8')
    print(f"Arquivo salvo com sucesso em: {caminho_saida}")

# Função principal
def main():
    Tk().withdraw()  # Oculta a janela principal do Tkinter
    
    caminhos_arquivos = filedialog.askopenfilenames(
        title="Selecione os arquivos", 
        filetypes=[("Arquivo FIX", "*.fix"), ("Arquivo CSV", "*.csv"), ("Todos os arquivos", "*.*")]
    )

    if not caminhos_arquivos:
        print("Nenhum arquivo selecionado.")
        return

    dados = []
    for caminho_arquivo in caminhos_arquivos:
        # Verifica a extensão do arquivo para processar adequadamente
        if caminho_arquivo.endswith('.fix'):
            dados.extend(processar_arquivo_fix(caminho_arquivo))  # Processa arquivos FIX
        elif caminho_arquivo.endswith('.csv'):
            dados.extend(processar_arquivo_csv(caminho_arquivo))  # Processa arquivos CSV

    if dados:
        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar arquivo CSV",
            defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv")]  # Tipo de arquivo para salvar
        )
        if caminho_saida:
            salvar_como_csv(dados, caminho_saida)  # Salva os dados extraídos no formato CSV
        else:
            print("Nenhum caminho de saída selecionado.")
    else:
        print("Nenhum dado foi extraído dos arquivos.")

if __name__ == "__main__":
    main()
