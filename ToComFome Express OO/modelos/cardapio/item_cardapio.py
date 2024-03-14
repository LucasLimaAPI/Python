from abc import ABC, abstractmethod
#Classe abstrata = todas as classes derivadas da classe item cardápio tenha uma função que apliquem desconto e cada desconto terá um valor diferente.
class ItemCardapio(ABC):
    def __init__(self, nome , price):
        self._nome = nome
        self._preco = price

    @abstractmethod
    def aplicar_desconto(self):
        pass