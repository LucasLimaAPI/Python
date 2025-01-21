import pandas as pd
import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog
from collections import defaultdict

# Função para ler o arquivo XLSX
def read_xlsx(file_path):
    return pd.read_excel(file_path)

# Função para ler o arquivo TXT e extrair as informações
def read_txt(file_path):
    dados = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            linha = line.strip()  # Remove espaços em branco no início e no fim
            if linha:  # Ignora linhas vazias
                # Divide a linha com base no separador ";"
                partes = linha.split(';')
                if len(partes) >= 1:  # Verifica se a linha tem pelo menos uma parte
                    nome = partes[0].strip()  # Nome é a primeira parte
                    cpf_cnpj = partes[1].strip() if len(partes) > 1 else ""  # CPF/CNPJ é a segunda parte (se existir)
                    tipo = partes[2].strip() if len(partes) > 2 else ""  # Tipo é a terceira parte (se existir)
                    data = partes[3].strip() if len(partes) > 3 else ""  # Data é a quarta parte (se existir)
                    
                    # Trata o valor como float, substituindo vírgula por ponto e lidando com valores vazios
                    valor_str = partes[4].strip().replace(',', '.') if len(partes) > 4 and partes[4].strip() else "0"
                    try:
                        valor = float(valor_str)  # Converte para float
                    except ValueError:
                        valor = 0.0  # Define como 0.0 se a conversão falhar
                    
                    dados.append({"Nome": nome, "CPF/CNPJ": cpf_cnpj, "Tipo": tipo, "Data": data, "Valor": valor})
    return dados

# Função para processar os dados e calcular os totais de créditos e débitos
def calcular_totais(dados):
    totais = defaultdict(lambda: {'creditos': 0.0, 'debitos': 0.0})  # Usamos float para valores decimais
    for item in dados:
        nome = item["Nome"]
        cpf = item["CPF/CNPJ"]
        tipo = item["Tipo"]
        valor = item["Valor"]
        
        if tipo == 'C':
            totais[(nome, cpf)]['creditos'] += valor
        elif tipo == 'D':
            totais[(nome, cpf)]['debitos'] += valor
    return totais

