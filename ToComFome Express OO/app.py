from modelos.restaurante import Restaurante
from modelos.cardapio.drink import Drink
from modelos.cardapio.prato import Prato


restaurante_praca = Restaurante('Praça', 'Gourmet')
bebida_suco = Drink('Soda Cola', 5.00, 'grande')
prato_comida = Prato('Baião de Dois', 20.00, 'Para Dois')
restaurante_praca.add_bebida_no_cardapio(bebida_suco)
restaurante_praca.add_prato_no_cardapio(prato_comida)


# vai gerar um diretorio que vai armazenar os arquivos e codigos em bitcode "pycache"

def main():
    print(bebida_suco)
    print(prato_comida)

if __name__ == '__main__': # Vai ser nosso programa principal e vai conter metodo main, nao sera importado para outro script para ser executado.
    main()