from modelos.avaliacao import Avaliacao
class Restaurante:
    restaurantes = []

#__str__ = ele e um metoto especial que pega um objeto em formato de texto e mostra esta informação, a gente pode escolher o nome categoria o ativo podemos pode escolher e definir.
#__init__ = um método construtor sempre onde que criarmos uma instância de um objeto esse método é chamado
    
    def __init__(self, nome, categoria):#Para nao confundir sempre passamos como primeiro parametro "self" para entender que se trata do objeto que nos referenciamos naquele momento
        self._nome = nome.title()
        self._categoria = categoria.title()
        self._ativo= False # o underline deixará como protegido e informa que este atributo não deve ser mexido
        self._avaliacao = []
        Restaurante.restaurantes.append(self)

    def __str__(self):
        return f'{self._nome} | {self._categoria}'
    
    @classmethod#Metodo da classe 
    def listar_restaurantes(cls):
        print(f'{'Nome do restaurante'.ljust(25)} | {'Categoria'.ljust(25)} | {'Avaliação'.ljust(25)} | {'Status'}')
        for restaurante in cls.restaurantes:
            print(f'{restaurante._nome.ljust(25)} | {restaurante._categoria.ljust(25)} | {str(restaurante.media_avaliacoes).ljust(25)} | {restaurante.ativo}')

#@ decorator do python
    @property# podemos pegar um produto no caso um ativo e modificar a forma que ele será lido.
    def ativo(self):
        return '✅' if self._ativo else '❌'
    
    def alternar_estado(self):
        self._ativo = not self._ativo
        
    def receber_avaliacao(self, cliente, nota):
        if 0 < nota <= 5:
            avaliacao = Avaliacao(cliente, nota)
            self._avaliacao.append(avaliacao)

    @property # agora seremos capaz de ler essas informações
    def media_avaliacoes(self):
        if not self._avaliacao:
            return '-'
        soma_das_notas = sum(avaliacao._nota for avaliacao in self._avaliacao)
        quantidade_notas = len(self._avaliacao)
        media = round(soma_das_notas / quantidade_notas, 1)
        return media
