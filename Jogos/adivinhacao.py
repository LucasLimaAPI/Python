print("*************************************")
print("Bem vindo ao meu jogo de Adivinhação!")
print("*************************************")

numero_secreto = 22
palpite = int(input('Digite o seu número: '))
acertou = numero_secreto == palpite
maior = palpite > numero_secreto
menor = palpite < numero_secreto

print("Você digitou", palpite)

if acertou:
  print("Você Acertou!!")
else:
  if maior:
    print("Você errou, talvez seu número seja menor!")
  else:
    menor
    print("Você errou, talvez seu número seja maior!")

print("Fim de jogo.")
