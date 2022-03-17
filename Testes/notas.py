from tkinter import messagebox

nome= (input('Digite seu nome: '))
idade= int(input('Digite sua idade: '))

    
p1=int(input('Digita sua nota: '))
p2= int(input('Digite sua nota: '))
media= (p1+p2)/2
     

if media < 10 & idade < 18:
    messagebox.showinfo("iNFO",\
        f'{nome} voce foi reprovado por falta de nota e por idade incompativel!')
elif media < 10:
    messagebox.showinfo(f'INFO',\
       f'{nome} voce foi reprovado por falta de nota!!')
elif idade < 18:
     messagebox.showinfo('iNFO',\
     f'{nome} voce foi reprovado pois sua idade é incompativel!!')
else:
    messagebox.showinfo('INFO',\
         'Você passou!!')
        




