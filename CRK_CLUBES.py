import pandas as pd
import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog

# 📌 Função para ler o Excel convertido do TXT
def read_excel(file_path):
    df = pd.read_excel(file_path, dtype=str).fillna('')  # Lê o Excel
    df.columns = df.columns.str.strip().str.upper()  # Normaliza os nomes das colunas
    print("🔍 Colunas do arquivo convertido:", df.columns.tolist())

    if 'COTISTA' not in df.columns or 'VALOR LIQ' not in df.columns:
        raise KeyError("⚠️ A coluna 'COTISTA' ou 'VALOR LIQ' não foi encontrada no arquivo Excel.")

    df['VALOR LIQ'] = df['VALOR LIQ'].str.replace(',', '.').astype(float)  # Corrige a formatação do valor
    return df

# 📌 Função para ler a base de cotistas
def read_base_xlsx(file_path):
    df = pd.read_excel(file_path, dtype=str).fillna('')  # Lê os dados
    df.columns = df.columns.str.strip().str.upper()  # Normaliza os nomes das colunas

    required_columns = ['COTISTA', 'CPF', 'NOME_CLIENTE', 'LOGRADOURO', 'NUMERO', 'COMPLEMENTO',
                        'BAIRRO', 'CIDADE', 'UF', 'SINACOR', 'CNPJ_FUNDO']
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise KeyError(f"⚠️ Colunas ausentes no arquivo base: {missing_cols}")

    df['ENDERECO'] = df['LOGRADOURO'] + ' ' + df['NUMERO'] + ' ' + df['COMPLEMENTO'] + ' ' + df['BAIRRO'] + ' ' + df['CIDADE'] + ' ' + df['UF']
    df['ENDERECO'] = df['ENDERECO'].str.strip()

    # Depuração - Exibindo as colunas e os primeiros cotistas
    print(f"🔍 Colunas do arquivo base: {df.columns.tolist()}")
    print(f"🔍 COTISTAS na base: {df['COTISTA'].head(20).tolist()}")

    return df


# 📌 Criar XML corretamente associando os cotistas do TXT com a base
def create_xml(converted_df, base_df, output_path):
    root = ET.Element("eFinanceira")
    lote_eventos = ET.SubElement(root, "loteEventos")

    # Garantir que ambos os campos 'COTISTA' estejam no mesmo formato (remover espaços extras, maiúsculas)
    converted_df['COTISTA'] = converted_df['COTISTA'].str.strip().str.upper()
    base_df['COTISTA'] = base_df['COTISTA'].str.strip().str.upper()

    # Depuração para imprimir os valores de COTISTA e ver se há alguma diferença
    print("🔍 COTISTAS no arquivo convertido:", converted_df['COTISTA'].tolist())
    print("🔍 COTISTAS na base:", base_df['COTISTA'].tolist())

    if base_df.empty:
        print("⚠️ Nenhum cotista encontrado na base!")
        return

    # Gerando o XML
    for _, row in converted_df.iterrows():
        cotista_id = row['COTISTA']

        # Verificar se o cotista está na base
        base_info = base_df[base_df['COTISTA'] == cotista_id]
        if base_info.empty:
            print(f"⚠️ Cotista {cotista_id} não encontrado na base, ignorando...")
            continue

        tot_creditos = converted_df.loc[(converted_df['COTISTA'] == cotista_id) & (converted_df['TIPO'] == 'C'), 'VALOR LIQ'].sum()
        tot_debitos = converted_df.loc[(converted_df['COTISTA'] == cotista_id) & (converted_df['TIPO'] == 'D'), 'VALOR LIQ'].sum()

        # Busca as informações do cotista na base
        base_info = base_info.iloc[0]  # Pega a primeira linha que corresponde
        cpf = base_info['CPF']
        nome_cliente = base_info['NOME_CLIENTE']
        endereco = base_info['ENDERECO']
        sinacor = base_info['SINACOR']
        cnpj_fundo = base_info['CNPJ_FUNDO']

        evento = ET.SubElement(lote_eventos, "evento", id=f"ID{cotista_id}")
        efin = ET.SubElement(evento, "eFinanceira")
        evt_mov = ET.SubElement(efin, "evtMovOpFin", id=f"ID{cotista_id}")

        ide_evento = ET.SubElement(evt_mov, "ideEvento")
        ET.SubElement(ide_evento, "indRetificacao").text = "1"
        ET.SubElement(ide_evento, "tpAmb").text = "1"
        ET.SubElement(ide_evento, "aplicEmi").text = "2"
        ET.SubElement(ide_evento, "verAplic").text = "ATLAS/PAS"

        ide_declarante = ET.SubElement(evt_mov, "ideDeclarante")
        ET.SubElement(ide_declarante, "cnpjDeclarante").text = "04257795000179"

        ide_declarado = ET.SubElement(evt_mov, "ideDeclarado")
        ET.SubElement(ide_declarado, "tpNI").text = "1"
        ET.SubElement(ide_declarado, "NIDeclarado").text = cpf
        ET.SubElement(ide_declarado, "NomeDeclarado").text = nome_cliente
        ET.SubElement(ide_declarado, "EnderecoLivre").text = endereco

        info_conta = ET.SubElement(evt_mov, "movOpFin")
        conta = ET.SubElement(info_conta, "Conta")
        info_conta = ET.SubElement(conta, "infoConta")
        ET.SubElement(info_conta, "Reportavel").text = "BR"
        ET.SubElement(info_conta, "tpConta").text = "3"
        ET.SubElement(info_conta, "subTpConta").text = "302"
        ET.SubElement(info_conta, "tpNumConta").text = "OECD601"
        ET.SubElement(info_conta, "numConta").text = sinacor

        fundo = ET.SubElement(info_conta, "Fundo")
        ET.SubElement(fundo, "GIIN").text = ""
        ET.SubElement(fundo, "CNPJ").text = cnpj_fundo

        balanco = ET.SubElement(info_conta, "BalancoConta")
        ET.SubElement(balanco, "totCreditos").text = f"{tot_creditos:.2f}".replace('.', ',')
        ET.SubElement(balanco, "totDebitos").text = f"{tot_debitos:.2f}".replace('.', ',')

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"✅ XML gerado com sucesso: {output_path}")


# 📌 Interface para selecionar arquivos
root = Tk()
root.withdraw()
converted_xlsx_path = filedialog.askopenfilename(title="Selecione o Excel convertido do TXT", filetypes=[("Excel", "*.xlsx")])
base_xlsx_path = filedialog.askopenfilename(title="Selecione a base de cotistas", filetypes=[("Excel", "*.xlsx")])
output_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML", "*.xml")])

if converted_xlsx_path and base_xlsx_path and output_path:
    converted_df = read_excel(converted_xlsx_path)
    base_df = read_base_xlsx(base_xlsx_path)
    create_xml(converted_df, base_df, output_path)
else:
    print("❌ Operação cancelada pelo usuário.")
