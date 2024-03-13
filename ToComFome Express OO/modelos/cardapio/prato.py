from modelos.cardapio.item_cardapio import ItemCardapio
#Herança
class Prato(ItemCardapio):

    def __init__(self, nome, price, description):
        super().__init__(nome, price)# super > vai permitir que a gente acesse informações de outra classe neste caso a classe cardápio, ou seja herdamos os atributos e isso nos permito utilizar esses atribudos e adicionar outros.
        self.description = description

    def __str__(self):
        return self._nome