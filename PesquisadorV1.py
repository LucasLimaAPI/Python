import time
import pandas as pd
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Criar janela para seleção de arquivos
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
if not file_path:
    messagebox.showerror("Erro", "Nenhum arquivo selecionado. O programa será encerrado.")
    exit()

chrome_driver_path = filedialog.askopenfilename(title="Selecione o ChromeDriver", filetypes=[("Executáveis", "*.exe")])
if not chrome_driver_path:
    messagebox.showerror("Erro", "ChromeDriver não selecionado. O programa será encerrado.")
    exit()

# Ler o arquivo Excel
df = pd.read_excel(file_path)
cpf_list = df["CPF"].astype(str).tolist()

# Configuração do Selenium
options = webdriver.ChromeOptions()
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Abrir o site da CVM
url = "https://sistemas.cvm.gov.br/asp/cvmwww/cadastro/formCad.asp"
driver.get(url)

# Aguardar o campo CPF carregar
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "NrPfPj")))

ultimo_captcha = None  # Armazena o último captcha digitado

# Loop para preencher os CPFs
for cpf in cpf_list:
    input("Pressione Enter para preencher o próximo CPF...")  
    try:
        # Aguarda o campo CPF aparecer
        cpf_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "NrPfPj"))
        )
        cpf_input.clear()
        cpf_input.send_keys(cpf)
        cpf_input.send_keys(Keys.RETURN)
        print(f"✅ CPF {cpf} preenchido com sucesso!")

        # Verifica se há um campo de captcha antes de prosseguir
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "strCAPTCHA"))
            )
            captcha_presente = True
        except:
            captcha_presente = False

        if captcha_presente:
            # Se o captcha for o mesmo da última vez, reutiliza
            if ultimo_captcha is None:
                captcha_code = simpledialog.askstring("Captcha", "Digite o captcha exibido na página:")
                if not captcha_code:
                    messagebox.showerror("Erro", "Nenhum captcha inserido. O programa será encerrado.")
                    driver.quit()
                    exit()
                ultimo_captcha = captcha_code  

            # Preencher captcha
            captcha_input = driver.find_element(By.NAME, "strCAPTCHA")
            captcha_input.clear()
            captcha_input.send_keys(ultimo_captcha)
            captcha_input.send_keys(Keys.RETURN)

            # Aguardar resposta da CVM
            time.sleep(2)

            # Verificar se o captcha foi aceito
            if "erro" in driver.page_source.lower():
                messagebox.showwarning("Aviso", "Captcha incorreto. Digite novamente.")
                ultimo_captcha = None  
                driver.execute_script("window.history.go(-1);")  
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "NrPfPj")))  
                continue  

            print("✅ Captcha validado com sucesso!")

        # Aguardar a página carregar
        time.sleep(3)

        # **🔍 VERIFICAÇÃO CORRIGIDA 🔍**
        try:
            mensagem = driver.find_element(By.CLASS_NAME, "Msg").text
            if "Nao foram encontrados participantes para esta consulta" in mensagem:
                status = "NÃO é profissional"
            else:
                status = "É profissional"
        except:
            status = "É profissional"  # Se o elemento não for encontrado, assume que é profissional

        # Salvar resultado no TXT
        with open("resultado_consulta.txt", "a", encoding="utf-8") as file:
            file.write(f"CPF {cpf} - {status}\n")

        print(f"📄 Resultado salvo: {cpf} {status}")

        # Voltar para a página anterior
        driver.execute_script("window.history.go(-1);")  
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "NrPfPj")))  

    except Exception as e:
        print(f"❌ Erro ao preencher CPF {cpf}: {e}")

driver.quit()
