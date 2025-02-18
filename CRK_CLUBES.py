import pandas as pd
import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog, simpledialog

def read_excel(file_path):
    df = pd.read_excel(file_path, dtype=str).fillna('')
    df.columns = df.columns.str.strip().str.upper()
    df['VALOR LIQ'] = df['VALOR LIQ'].str.replace(',', '.').astype(float)
    return df

def read_base_xlsx(file_path):
    df = pd.read_excel(file_path, dtype=str).fillna('')
    df.columns = df.columns.str.strip().str.upper()
    df['ENDERECO'] = df['LOGRADOURO'] + ' ' + df['NUMERO'] + ' ' + df['COMPLEMENTO'] + ' ' + df['BAIRRO'] + ' ' + df['CIDADE'] + ' ' + df['UF']
    df['ENDERECO'] = df['ENDERECO'].str.strip()
    return df

def read_saldos_xlsx(file_path):
    df = pd.read_excel(file_path, dtype=str).fillna('0')
    df.columns = df.columns.str.strip().str.upper()
    return df

def get_month_index(month_abbr):
    meses = {'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6,
             'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12}
    return meses.get(month_abbr.upper(), 0)

import xml.etree.ElementTree as ET

def create_xml(converted_df, base_df, saldos_df, output_path, selected_month):
    root = ET.Element("eFinanceira")
    lote_eventos = ET.SubElement(root, "loteEventos")

    converted_df['COTISTA'] = converted_df['COTISTA'].str.strip().str.upper()
    base_df['COTISTA'] = base_df['COTISTA'].str.strip().str.upper()
    saldos_df['COTISTA'] = saldos_df['COTISTA'].str.strip().str.upper()

    aggregated_df = converted_df.groupby('COTISTA').agg({
        'VALOR LIQ': 'sum',
        'TIPO': lambda x: ', '.join(x)
    }).reset_index()

    mes_index = get_month_index(selected_month)
    encontrados = []
    nao_encontrados = []
    
    for _, row in aggregated_df.iterrows():
        cotista_id = row['COTISTA']
        base_info = base_df[base_df['COTISTA'] == cotista_id]
        if base_info.empty:
            nao_encontrados.append(cotista_id)
            continue
        
        encontrados.append(cotista_id)
        
        tot_creditos = converted_df.loc[(converted_df['COTISTA'] == cotista_id) & (converted_df['TIPO'] == 'C'), 'VALOR LIQ'].sum()
        tot_debitos = converted_df.loc[(converted_df['COTISTA'] == cotista_id) & (converted_df['TIPO'] == 'D'), 'VALOR LIQ'].sum()

        base_info = base_info.iloc[0]
        cpf = base_info['CPF']
        nome_cliente = base_info['NOME_CLIENTE']
        endereco = base_info['ENDERECO']
        sinacor = base_info['SINACOR']
        cnpj_fundo = base_info['CNPJ_FUNDO']
        data_nascimento = base_info['DATA_NASCIMENTO']
        
        tot_pgtos_acum = 0.00
        saldos_info = saldos_df[saldos_df['COTISTA'] == cotista_id]
        if not saldos_info.empty and mes_index > 0:
            saldos_info = saldos_info.iloc[0]
            tot_pgtos_acum = sum(float(saldos_info[col].replace(',', '.')) for col in saldos_info.index[1:mes_index+1])
        
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
        ET.SubElement(ide_declarado, "DataNasc").text = data_nascimento
        
        for tag in ["PaisEndereco", "PaisResid", "PaisNacionalidade"]:
            pais = ET.SubElement(ide_declarado, tag)
            ET.SubElement(pais, "Pais").text = "BR"
        
        mes_caixa = ET.SubElement(evt_mov, "mesCaixa")
        ET.SubElement(mes_caixa, "anoMesCaixa").text = "202408"#isso é manual 

        mov_op_fin = ET.SubElement(mes_caixa, "movOpFin")
        conta = ET.SubElement(mov_op_fin, "Conta")
        info_conta = ET.SubElement(conta, "infoConta")
        
        reportavel = ET.SubElement(info_conta, "Reportavel")
        ET.SubElement(reportavel, "Pais").text = "BR"

        ET.SubElement(info_conta, "tpConta").text = "3"
        ET.SubElement(info_conta, "subTpConta").text = "302"
        ET.SubElement(info_conta, "tpNumConta").text = "OECD601"
        ET.SubElement(info_conta, "numConta").text = f"BR{sinacor}{cnpj_fundo}"
        ET.SubElement(info_conta, "tpRelacaoDeclarado").text = "1"
        ET.SubElement(info_conta, "NoTitulares").text = "1"
        
        fundo = ET.SubElement(info_conta, "Fundo")
        ET.SubElement(fundo, "GIIN").text = ""
        ET.SubElement(fundo, "CNPJ").text = cnpj_fundo
        
        balanco = ET.SubElement(info_conta, "BalancoConta")
        ET.SubElement(balanco, "totCreditos").text = f"{tot_creditos:.2f}".replace('.', ',')
        ET.SubElement(balanco, "totDebitos").text = f"{tot_debitos:.2f}".replace('.', ',')
        ET.SubElement(balanco, "totCreditosMesmaTitularidade").text = "0,00"
        ET.SubElement(balanco, "totDebitosMesmaTitularidade").text = "0,00"

        pgtos_acum = ET.SubElement(info_conta, "PgtosAcum")
        if tot_pgtos_acum == 0.00:
            ET.SubElement(pgtos_acum, "tpPgto").text = "999"
        else:
            ET.SubElement(pgtos_acum, "tpPgto").text = "CRS503"
        ET.SubElement(pgtos_acum, "totPgtosAcum").text = f"{tot_pgtos_acum:.2f}".replace('.', ',')
    
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"✅ XML gerado com sucesso: {output_path}")
    print("🔍 Cotistas encontrados:", encontrados)
    print("❌ Cotistas não encontrados:", nao_encontrados)

root = Tk()
root.withdraw()
selected_month = simpledialog.askstring("Mês de Referência", "Digite o mês (ex: JAN, FEV, MAR...):")
converted_xlsx_path = filedialog.askopenfilename(title="Selecione o Excel convertido", filetypes=[("Excel", "*.xlsx")])
base_xlsx_path = filedialog.askopenfilename(title="Selecione a base de cotistas", filetypes=[("Excel", "*.xlsx")])
saldos_xlsx_path = filedialog.askopenfilename(title="Selecione o arquivo de saldos", filetypes=[("Excel", "*.xlsx")])
output_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML", "*.xml")])

if converted_xlsx_path and base_xlsx_path and saldos_xlsx_path and output_path and selected_month:
    converted_df = read_excel(converted_xlsx_path)
    base_df = read_base_xlsx(base_xlsx_path)
    saldos_df = read_saldos_xlsx(saldos_xlsx_path)
    create_xml(converted_df, base_df, saldos_df, output_path, selected_month)
else:
    print("❌ Operação cancelada pelo usuário.")
