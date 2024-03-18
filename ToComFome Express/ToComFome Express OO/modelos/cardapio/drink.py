from modelos.cardapio.item_cardapio import ItemCardapio
#Herança.
class Drink(ItemCardapio):
    def __init__(self, nome ,price, size):
        super().__init__(nome, price) #__init_ para acessar os metodos e atibutos que queremos.
        self.size = size

    def __str__(self):
        return self._nome
    
    def aplicar_desconto(self):
        self._preco -= (self._preco * 0.08)