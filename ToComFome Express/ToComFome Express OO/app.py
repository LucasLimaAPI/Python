from modelos.restaurante import Restaurante
from modelos.cardapio.drink import Drink
from modelos.cardapio.prato import Prato


restaurante_praca = Restaurante('Praça', 'Gourmet')
bebida_suco = Drink('Soda Cola', 5.00, 'Grande')
bebida_suco.aplicar_desconto()
prato_comida = Prato('Baião de Dois', 20.00, 'Preparado de arroz e feijão, usado prefencialmente o feijão de corda') 
prato_comida.aplicar_desconto()
restaurante_praca.add_no_cardapio(bebida_suco)
restaurante_praca.add_no_cardapio(prato_comida)

# vai gerar um diretorio que vai armazenar os arquivos e codigos em bitcode "pycache"

def main():
    restaurante_praca.exibir_cardapio
    

if __name__ == '__main__': # Vai ser nosso programa principal e vai conter metodo main, nao sera importado para outro script para ser executado.
    main()