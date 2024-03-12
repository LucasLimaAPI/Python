from modelos.restaurante import Restaurante



restaurante_praca = Restaurante('Cantina', 'Gourmet')
restaurante_praca.receber_avaliacao('Lucas', 5)
restaurante_praca.receber_avaliacao('Lais', 3)
restaurante_praca.receber_avaliacao('Emy', 3)



# vai gerar um diretorio que vai armazenar os arquivos e codigos em bitcode "pycache"

def main():
    Restaurante.listar_restaurantes()

if __name__ == '__main__': # Vai ser nosso programa principal e vai conter metodo main, nao sera importado para outro script para ser executado.
    main()