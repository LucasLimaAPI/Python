#Bibliotecas
import os

#Vamos criar uma lista para armazenar os dados, porém como receberemos muitos dados faremos um dicionario com estrutura de chave e valor
restaurantes = [{'nome':'Praça', 'categoria':'Brasileira', 'ativo':False}, 
                {'nome':'Madera', 'categoria':'Portuguesa', 'ativo':False},
                {'nome':'Ço-vo', 'categoria':'francesa', 'ativo':False}]



def exibir_nome_do_programa():
      print("""
████████████████████████████████████████████████████████████████████████████████████████████████████
█─▄─▄─█─▄▄─█─▄▄▄─█─▄▄─█▄─▀█▀─▄█▄─▄▄─█─▄▄─█▄─▀█▀─▄█▄─▄▄─███▄─▄▄─█▄─▀─▄█▄─▄▄─█▄─▄▄▀█▄─▄▄─█─▄▄▄▄█─▄▄▄▄█
███─███─██─█─███▀█─██─██─█▄█─███─▄███─██─██─█▄█─███─▄█▀████─▄█▀██▀─▀███─▄▄▄██─▄─▄██─▄█▀█▄▄▄▄─█▄▄▄▄─█
▀▀▄▄▄▀▀▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▀▀▀▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▀▀▄▄▄▄▄▀▄▄█▄▄▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀\n""")


def exibir_opcoes():
      '''Esta função é responsável por exibir as opções ao usuário'''
      print('1. Cadastrar Restaurante ')
      print('2. Listar Restaurante ')
      print('3. Alternar Estado do Restaurante ')
      print('4. Sair')#\n pula uma linha


def finalizar_app():
     '''Esta função encerra a aplicação'''
     exibir_subtitulo('Encerrando a aplicação')#este comando vai executar o comando cls que irá limpar o console quando esta funcao for executada.


def voltar_menu():
      '''Esta função é responsável por retornar de volta ao menu principal'''
      input('Digite uma tecla para voltar ao menu principal ')
      main()


def switch_status():
      '''Essa função é resposável por alternar o status do restaurante'''
      exibir_subtitulo('Alternando estado do restaurante')
      nome_restaurante= input('Digite o nome do restaurante que deseja alternar o estado: ')
      find_restaurant = False

      for restaurante in restaurantes:
            if nome_restaurante == restaurante['nome']:
                  find_restaurant = True
                  restaurante['ativo']= not restaurante['ativo']#Com este proposito ele ira reverter os valors se tiver true vai ficar false e vice e versa.
                  mensagem = f'O restaurante {nome_restaurante} foi ativado com sucesso.' if restaurante['ativo'] else f'O restaurante {nome_restaurante} foi destivado com sucesso'
                  print(mensagem)

      if not find_restaurant:
            print('O restaurante não foi encontrado.')

      voltar_menu()


def opcao_invalida():
      """Esta função é responsável por invalidas seleções erradas"""
      print('Opção Inválida!')
      voltar_menu()


def exibir_subtitulo(texto):
      '''Essa função é responsável por exibir os subtitulos'''
      os.system('cls')
      linha = '#' * (len(texto) + 4)
      print(linha)
      print(texto)
      print(linha)
      print()


def cadastrar_restaurante():
   
      '''Essa função é responsável por cadastrar um novo restaurante.'''#docsctrings resposáveis por facilitar o entendimento do codigo
      exibir_subtitulo('Cadastro de um novo retaurante.\n')
      nome_do_restaurante = input('Digite o nome do restaurante que deseja cadastrar: ')
      categoria = input(f'Digite o nome da categoria do restaurante {nome_do_restaurante}: ')
      dados_do_restaurante = {'nome':nome_do_restaurante,'categoria':categoria, 'ativo':False}
      restaurantes.append(dados_do_restaurante)#Pegar o nome e colocar na lista restaurantes.
      print(f'O restaurante {nome_do_restaurante} foi cadastrado.\n')
      
 

      voltar_menu()


def listar_restaurantes():
      
      '''Essa função é responsável por listar os restaurantes cadastrados.'''
      exibir_subtitulo('Listando os restaurantes\n')
      
      print(f'{'Nome do restaurante'.ljust(22)} | {'Categoria'.ljust(20)} | Status')

      for restaurante in restaurantes:
            nome_restaurante = restaurante['nome']
            categoria = restaurante['categoria']
            ativo = 'ativado' if restaurante['ativo'] else 'desativado'
            print(f'- {nome_restaurante.ljust(20)} | {categoria.ljust(20)} | {ativo}') #ljust() uma funcao que separa de forma

      

      voltar_menu()


def escolher_opcao():
      '''Esta função é responsável por selecionar a opção selecionada'''
      try:
            opcao_escolhida = int(input('Escolha uma opção: '))#Listar restaurantes ou assim por diante

            print(f'Você escolheu a opção: {opcao_escolhida}')
            if opcao_escolhida == 1:
                 cadastrar_restaurante()
            elif opcao_escolhida == 2:
                 listar_restaurantes()
            elif opcao_escolhida == 3:
                  switch_status()
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
