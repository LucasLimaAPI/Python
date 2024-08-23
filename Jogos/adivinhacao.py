import random

print("*************************************")
print("Bem vindo ao meu jogo de Adivinhação!")
print("*************************************")

numero_secreto = random.randint(1,101)
total_de_tentativas = 3

print(numero_secreto)

for rodada in range(1,total_de_tentativas + 1):
  print(f"Tentativa {rodada} de {total_de_tentativas}")
  palpite = int(input('Digite o seu número: '))

  if palpite < 1 or palpite > 100:
    print("Você deve digitar um número entre 1 e 100!")
    continue

  acertou = numero_secreto == palpite
  maior = palpite > numero_secreto
  menor = palpite < numero_secreto
  print("Você digitou", palpite)

  if acertou:
    print("Você Acertou!!")
    break
  else:
    if maior:
     print("Você errou, talvez seu número seja menor!")
    else:
      menor
      print("Você errou, talvez seu número seja maior!")

print("Fim de jogo.")
