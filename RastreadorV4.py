import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def selecionar_arquivos():
    root = tk.Tk()
    root.withdraw()
    arquivos = filedialog.askopenfilenames(
        title="Selecione os arquivos CSV ou Excel",
        filetypes=[("Arquivos CSV/Excel", "*.csv *.xlsx *.xls")]
    )
    return root.tk.splitlist(arquivos)

def juntar_arquivos_por_USER(arquivos):
    df_base = pd.DataFrame()
    df_info_extra = pd.DataFrame()

    for arquivo in arquivos:
        try:
            if arquivo.endswith('.csv'):
                df = pd.read_csv(arquivo, encoding='utf-8', sep=None, engine='python')
            else:
                df = pd.read_excel(arquivo, engine='openpyxl')

            colunas = [c.upper().strip() for c in df.columns]

            if all(c in colunas for c in ["ID", "USER", "TIPO", "DATA", "FIELD", "ENTRADA"]):
                df.columns = colunas
                df_base = pd.concat([df_base, df], ignore_index=True)
            elif all(c in colunas for c in ["USER", "IP", "STATUS"]):
                df.columns = colunas
                df_info_extra = pd.concat([df_info_extra, df], ignore_index=True)

        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")

    # Merge com base no USER
    if not df_info_extra.empty:
        df_final = pd.merge(df_base, df_info_extra, on="USER", how="left")
    else:
        df_final = df_base

    return df_final

def salvar_arquivo(df_final):
    root = tk.Tk()
    root.withdraw()
    caminho_saida = filedialog.asksaveasfilename(
        defaultextension=".csv",  # muda o padrão para CSV
        filetypes=[("CSV", "*.csv")],
        title="Salvar arquivo combinado"
    )

    if caminho_saida:
        try:
            df_final.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso:\n{caminho_saida}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo:\n{e}")


def main():
    arquivos = selecionar_arquivos()
    if not arquivos:
        messagebox.showwarning("Aviso", "Nenhum arquivo foi selecionado.")
        return

    df_final = juntar_arquivos_por_USER(arquivos)

    if df_final.empty:
        messagebox.showwarning("Aviso", "Nenhum dado foi carregado dos arquivos.")
    else:
        salvar_arquivo(df_final)

if __name__ == "__main__":
    main()
