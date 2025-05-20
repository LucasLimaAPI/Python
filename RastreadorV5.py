import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict

def selecionar_arquivos():
    root = tk.Tk()
    root.withdraw()
    arquivos = filedialog.askopenfilenames(
        title="Selecione os arquivos CSV ou Excel",
        filetypes=[("Arquivos CSV ou Excel", "*.csv *.xlsx *.xls")]
    )
    return arquivos

def ler_arquivo(caminho):
    try:
        if caminho.endswith('.csv'):
            return pd.read_csv(caminho, encoding='utf-8')
        elif caminho.endswith('.xlsx') or caminho.endswith('.xls'):
            return pd.read_excel(caminho)
        else:
            return None
    except Exception as e:
        messagebox.showerror("Erro ao ler arquivo", f"{caminho}\n\n{e}")
        return None

def salvar_como_csv(df_final):
    root = tk.Tk()
    root.withdraw()
    caminho_saida = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv")],
        title="Salvar arquivo analisado"
    )

    if caminho_saida:
        try:
            df_final.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso:\n{caminho_saida}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo:\n{e}")

def analisar_suspeitos(df):
    df = df.copy()
    df['FIELD'] = df['FIELD'].astype(str).str.upper()

    # Criar dicionários: {user: [ips]}, {user: [macs]}
    user_ips = defaultdict(list)
    user_macs = defaultdict(list)

    for _, row in df.iterrows():
        user = row.get("USER")
        field = row.get("FIELD")
        valor = str(row.get("ENTRADA"))

        if field == "IP":
            user_ips[user].append(valor)
        elif field == "MAC ADDRESS":
            user_macs[user].append(valor)

    # Obter IP/MAC mais frequente por usuário
    user_main_ip = {u: pd.Series(v).mode()[0] if v else None for u, v in user_ips.items()}
    user_main_mac = {u: pd.Series(v).mode()[0] if v else None for u, v in user_macs.items()}

    # Inverter: ip -> [users], mac -> [users]
    ip_to_users = defaultdict(set)
    mac_to_users = defaultdict(set)

    for u, ips in user_ips.items():
        for ip in ips:
            ip_to_users[ip].add(u)
    for u, macs in user_macs.items():
        for mac in macs:
            mac_to_users[mac].add(u)

    # Analisar cada linha
    suspeitas = []
    for _, row in df.iterrows():
        user = row.get("USER")
        field = row.get("FIELD")
        valor = str(row.get("ENTRADA"))
        motivos = []

        if user not in user_main_ip or user not in user_main_mac:
            suspeitas.append("")
            continue

        ip_main = user_main_ip[user]
        mac_main = user_main_mac[user]

        if field == "IP":
            if valor != ip_main:
                motivos.append("IP suspeito")
            if len(ip_to_users[valor]) > 1:
                motivos.append("Possível invasão")

        if field == "MAC ADDRESS":
            if valor != mac_main:
                motivos.append("MAC suspeito")
            if len(mac_to_users[valor]) > 1:
                motivos.append("Possível invasão")

        suspeitas.append(", ".join(set(motivos)))

    df['SUSPEITO'] = suspeitas
    return df

def combinar_arquivos():
    arquivos = selecionar_arquivos()
    if not arquivos:
        return

    dfs = []
    for caminho in arquivos:
        df = ler_arquivo(caminho)
        if df is not None:
            dfs.append(df)

    if not dfs:
        messagebox.showwarning("Aviso", "Nenhum arquivo válido foi carregado.")
        return

    try:
        df_final = pd.concat(dfs, ignore_index=True)
        df_final = analisar_suspeitos(df_final)
        salvar_como_csv(df_final)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao combinar os arquivos:\n{e}")

if __name__ == "__main__":
    combinar_arquivos()