# Função para criar o XML
def create_xml(txt_data, df, output_file_path):
    # Cria o elemento raiz do XML
    root = ET.Element("root")

    # Calcula os totais de créditos e débitos
    totais = calcular_totais(txt_data)

    for (nome, cpf), valores in totais.items():
        print(f"Processando Nome: {nome}, CPF/CNPJ: {cpf}")  # Depuração

        # Busca informações no Excel (ignorando diferenças de maiúsculas/minúsculas)
        cliente_info = df[df['NOME_CLIENTE'].str.strip().str.upper() == nome.strip().upper()]

        if not cliente_info.empty:
            print(f"Informações encontradas no Excel para {nome}.")  # Depuração

            # Cria um novo evento
            evt = ET.SubElement(root, "evtMovOpFin")

            # Adiciona subelementos ao evento
            ide_evento = ET.SubElement(evt, "ideEvento")
            ET.SubElement(ide_evento, "indRetificacao").text = "1"  # FALTA
            ET.SubElement(ide_evento, "tpAmb").text = "1"  # FALTA
            ET.SubElement(ide_evento, "aplicEmi").text = "2"  # FALTA
            ET.SubElement(ide_evento, "verAplic").text = "ATLAS/PAS"  # FALTA

            ide_declarante = ET.SubElement(evt, "ideDeclarante")
            ET.SubElement(ide_declarante, "cnpjDeclarante").text = "04257795000179"

            ide_declarado = ET.SubElement(evt, "ideDeclarado")
            ET.SubElement(ide_declarado, "tpNI").text = "1"
            ET.SubElement(ide_declarado, "NIDeclarado").text = str(cpf)  # Converte para string
            ET.SubElement(ide_declarado, "NomeDeclarado").text = nome

            # Concatena todas as informações de endereço em um único campo
            endereco = []
            if 'LOGRADOURO' in df.columns:
                endereco.append(str(cliente_info['LOGRADOURO'].values[0]))
            if 'NUMERO' in df.columns:
                endereco.append(str(cliente_info['NUMERO'].values[0]))
            if 'COMPLEMENTO' in df.columns:
                endereco.append(str(cliente_info['COMPLEMENTO'].values[0]))
            if 'BAIRRO' in df.columns:
                endereco.append(str(cliente_info['BAIRRO'].values[0]))
            if 'CIDADE' in df.columns:
                endereco.append(str(cliente_info['CIDADE'].values[0]))
            if 'ESTADO' in df.columns:
                endereco.append(str(cliente_info['ESTADO'].values[0]))

            endereco_completo = ", ".join(filter(None, endereco))  # Concatena as informações, ignorando valores vazios
            ET.SubElement(ide_declarado, "EnderecoLivre").text = endereco_completo

            ET.SubElement(ide_declarado, "PaisEndereco").text = "BR"
            ET.SubElement(ide_declarado, "PaisResid").text = "BR"
            ET.SubElement(ide_declarado, "PaisNacionalidade").text = "BR"

            mes_caixa = ET.SubElement(evt, "mesCaixa")
            ET.SubElement(mes_caixa, "anoMesCaixa").text = "202407"  # COLOCAR NA MÃO

            mov_op_fin = ET.SubElement(mes_caixa, "movOpFin")
            conta = ET.SubElement(mov_op_fin, "Conta")
            info_conta = ET.SubElement(conta, "infoConta")
            ET.SubElement(info_conta, "Reportavel").text = "BR"
            ET.SubElement(info_conta, "tpConta").text = ""  # FALTA
            ET.SubElement(info_conta, "subTpConta").text = ""  # FALTA
            ET.SubElement(info_conta, "tpNumConta").text = ""  # FALTA
            ET.SubElement(info_conta, "numConta").text = str(cliente_info['Conta'].values[0])  # Converte para string
            ET.SubElement(info_conta, "tpRelacaoDeclarado").text = "1"
            ET.SubElement(info_conta, "NoTitulares").text = "1"

            fundo = ET.SubElement(info_conta, "Fundo")
            ET.SubElement(fundo, "GIIN").text = ""
            ET.SubElement(fundo, "CNPJ").text = str(cpf)  # Converte para string

            balanco_conta = ET.SubElement(info_conta, "BalancoConta")
            ET.SubElement(balanco_conta, "totCreditos").text = f"{valores['creditos']:.2f}"  # Formata para 2 casas decimais
            ET.SubElement(balanco_conta, "totDebitos").text = f"{valores['debitos']:.2f}"  # Formata para 2 casas decimais
            ET.SubElement(balanco_conta, "totCreditosMesmaTitularidade").text = "0,00"  # Precisa arrumar
            ET.SubElement(balanco_conta, "totDebitosMesmaTitularidade").text = "0,00"  # Precisa arrumar

            pgtos_acum = ET.SubElement(info_conta, "PgtosAcum")
            ET.SubElement(pgtos_acum, "tpPgto").text = "CRS503"
            ET.SubElement(pgtos_acum, "totPgtosAcum").text = "1014,52"
        else:
            print(f"Nenhuma informação encontrada no Excel para {nome}.")  # Depuração

    # Salva o novo arquivo XML
    tree = ET.ElementTree(root)
    with open(output_file_path, 'wb') as file:
        tree.write(file, encoding='utf-8', xml_declaration=True)
    print(f"Novo arquivo XML salvo em: {output_file_path}")

# Interface para selecionar arquivos
root = Tk()
root.withdraw()

# Selecionar o arquivo XLSX
xlsx_file_path = filedialog.askopenfilename(title="Selecione o arquivo XLSX", filetypes=[("Arquivos Excel", "*.xlsx")])
if not xlsx_file_path:
    print("Nenhum arquivo XLSX selecionado.")
    exit()

# Selecionar o arquivo TXT
txt_file_path = filedialog.askopenfilename(title="Selecione o arquivo TXT", filetypes=[("Arquivos de texto", "*.txt")])
if not txt_file_path:
    print("Nenhum arquivo TXT selecionado.")
    exit()

# Ler os arquivos
df = read_xlsx(xlsx_file_path)
txt_data = read_txt(txt_file_path)

# Verificar se os dados foram lidos corretamente
print("Dados do Excel:")
print(df.head())  # Exibe as primeiras linhas do Excel para depuração
print("\nDados do TXT:")
print(txt_data)  # Exibe os dados lidos do TXT para depuração

# Verificar se as colunas necessárias estão presentes no Excel
colunas_necessarias = ['NOME_CLIENTE', 'CPF/CNPJ', 'LOGRADOURO', 'NUMERO', 'COMPLEMENTO', 'BAIRRO', 'CIDADE', 'ESTADO', 'Conta']
if not all(coluna in df.columns for coluna in colunas_necessarias):
    print("Erro: O arquivo Excel não contém todas as colunas necessárias.")
    exit()

# Salvar o novo arquivo XML
output_file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("Arquivos XML", "*.xml")], title="Salvar novo XML como")
if output_file_path:
    create_xml(txt_data, df, output_file_path)
else:
    print("Operação cancelada pelo usuário.")