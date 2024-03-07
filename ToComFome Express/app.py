#Bibliotecas
import os

#Vamos criar uma lista para armazenar os dados, porém como receberemos muitos dados faremos um dicionario com estrutura de chave e valor
restaurantes = [{'nome':'Praça', 'categoria':'Brasileira', 'ativo':False}, 
                {'nome':'Madera', 'categoria':'Portuguesa', 'ativo':True},
                {'nome':'Ço-vo', 'categoria':'francesa', 'ativo':False}]

def exibir_nome_do_programa():
      print("""
████████████████████████████████████████████████████████████████████████████████████████████████████
█─▄─▄─█─▄▄─█─▄▄▄─█─▄▄─█▄─▀█▀─▄█▄─▄▄─█─▄▄─█▄─▀█▀─▄█▄─▄▄─███▄─▄▄─█▄─▀─▄█▄─▄▄─█▄─▄▄▀█▄─▄▄─█─▄▄▄▄█─▄▄▄▄█
███─███─██─█─███▀█─██─██─█▄█─███─▄███─██─██─█▄█─███─▄█▀████─▄█▀██▀─▀███─▄▄▄██─▄─▄██─▄█▀█▄▄▄▄─█▄▄▄▄─█
▀▀▄▄▄▀▀▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▀▀▀▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▀▀▄▄▄▄▄▀▄▄█▄▄▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀\n""")


def exibir_opcoes():
      print('1. Cadastrar Restaurante ')
      print('2. Listar Restaurante ')
      print('3. Ativar Restaurante ')
      print('4. Sair')#\n pula uma linha


def finalizar_app():
     exibir_subtitulo('Encerrando a aplicação')#este comando vai executar o comando cls que irá limpar o console quando esta funcao for executada.


def voltar_menu():
      input('Digite uma tecla para voltar ao menu principal ')
      main()


def opcao_invalida():
      print('Opção Inválida!')
      voltar_menu()


def exibir_subtitulo(texto):
      os.system('cls')
      print(texto)
      print()


def cadastrar_restaurante():
      exibir_subtitulo('Cadastro de um novo retaurante.\n')
      nome_do_restaurante = input('Digite o nome do restaurante que deseja cadastrar: ')
      restaurantes.append(nome_do_restaurante)#Pegar o nome e colocar na lista restaurantes.
      print(f'O restaurante {nome_do_restaurante} foi cadastrado.\n')
      
      voltar_menu()


def listar_restaurantes():
      exibir_subtitulo('Listando os restaurantes\n')

      for restaurante in restaurantes:
            nome_restaurante = restaurante['nome']
            categoria = restaurante['categoria']
            ativo = restaurante['ativo']
            print(f'- {nome_restaurante} | {categoria} | {ativo}')

      voltar_menu()


def escolher_opcao():
      try:
            opcao_escolhida = int(input('Escolha uma opção: '))#Listar restaurantes ou assim por diante

            print(f'Você escolheu a opção: {opcao_escolhida}')
            if opcao_escolhida == 1:
                 cadastrar_restaurante()
            elif opcao_escolhida == 2:
                 listar_restaurantes()
            elif opcao_escolhida == 3:
                  print('Ativar Restaurante')
            elif opcao_escolhida == 4:
                  finalizar_app()
            else:
                  opcao_invalida()
      except:
            opcao_invalida()
  

#Da para falar que o arquivo é o arquivo principal  o interpretador cria variavel chamada __name__ se o name for "__main__" significa que este codigo nao sera importado por outros scripts de codigo python ou etc e ele vai ser o programa principal.
def main():
     os.system('cls')
     exibir_nome_do_programa()
     exibir_opcoes()
     escolher_opcao()

if __name__ == '__main__':
     main()
