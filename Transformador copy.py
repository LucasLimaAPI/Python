import re
import pandas as pd
from tkinter import filedialog, Tk

def processar_arquivo_log(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    dados_extraidos = []

    padrao = re.compile(r"(?P<hora>\d{2}:\d{2}:\d{2}:\d{3})==>?#?(?P<evento>\w+)\s(?P<campos>.+)")

    for linha in linhas:
        match = padrao.search(linha)
        if '#' not in linha[0]:

            #hora = match.group('hora')
            evento = match.group('evento')
            #campos = match.group('campos').split('|')


            teste = linha.split("|")
            
            campo_dict = {campo.split('=')[0]: campo.split('=')[1] for campo in teste if '=' in campo}

            data = campo_dict['52'].split('-')[0]
            hora = (campo_dict['52'].split('-')[1])


            registro = {
                "Código Participante": '93',
                "Plataforma de negociação": "VALDI TRADER",
                "OMS": 'Trading Line Handler 11.1.2. 1049335',
                "Data": data,
                "Hora": hora,
                "ID da oferta": campo_dict.get('11', ''),
                "Id da oferta B3": campo_dict.get('17', ''),
                "Usuário": campo_dict.get('448', ''),
                "Código do Operador_Assessor": campo_dict.get('448', ''),
                "Código do cliente": campo_dict.get('1', ''),
                "Código Sessão": campo_dict.get('49', ''),
                "Status": evento,
                "Origem da oferta":campo_dict.get('50', ''),
                "Time Zone": ''
            }
            
            dados_extraidos.append(registro)

    return dados_extraidos

def salvar_como_csv(dados, caminho_saida):
    df = pd.DataFrame(dados)

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
        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar arquivo CSV",
            defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv")]
        )
        if caminho_saida:
            salvar_como_csv(dados, caminho_saida)
        else:
            print("Nenhum caminho de saída selecionado.")
    else:
        print("Nenhum dado foi extraído dos arquivos.")

if __name__ == "__main__":
    main()
