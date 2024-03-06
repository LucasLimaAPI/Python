print("""
████████████████████████████████████████████████████████████████████████████████████████████████████
█─▄─▄─█─▄▄─█─▄▄▄─█─▄▄─█▄─▀█▀─▄█▄─▄▄─█─▄▄─█▄─▀█▀─▄█▄─▄▄─███▄─▄▄─█▄─▀─▄█▄─▄▄─█▄─▄▄▀█▄─▄▄─█─▄▄▄▄█─▄▄▄▄█
███─███─██─█─███▀█─██─██─█▄█─███─▄███─██─██─█▄█─███─▄█▀████─▄█▀██▀─▀███─▄▄▄██─▄─▄██─▄█▀█▄▄▄▄─█▄▄▄▄─█
▀▀▄▄▄▀▀▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▀▀▀▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▀▀▄▄▄▄▄▀▄▄█▄▄▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀\n""")

print('1. Cadastrar Restaurante ')
print('2. Listar Restaurante ')
print('3. Ativar Restaurante ')
print('4. Sair\n')#\n pula uma linha

#snake case para variáveis.
opcao_escolhida = int(input('Escolha uma opção: '))#Listar restaurantes ou assim por diante
print(f'Você escolheu a opção: {opcao_escolhida}')

if opcao_escolhida == 1:
    print('Cadastrar Restaurante')
elif opcao_escolhida == 2:
    print('Listar Restaurantes')
elif opcao_escolhida == 3:
    print('Ativar Restaurante')
else:
    print('Encerrando Programa...')


