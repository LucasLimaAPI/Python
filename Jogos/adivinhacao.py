print("*************************************")
print("Bem vindo ao meu jogo de Adivinhação!")
print("*************************************")

numero_secreto = 22
total_de_tentativas = 3
rodada = 1

while(rodada <= total_de_tentativas):
  print("Tentativa",rodada,"de", total_de_tentativas)
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
      rodada = rodada + 1

print("Fim de jogo.")
