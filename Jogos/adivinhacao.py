import random

print("*************************************")
print("Bem vindo ao meu jogo de Adivinhação!")
print("*************************************")

numero_secreto = random.randrange(1,101)
total_de_tentativas = 0
pontos = 1000

print("Qual nível de dificuldade?")
print("(1) Fácil (2) Médio (3) Díficil")
nivel = int(input("Defina o Nível:"))

if nivel == 1:
  total_de_tentativas = 20
elif nivel == 2:
  total_de_tentativas = 10
else:
  total_de_tentativas = 5


for rodada in range(1,total_de_tentativas + 1):
  print(f"Tentativa {rodada} de {total_de_tentativas}")

  palpite = int(input('Digite o seu número: '))

  if palpite < 1 or palpite > 100:
    print("Você deve digitar um número entre 1 e 100!")
    continue

  acertou = numero_secreto == palpite
  maior = palpite > numero_secreto
  menor = palpite < numero_secreto

  if acertou:
    print(f"Você Acertou e fez {pontos} pontos")
    break
  else:
    if maior:
     print("Você errou, talvez seu número seja menor!")
    elif menor :
      print("Você errou, talvez seu número seja maior!")
      pontos_perdidos = abs(numero_secreto - palpite) #abs = absoluto
      pontos = pontos - pontos_perdidos

print("Fim de jogo.")
