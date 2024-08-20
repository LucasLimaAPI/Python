print("*************************************")
print("Bem vindo ao meu jogo de Adivinhação!")
print("*************************************")

numero_secreto = 22

palpite: int = int(input('Digite o seu número: '))

print("Você digitou", palpite)

if numero_secreto == palpite:
  print("Você Acertou!!")
else:
  print("Você errou, o número era : ", numero_secreto)
