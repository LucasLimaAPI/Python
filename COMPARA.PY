import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import pandas as pd

def selecionar_arquivo():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos XML", "*.xml")])
    return arquivo

def comparar_xmls(xml1_path, xml2_path, output_excel):
    tree1 = ET.parse(xml1_path)
    root1 = tree1.getroot()
    tree2 = ET.parse(xml2_path)
    root2 = tree2.getroot()
    
    # Coletando os NIDeclarado do segundo XML
    ni_declarados_xml2 = {elem.text for elem in root2.findall(".//{*}NIDeclarado")}
    
    repetidos = []

    for ni_elem in root1.findall(".//{*}NIDeclarado"):
        if ni_elem is not None and ni_elem.text in ni_declarados_xml2:
            repetidos.append(ni_elem.text)

    # Verifica se encontrou algum valor antes de salvar
    if repetidos:
        df = pd.DataFrame(repetidos, columns=["NIDeclarado Repetido"])
        df.to_excel(output_excel, index=False)
        print(f"Excel salvo em: {output_excel}")
    else:
        print("Nenhum NIDeclarado repetido foi encontrado.")

# Criar interface Tkinter
root = tk.Tk()
root.withdraw()

print("Selecione o primeiro XML (com mais informações)")
xml1_path = selecionar_arquivo()

print("Selecione o segundo XML (com menos informações)")
xml2_path = selecionar_arquivo()

output_excel = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])

if xml1_path and xml2_path and output_excel:
    comparar_xmls(xml1_path, xml2_path, output_excel)
else:
    print("Seleção cancelada.")
